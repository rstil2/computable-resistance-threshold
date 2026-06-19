"""
cBioPortal REST helpers for public cohort assembly.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_URL = "https://www.cbioportal.org/api"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"


def _get(path: str, *, timeout: int = 120, retries: int = 3) -> Any:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    last_err: Optional[Exception] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"cBioPortal request failed: {url}") from last_err


def _post(path: str, body: dict, *, timeout: int = 300, retries: int = 3) -> Any:
    url = f"{BASE_URL}{path}"
    payload = json.dumps(body).encode()
    last_err: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else []
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"cBioPortal POST failed: {url}") from last_err


def fetch_patient_table(study_id: str, *, cache: bool = True) -> List[Dict[str, str]]:
    """Merge PATIENT + SAMPLE clinical attributes into one row per patient."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{study_id}_clinical.json"
    if cache and cache_file.exists():
        with open(cache_file) as fh:
            return json.load(fh)

    pat = _get(f"/studies/{study_id}/clinical-data?clinicalDataType=PATIENT&pageSize=50000")
    smp = _get(f"/studies/{study_id}/clinical-data?clinicalDataType=SAMPLE&pageSize=50000")

    rows: Dict[str, Dict[str, str]] = {}
    for rec in pat:
        rows.setdefault(rec["patientId"], {})[rec["clinicalAttributeId"]] = rec["value"]
    for rec in smp:
        d = rows.setdefault(rec["patientId"], {})
        if rec["clinicalAttributeId"] not in d:
            d[rec["clinicalAttributeId"]] = rec["value"]

    out = [{"patientId": pid, **attrs} for pid, attrs in rows.items()]
    if cache:
        with open(cache_file, "w") as fh:
            json.dump(out, fh, indent=2)
    return out


def mutation_profile_id(study_id: str) -> Optional[str]:
    cache_file = CACHE_DIR / f"{study_id}_mutation_profile.txt"
    if cache_file.exists():
        return cache_file.read_text().strip() or None
    profiles = _get(f"/studies/{study_id}/molecular-profiles")
    mp = None
    for p in profiles:
        if p.get("molecularAlterationType", "").startswith("MUTATION"):
            mp = p["molecularProfileId"]
            break
    if mp:
        cache_file.write_text(mp)
    return mp


def fetch_study_samples(study_id: str, *, cache: bool = True) -> List[dict]:
    cache_file = CACHE_DIR / f"{study_id}_samples.json"
    if cache and cache_file.exists():
        with open(cache_file) as fh:
            return json.load(fh)
    samples = _get(f"/studies/{study_id}/samples?pageSize=50000")
    if cache:
        with open(cache_file, "w") as fh:
            json.dump(samples, fh)
    return samples


def choose_baseline_sample(samples: List[dict]) -> Dict[str, str]:
    """
    Map patientId -> sampleId for baseline sequencing.
    Prefer Pre-treatment / primary tumour samples.
    """
    by_patient: Dict[str, List[dict]] = {}
    for s in samples:
        by_patient.setdefault(s["patientId"], []).append(s)

    chosen: Dict[str, str] = {}
    for pid, pts in by_patient.items():
        ids = [s["sampleId"] for s in pts]
        pre = [sid for sid in ids if sid.endswith("_Pre") or sid.endswith("-Pre") or "_Pre" in sid or "-pre" in sid.lower()]
        if pre:
            chosen[pid] = sorted(pre)[0]
            continue
        primary = [
            s["sampleId"]
            for s in pts
            if "primary" in s.get("sampleType", "").lower()
        ]
        if primary:
            chosen[pid] = sorted(primary)[0]
            continue
        chosen[pid] = sorted(ids)[0]
    return chosen


def fetch_study_mutations(
    study_id: str,
    *,
    cache: bool = True,
    batch_size: int = 40,
) -> Dict[str, List[float]]:
    """
    Return sampleId -> list of VAFs for all samples in study.
    Cached to {study_id}_vafs_by_sample.json
    """
    cache_file = CACHE_DIR / f"{study_id}_vafs_by_sample.json"
    if cache and cache_file.exists():
        with open(cache_file) as fh:
            raw = json.load(fh)
        return {k: [float(x) for x in v] for k, v in raw.items()}

    mp = mutation_profile_id(study_id)
    if not mp:
        return {}

    samples = fetch_study_samples(study_id, cache=cache)
    sample_ids = [s["sampleId"] for s in samples]
    vafs_by_sample: Dict[str, List[float]] = {}

    for i in range(0, len(sample_ids), batch_size):
        batch = sample_ids[i : i + batch_size]
        body = {
            "sampleMolecularIdentifiers": [
                {"sampleId": sid, "molecularProfileId": mp} for sid in batch
            ]
        }
        print(f"    mutations batch {i // batch_size + 1}/{(len(sample_ids) + batch_size - 1) // batch_size} …")
        muts = _post("/mutations/fetch", body)
        for mut in muts:
            sid = mut.get("sampleId")
            alt = mut.get("tumorAltCount")
            ref = mut.get("tumorRefCount")
            if sid is None or alt is None or ref is None:
                continue
            total = alt + ref
            if total <= 0:
                continue
            vaf = alt / total
            if 0 < vaf < 1:
                vafs_by_sample.setdefault(sid, []).append(vaf)
        time.sleep(0.3)

    if cache:
        with open(cache_file, "w") as fh:
            json.dump(vafs_by_sample, fh)
    return vafs_by_sample


def patient_vaf_map(study_id: str, *, cache: bool = True) -> Dict[str, List[float]]:
    """patientId -> VAF list at chosen baseline sample."""
    samples = fetch_study_samples(study_id, cache=cache)
    baseline = choose_baseline_sample(samples)
    vafs_by_sample = fetch_study_mutations(study_id, cache=cache)
    out: Dict[str, List[float]] = {}
    for pid, sid in baseline.items():
        vafs = vafs_by_sample.get(sid, [])
        if vafs:
            out[pid] = vafs
    return out


def parse_purity(row: dict) -> Optional[float]:
    for key in ("TUMOR_PURITY", "TUMOR_PURITY_PERCENTAGE"):
        raw = row.get(key, "")
        if not raw:
            continue
        try:
            val = float(raw)
            return val / 100.0 if val > 1 else val
        except ValueError:
            continue
    return None


def cohort_summary(study_id: str) -> Dict[str, Any]:
    rows = fetch_patient_table(study_id)
    attrs = set()
    for r in rows:
        attrs.update(r.keys())
    return {
        "study_id": study_id,
        "n_patients": len(rows),
        "clinical_attributes": sorted(attrs),
    }
