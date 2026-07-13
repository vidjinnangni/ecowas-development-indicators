"""
Transforme les fichiers JSON bruts (un par indicateur) en un unique
CSV "tidy" : une ligne = pays x indicateur x année.
"""

import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

NOMS_INDICATEURS = {
    "croissance_pib": "Croissance du PIB (%)",
    "pib_par_habitant": "PIB par habitant (US$)",
    "aide_publique_dev_pct_rnb": "Aide publique au développement (% RNB)",
    "ide_entrees_pct_pib": "IDE entrées nettes (% PIB)",
    "inflation": "Inflation (%)",
    "dette_exterieure_pct_rnb": "Dette extérieure (% RNB)",
}


def charger_indicateur(nom_fichier: str) -> pd.DataFrame:
    chemin = RAW_DIR / f"{nom_fichier}.json"
    with open(chemin) as f:
        records = json.load(f)

    lignes = []
    for r in records:
        # La structure standard de l'API World Bank pour chaque enregistrement :
        # {"indicator": {...}, "country": {"id": "BJ", "value": "Benin"},
        #  "countryiso3code": "BEN", "date": "2020", "value": 3.4, ...}
        if r.get("value") is None:
            continue  # valeur manquante à la source, on l'ignore plutôt que de deviner
        lignes.append({
            "pays": r["country"]["value"],
            "code_iso3": r["countryiso3code"],
            "annee": int(r["date"]),
            "indicateur": nom_fichier,
            "valeur": r["value"],
        })

    return pd.DataFrame(lignes)


def main():
    fichiers_disponibles = [f.stem for f in RAW_DIR.glob("*.json")]
    if not fichiers_disponibles:
        raise FileNotFoundError(
            "Aucun fichier trouvé dans data/raw/. "
            "Lance d'abord scripts/fetch_data.py"
        )

    dfs = [charger_indicateur(nom) for nom in fichiers_disponibles]
    df = pd.concat(dfs, ignore_index=True)

    df["nom_indicateur"] = df["indicateur"].map(NOMS_INDICATEURS)
    df = df.sort_values(["pays", "indicateur", "annee"])

    chemin_sortie = PROCESSED_DIR / "indicateurs_cedeao.csv"
    df.to_csv(chemin_sortie, index=False)
    print(f"{len(df)} lignes -> {chemin_sortie}")
    print(f"Pays : {df['pays'].nunique()} | Indicateurs : {df['indicateur'].nunique()} "
          f"| Période : {df['annee'].min()}-{df['annee'].max()}")


if __name__ == "__main__":
    main()
