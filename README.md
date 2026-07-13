🇫🇷 Français | [🇬🇧 English](README.en.md)

# Indicateurs économiques CEDEAO

Pipeline de récupération et d'analyse d'indicateurs économiques et d'aide au
développement pour les 15 pays de la CEDEAO, via l'[API World Bank](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589).

## Structure

```
ecowas-development-indicators/
├── data/
│   ├── raw/          # JSON brut de l'API (1 fichier par indicateur, généré par fetch_data.py)
│   └── processed/     # CSV tidy final (généré par clean_data.py)
├── scripts/
│   ├── fetch_data.py  # appelle l'API World Bank, gère la pagination, met en cache
│   ├── clean_data.py  # JSON -> CSV tidy (pays x indicateur x année)
│   └── analyse.py     # comparaisons régionales, classements, corrélations, graphiques
├── notebook/
│   └── exploration.ipynb
└── outputs/            # graphiques + rapport générés
```

## Pays couverts

Bénin, Burkina Faso, Cabo Verde, Côte d'Ivoire, Gambie, Ghana, Guinée,
Guinée-Bissau, Liberia, Mali, Niger, Nigeria, Sénégal, Sierra Leone, Togo.

## Indicateurs

| Code World Bank | Indicateur |
|---|---|
| `NY.GDP.MKTP.KD.ZG` | Croissance du PIB (% annuel) |
| `NY.GDP.PCAP.CD` | PIB par habitant (US$ courants) |
| `DT.ODA.ODAT.GN.ZS` | Aide publique au développement reçue (% du RNB) |
| `BX.KLT.DINV.WD.GD.ZS` | Investissements directs étrangers, entrées nettes (% du PIB) |
| `FP.CPI.TOTL.ZG` | Inflation, prix à la consommation (% annuel) |
| `DT.DOD.DECT.GN.ZS` | Dette extérieure (% du RNB) |

Période : 2000-2023. D'autres indicateurs peuvent être ajoutés en modifiant
le dictionnaire `INDICATEURS` dans `fetch_data.py`. La liste complète des
codes peut être recherchée ici : https://api.worldbank.org/v2/indicator?format=json&per_page=100&search=<mot-clé>

## Utilisation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python scripts/fetch_data.py    # télécharge les données brutes (nécessite internet, pas de clé API)
python scripts/clean_data.py    # génère data/processed/indicateurs_cedeao.csv
python scripts/analyse.py       # génère les graphiques et le rapport dans outputs/
```

Ou explorer pas à pas dans `notebook/exploration.ipynb`.

## Aperçu des résultats
 
**Croissance, inflation et aide au développement : moyenne régionale 2000-2023**
 
![Tendances régionales CEDEAO](outputs/tendances_regionales.png)
 
L'inflation régionale change nettement de régime après 2020-2021, tandis que
l'aide publique au développement suit une tendance de fond à la baisse
depuis son pic de 2007. Voir [ANALYSE.md](ANALYSE.md) pour la lecture
détaillée.
 
**Aide publique au développement vs croissance du PIB (2023)**
 
![APD vs croissance](outputs/correlation_aide_croissance.png)
 
Aucune relation linéaire nette n'apparaît entre les deux — une lecture à
nuancer plutôt qu'une conclusion, détaillée dans l'analyse.
 
**[Lire l'analyse complète →](ANALYSE.md)** 

## Note sur l'API

L'API World Bank est publique et gratuite, mais certaines combinaisons
pays/indicateur/année peuvent être manquantes selon les pays (couverture des
données inégale, en particulier avant les années 2000 ou pour les plus
petits pays). Le script `clean_data.py` ignore les valeurs manquantes plutôt
que de les deviner.

## Pistes d'évolution

- Ajouter d'autres blocs thématiques (éducation, santé, numérique) pour
  croiser avec les indicateurs économiques.
- Construire un dashboard interactif (Streamlit).
- Automatiser une mise à jour périodique des données.
- Comparer la CEDEAO à d'autres blocs régionaux (CEMAC, SADC...).

---

*Projet réalisé dans le cadre de mon apprentissage de Python/Pandas, en lien
avec mon expérience professionnelle en gestion de programmes de développement
et coordination de partenariats avec des bailleurs.*

---

## Licence

Le code de ce projet est sous licence [MIT](LICENSE). Les données proviennent
de la Banque mondiale ([World Bank Open Data](https://data.worldbank.org)),
sous licence [CC-BY 4.0](https://datacatalog.worldbank.org/public-licenses#cc-by).
