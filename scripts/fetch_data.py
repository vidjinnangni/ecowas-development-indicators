"""
Récupère des indicateurs économiques et d'aide au développement
pour les 15 pays de la CEDEAO via l'API World Bank (v2).

Documentation officielle : https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

Aucune clé API n'est requise. Les résultats sont mis en cache localement
dans data/raw/ pour éviter de re-télécharger à chaque exécution.
"""

import json
import time
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.worldbank.org/v2/country"

# Les 15 pays de la CEDEAO (codes ISO3)
PAYS_CEDEAO = [
    "BEN", "BFA", "CPV", "CIV", "GMB", "GHA", "GIN", "GNB",
    "LBR", "MLI", "NER", "NGA", "SEN", "SLE", "TGO",
]

# Indicateurs : Économie & aide au développement
INDICATEURS = {
    "NY.GDP.MKTP.KD.ZG": "croissance_pib",
    "NY.GDP.PCAP.CD": "pib_par_habitant",
    "DT.ODA.ODAT.GN.ZS": "aide_publique_dev_pct_rnb",
    "BX.KLT.DINV.WD.GD.ZS": "ide_entrees_pct_pib",
    "FP.CPI.TOTL.ZG": "inflation",
    "DT.DOD.DECT.GN.ZS": "dette_exterieure_pct_rnb",
}

ANNEE_DEBUT = 2000
ANNEE_FIN = 2023


def requete_avec_reessai(url: str, params: dict, max_essais: int = 4) -> dict:
    """Effectue la requête GET avec réessai (backoff) en cas d'erreur transitoire
    (l'API World Bank renvoie parfois un 400/503 passager sans raison liée aux données)."""
    derniere_erreur = None
    for essai in range(1, max_essais + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            derniere_erreur = e
            attente = 2 ** essai  # 2s, 4s, 8s, 16s
            print(f"    Erreur HTTP ({e}), nouvel essai dans {attente}s "
                  f"({essai}/{max_essais})...")
            time.sleep(attente)
    raise derniere_erreur


def fetch_indicator(code_indicateur: str) -> list:
    """Récupère toutes les pages de résultats pour un indicateur, tous pays CEDEAO."""
    pays_str = ";".join(PAYS_CEDEAO)
    url = f"{BASE_URL}/{pays_str}/indicator/{code_indicateur}"

    resultats = []
    page = 1
    while True:
        params = {
            "format": "json",
            "per_page": 1000,
            "date": f"{ANNEE_DEBUT}:{ANNEE_FIN}",
            "page": page,
        }
        data = requete_avec_reessai(url, params)

        # data[0] = métadonnées de pagination, data[1] = enregistrements
        if len(data) < 2 or data[1] is None:
            break

        resultats.extend(data[1])

        meta = data[0]
        if page >= meta.get("pages", 1):
            break
        page += 1
        time.sleep(0.5)  # politesse envers l'API, entre deux pages

    return resultats


def main():
    for code, nom_fichier in INDICATEURS.items():
        print(f"Récupération de {code} ({nom_fichier})...")
        resultats = fetch_indicator(code)
        chemin = RAW_DIR / f"{nom_fichier}.json"
        with open(chemin, "w") as f:
            json.dump(resultats, f, indent=2)
        print(f"  -> {len(resultats)} enregistrements sauvegardés dans {chemin}")
        time.sleep(1)  # pause entre deux indicateurs, pour ne pas enchaîner trop vite

    print("\nTerminé. Lance ensuite scripts/clean_data.py")


if __name__ == "__main__":
    main()
