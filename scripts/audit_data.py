"""Controlla che i dati scaricati contengano davvero quello che serve alla tesi.

Uso (dopo scripts/download_data.py):

    uv run python scripts/audit_data.py

Per ogni file in data/raw/ stampa e salva in results/data_audit.md:
- righe, colonne, valori mancanti, righe duplicate;
- la distribuzione della variabile target (churn, oppure visit/conversion per l'uplift);
- quante righe hanno davvero l'etichetta (alcuni file di test non ce l'hanno);
- se ci sono le colonne richieste da ogni domanda di ricerca:
    * RQ1-RQ3 (chi contattare): target di churn binario + variabili descrittive;
    * RQ4 (quando intervenire): una durata, cioe' da quanto tempo il cliente e' attivo;
    * RQ5 (uplift): una colonna di trattamento assegnato a caso + un esito.

Il file results/data_audit.md e' la base del paragrafo "Dataset" del capitolo di metodologia.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_PATH = PROJECT_ROOT / "results" / "data_audit.md"

# Cosa ci aspettiamo da ogni dataset. I nomi delle colonne sono confrontati
# ignorando maiuscole, spazi e simboli (per esempio "Subscription  Length").
EXPECTED = {
    "telco": {"type": "churn", "target": ["churn"], "duration": ["tenure"]},
    "iranian": {"type": "churn", "target": ["churn"], "duration": ["subscriptionlength"]},
    "cell2cell": {"type": "churn", "target": ["churn"], "duration": ["monthsinservice"]},
    "hillstrom": {"type": "uplift", "treatment": ["segment"], "outcomes": ["visit", "conversion", "spend"]},
    "criteo": {"type": "uplift", "treatment": ["treatment"], "outcomes": ["visit", "conversion"], "optional": True},
}

DATA_SUFFIXES = (".csv", ".csv.gz", ".txt", ".xlsx", ".xls")


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lookup = {norm(c): c for c in df.columns}
    for cand in candidates:
        if cand in lookup:
            return lookup[cand]
    return None


def load(path: Path) -> pd.DataFrame:
    if path.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    # sep=None: pandas riconosce da solo virgola, punto e virgola o tabulazione
    return pd.read_csv(path, sep=None, engine="python")


def num(n: int) -> str:
    """Numero con il punto delle migliaia, all'italiana: 7043 -> 7.043."""
    return f"{n:,}".replace(",", ".")


def fmt_pct(x: float) -> str:
    return f"{x:.1%}".replace(".", ",")


