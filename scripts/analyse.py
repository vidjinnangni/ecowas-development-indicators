"""
Analyse comparative des indicateurs économiques CEDEAO.

- Tendances régionales par indicateur
- Classement des pays sur la dernière année disponible
- Corrélation entre aide publique au développement et croissance du PIB
- Génération de graphiques
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

NOMS_COURTS = {
    "croissance_pib": "Croissance PIB (%)",
    "pib_par_habitant": "PIB/habitant (US$)",
    "aide_publique_dev_pct_rnb": "APD (% RNB)",
    "ide_entrees_pct_pib": "IDE (% PIB)",
    "inflation": "Inflation (%)",
    "dette_exterieure_pct_rnb": "Dette ext. (% RNB)",
}


def charger_donnees() -> pd.DataFrame:
    chemin = PROCESSED_DIR / "indicateurs_cedeao.csv"
    if not chemin.exists():
        raise FileNotFoundError(
            "data/processed/indicateurs_cedeao.csv introuvable. "
            "Lance d'abord fetch_data.py puis clean_data.py"
        )
    return pd.read_csv(chemin)


def tendance_regionale(df: pd.DataFrame, indicateur: str) -> pd.Series:
    """Moyenne CEDEAO par année pour un indicateur donné."""
    sous_df = df[df["indicateur"] == indicateur]
    return sous_df.groupby("annee")["valeur"].mean()


def classement_pays(df: pd.DataFrame, indicateur: str, derniere_annee: int) -> pd.Series:
    sous_df = df[(df["indicateur"] == indicateur) & (df["annee"] == derniere_annee)]
    return sous_df.set_index("pays")["valeur"].sort_values(ascending=False)


def graphique_tendance_multi(df: pd.DataFrame):
    indicateurs = ["croissance_pib", "inflation", "aide_publique_dev_pct_rnb"]
    fig, axes = plt.subplots(len(indicateurs), 1, figsize=(10, 12), sharex=True)

    for ax, indicateur in zip(axes, indicateurs):
        tendance = tendance_regionale(df, indicateur)
        ax.plot(tendance.index, tendance.values, marker="o", color="#2E86AB")
        ax.set_title(f"CEDEAO — {NOMS_COURTS[indicateur]} (moyenne régionale)")
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel("Année")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "tendances_regionales.png", dpi=150)
    plt.close(fig)


def graphique_classement(df: pd.DataFrame, indicateur: str, derniere_annee: int, nom_fichier: str):
    classement = classement_pays(df, indicateur, derniere_annee).dropna()

    fig, ax = plt.subplots(figsize=(10, 7))
    couleurs = plt.cm.viridis_r([i / len(classement) for i in range(len(classement))])
    ax.barh(classement.index[::-1], classement.values[::-1], color=couleurs[::-1])
    ax.set_title(f"{NOMS_COURTS[indicateur]} par pays — {derniere_annee}")
    ax.set_xlabel(NOMS_COURTS[indicateur])
    fig.tight_layout()
    fig.savefig(OUT_DIR / nom_fichier, dpi=150)
    plt.close(fig)


def graphique_correlation_aide_croissance(df: pd.DataFrame, derniere_annee: int):
    """Explore la relation entre aide publique au développement et croissance du PIB."""
    aide = df[(df["indicateur"] == "aide_publique_dev_pct_rnb") & (df["annee"] == derniere_annee)]
    croissance = df[(df["indicateur"] == "croissance_pib") & (df["annee"] == derniere_annee)]

    merge = aide.merge(croissance, on="pays", suffixes=("_aide", "_croissance"))

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(merge["valeur_aide"], merge["valeur_croissance"], s=80, color="#E76F51")
    for _, row in merge.iterrows():
        ax.annotate(row["pays"], (row["valeur_aide"], row["valeur_croissance"]),
                    fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax.set_xlabel("Aide publique au développement (% RNB)")
    ax.set_ylabel("Croissance du PIB (%)")
    ax.set_title(f"APD vs croissance du PIB — CEDEAO, {derniere_annee}")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "correlation_aide_croissance.png", dpi=150)
    plt.close(fig)


def generer_rapport(df: pd.DataFrame, derniere_annee: int):
    lignes = [
        "# Rapport comparatif — Indicateurs économiques CEDEAO\n",
        f"*Basé sur les données World Bank, dernière année disponible : {derniere_annee}*\n",
        "## Classements clés\n",
    ]

    for indicateur in ["croissance_pib", "pib_par_habitant", "aide_publique_dev_pct_rnb"]:
        classement = classement_pays(df, indicateur, derniere_annee).dropna()
        lignes.append(f"### {NOMS_COURTS[indicateur]}\n")
        lignes.append(f"- Le plus élevé : **{classement.index[0]}** ({classement.iloc[0]:.1f})")
        lignes.append(f"- Le plus bas : **{classement.index[-1]}** ({classement.iloc[-1]:.1f})")
        lignes.append(f"- Moyenne CEDEAO : **{classement.mean():.1f}**\n")

    with open(OUT_DIR / "rapport_cedeao.md", "w") as f:
        f.write("\n".join(lignes))


def main():
    df = charger_donnees()
    derniere_annee = int(df[df["indicateur"] == "croissance_pib"]["annee"].max())

    graphique_tendance_multi(df)
    graphique_classement(df, "pib_par_habitant", derniere_annee, "classement_pib_habitant.png")
    graphique_classement(df, "aide_publique_dev_pct_rnb", derniere_annee, "classement_aide_developpement.png")
    graphique_correlation_aide_croissance(df, derniere_annee)
    generer_rapport(df, derniere_annee)

    print(f"Analyse terminée pour l'année {derniere_annee}.")
    print(f"Fichiers générés dans {OUT_DIR}/")


if __name__ == "__main__":
    main()
