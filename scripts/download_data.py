"""Scarica tutti i dataset della tesi in data/raw/ e registra da dove vengono.

Uso (dalla cartella principale del progetto):

    uv run python scripts/download_data.py                 # tutti i dataset tranne Criteo
    uv run python scripts/download_data.py --criteo        # aggiunge Criteo, campione 10% (~ 1,4 milioni di righe)
    uv run python scripts/download_data.py --criteo-full   # Criteo completo (file grande, solo se serve)
    uv run python scripts/download_data.py --only telco hillstrom

Cosa fa:
1. scarica ogni dataset nella sua cartella, per esempio data/raw/telco/;
2. salta i file gia' presenti, quindi si puo' rilanciare senza problemi;
3. scrive results/data_manifest.json con fonte, data di download, dimensione e
   impronta SHA-256 di ogni file. L'impronta serve a dimostrare che i dati usati
   nella tesi sono sempre gli stessi, anche se la fonte online cambia.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
# Il registro sta in results/ (e non in data/) cosi' finisce su GitHub, mentre i dati no.
MANIFEST_PATH = PROJECT_ROOT / "results" / "data_manifest.json"

# Catalogo dei dataset: un'unica fonte di verita' su cosa scaricare e da dove.
DATASETS = {
    "telco": {
        "kind": "kaggle",
        "slug": "blastchar/telco-customer-churn",
        "page": "https://www.kaggle.com/datasets/blastchar/telco-customer-churn",
        "role": "Dataset principale: modelli, EMPC, survival analysis",
    },
    "iranian": {
        "kind": "url_zip",
        "url": "https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip",
        "page": "https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset",
        "role": "Dataset di controllo, piccolo",
    },
    "cell2cell": {
        "kind": "kaggle",
        "slug": "jpacse/datasets-for-churn-telecom",
        "page": "https://www.kaggle.com/datasets/jpacse/datasets-for-churn-telecom",
        "role": "Dataset di controllo, il piu' grande",
    },
    "hillstrom": {
        "kind": "url",
        # Stessa fonte usata da scikit-uplift (fetch_hillstrom).
        "url": "https://hillstorm1.s3.us-east-2.amazonaws.com/hillstorm_no_indices.csv.gz",
        "md5": "a68a81291f53a14f4e29002629803ba3",
        "page": "https://www.uplift-modeling.com/en/latest/api/datasets/fetch_hillstrom.html",
        "role": "Esperimento randomizzato per l'uplift modeling",
    },
    "criteo": {
        "kind": "url",
        # Stesse fonti usate da scikit-uplift (fetch_criteo).
        "url": "https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo10.csv.gz",
        "url_full": "https://criteo-bucket.s3.eu-central-1.amazonaws.com/criteo.csv.gz",
        "page": "https://huggingface.co/datasets/criteo/criteo-uplift",
        "role": "Facoltativo: test di scala per l'uplift",
        "optional": True,
    },
}


# --------------------------------------------------------------------------- utilita'

def file_hash(path: Path, algorithm: str = "sha256") -> str:
    """Calcola l'impronta di un file leggendolo a blocchi (funziona anche con file grandi)."""
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_url(url: str, dest: Path) -> None:
    """Scarica un URL in `dest`, scrivendo prima su un file temporaneo."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    print(f"  scarico {url}")
    with urllib.request.urlopen(url, timeout=120) as response, tmp.open("wb") as out:
        shutil.copyfileobj(response, out, length=1024 * 1024)
    tmp.replace(dest)




def unzip(zip_path: Path, dest_dir: Path) -> None:
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest_dir)


def data_files(folder: Path) -> list[Path]:
    """Tutti i file di dati in una cartella (esclusi i file temporanei)."""
    return sorted(p for p in folder.rglob("*") if p.is_file() and not p.name.endswith(".part"))


# --------------------------------------------------------------------------- download

def fetch(name: str, meta: dict, criteo_full: bool = False) -> list[Path]:
    folder = RAW_DIR / name
    existing = data_files(folder) if folder.exists() else []
    if existing:
        print(f"[{name}] gia' presente ({len(existing)} file), salto il download")
        return existing

    print(f"[{name}] {meta['role']}")
    if meta["kind"] == "kaggle":
        kaggle_download(meta["slug"], folder)
    elif meta["kind"] == "url_zip":
        zip_path = folder / Path(meta["url"]).name.replace("+", "_")
        download_url(meta["url"], zip_path)
        unzip(zip_path, folder)
    elif meta["kind"] == "url":
        url = meta["url_full"] if (criteo_full and "url_full" in meta) else meta["url"]
        dest = folder / Path(url).name
        download_url(url, dest)
        if "md5" in meta and file_hash(dest, "md5") != meta["md5"]:
            dest.unlink()
            raise RuntimeError("il file scaricato non corrisponde all'impronta attesa (download corrotto)")
    else:
        raise ValueError(f"tipo di fonte sconosciuto: {meta['kind']}")
    return data_files(folder)


def update_manifest(name: str, meta: dict, files: list[Path]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    previous = manifest.get(name, {})
    manifest[name] = {
        "role": meta["role"],
        "source_page": meta["page"],
        "source": meta.get("slug") or meta.get("url"),
        # la data del primo download resta quella originale
        "downloaded_at": previous.get("downloaded_at")
        or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": [
            {
                "path": str(p.relative_to(RAW_DIR)),
                "bytes": p.stat().st_size,
                "sha256": file_hash(p),
            }
            for p in files
        ],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scarica i dataset della tesi in data/raw/")
    parser.add_argument("--only", nargs="+", choices=sorted(DATASETS), help="scarica solo questi dataset")
    parser.add_argument("--criteo", action="store_true", help="includi Criteo (campione 10%%)")
    parser.add_argument("--criteo-full", action="store_true", help="includi Criteo completo")
    args = parser.parse_args(argv)

    names = args.only or [
        n for n, m in DATASETS.items() if not m.get("optional") or args.criteo or args.criteo_full
    ]

    failures = {}
    for name in names:
        meta = DATASETS[name]
        try:
            files = fetch(name, meta, criteo_full=args.criteo_full)
            update_manifest(name, meta, files)
            print(f"[{name}] ok: {', '.join(p.name for p in files)}")
        except Exception as exc:  # un dataset che fallisce non blocca gli altri
            failures[name] = str(exc)
            print(f"[{name}] ERRORE: {exc}")
            print(f"[{name}] in alternativa scaricalo a mano da {meta['page']} "
                  f"e mettilo in {RAW_DIR / name}, poi rilancia lo script.")

    print()
    if failures:
        print(f"Completato con {len(failures)} errori: {', '.join(failures)}")
        return 1
    print(f"Tutto scaricato. Registro delle fonti: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