def audit_file(dataset: str, path: Path, expected: dict) -> tuple[list[str], dict[str, str]]:
    """Restituisce le righe di report in markdown e l'esito dei requisiti."""
    df = load(path)
    lines = [f"### {dataset} – `{path.relative_to(RAW_DIR)}`", ""]
    lines.append(f"- Righe: **{num(len(df))}**, colonne: **{df.shape[1]}**")
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        lines.append("- Valori mancanti: nessuno")
    else:
        top = ", ".join(f"`{c}` ({n})" for c, n in missing.head(5).items())
        lines.append(f"- Valori mancanti in {len(missing)} colonne; le principali: {top}")
    # Attenzione: valori vuoti scritti come spazio (caso noto: TotalCharges nel Telco)
    blanks = [c for c in df.select_dtypes(exclude="number").columns
              if df[c].astype(str).str.strip().eq("").any()]
    if blanks:
        lines.append(f"- Celle con solo spazi (sono mancanti nascosti): {', '.join(f'`{c}`' for c in blanks)}")
    lines.append(f"- Righe duplicate: {int(df.duplicated().sum())}")

    results: dict[str, str] = {}
    if expected["type"] == "churn":
        target = find_col(df, expected["target"])
        if target is None:
            lines.append("- **Target di churn: NON TROVATO**")
            results["Target churn binario (RQ1-RQ3)"] = "NO"
        else:
            labelled = df[target].notna().sum()
            dist = df[target].value_counts(normalize=True, dropna=True)
            dist_txt = ", ".join(f"{k}: {fmt_pct(v)}" for k, v in dist.items())
            lines.append(f"- Target `{target}`: {dist_txt}")
            lines.append(f"- Righe con etichetta: {num(labelled)} su {num(len(df))}")
            if labelled == 0:
                # tipico dei file "holdout" delle competizioni: utile solo come dati senza etichetta
                results["Target churn binario (RQ1-RQ3)"] = "SENZA ETICHETTA (file di test, non usabile per addestrare)"
            elif dist.size == 2:
                results["Target churn binario (RQ1-RQ3)"] = "OK"
            else:
                results["Target churn binario (RQ1-RQ3)"] = f"DA VERIFICARE ({dist.size} valori diversi)"
        duration = find_col(df, expected["duration"])
        if duration is None:
            lines.append("- **Durata del rapporto (per la survival): NON TROVATA**")
            results["Durata per la survival (RQ4)"] = "NO"
        else:
            d = pd.to_numeric(df[duration], errors="coerce")
            lines.append(f"- Durata `{duration}`: da {d.min():g} a {d.max():g}, mediana {d.median():g}")
            results["Durata per la survival (RQ4)"] = "OK"
    else:
        treatment = find_col(df, expected["treatment"])
        if treatment is None:
            lines.append("- **Colonna di trattamento: NON TROVATA**")
            results["Trattamento + esito per l'uplift (RQ5)"] = "NO"
        else:
            groups = df[treatment].value_counts(normalize=True)
            lines.append("- Trattamento `{}`: {}".format(
                treatment, ", ".join(f"{k}: {fmt_pct(v)}" for k, v in groups.items())))
            found = [c for c in (find_col(df, [o]) for o in expected["outcomes"]) if c]
            for c in found:
                if df[c].nunique() <= 2:
                    lines.append(f"- Esito `{c}`: media {fmt_pct(df[c].mean())}")
                else:
                    lines.append(f"- Esito `{c}`: media {df[c].mean():.2f}")
            results["Trattamento + esito per l'uplift (RQ5)"] = "OK" if found else "NO"

    lines.append(f"- Colonne: {', '.join(f'`{c}`' for c in df.columns)}")
    lines.append("")
    return lines, results


def main() -> int:
    if not RAW_DIR.exists():
        print("Cartella data/raw non trovata: lancia prima scripts/download_data.py")
        return 1

    report = ["# Controllo dei dati", "",
              "Generato da `scripts/audit_data.py`. Non modificare a mano: rilancia lo script.", ""]
    summary: list[tuple[str, str, str]] = []

    for dataset, expected in EXPECTED.items():
        folder = RAW_DIR / dataset
        files = [p for p in sorted(folder.rglob("*")) if p.is_file() and p.name.lower().endswith(DATA_SUFFIXES)] \
            if folder.exists() else []
        if not files:
            if expected.get("optional"):
                report += [f"### {dataset}", "", "- Non scaricato (facoltativo)", ""]
                summary.append((dataset, "File presenti", "FACOLTATIVO, non scaricato"))
            else:
                report += [f"### {dataset}", "", "- Nessun file trovato (non scaricato?)", ""]
                summary.append((dataset, "File presenti", "NO"))
            continue
        for path in files:
            try:
                lines, results = audit_file(dataset, path, expected)
            except Exception as exc:
                lines, results = [f"### {dataset} – `{path.name}`", "", f"- ERRORE in lettura: {exc}", ""], \
                    {"Lettura del file": "ERRORE"}
            report += lines
            summary += [(f"{dataset} ({path.name})", req, res) for req, res in results.items()]

    table = ["## Riepilogo", "", "| Dataset | Requisito | Esito |", "| --- | --- | --- |"]
    table += [f"| {d} | {r} | {e} |" for d, r, e in summary]
    report = report[:4] + table + ["", "## Dettaglio per file", ""] + report[4:]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(table))
    print(f"\nReport completo: {REPORT_PATH}")
    problems = [s for s in summary if s[2] in ("NO", "ERRORE") or s[2].startswith("DA VERIFICARE")]
    if problems:
        print(f"\nATTENZIONE: {len(problems)} requisiti non soddisfatti, vedi il riepilogo.")
        return 2
    print("\nTutti i requisiti obbligatori sono soddisfatti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
