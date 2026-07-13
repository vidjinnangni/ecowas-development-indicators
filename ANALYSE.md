# Analyse, indicateurs économiques CEDEAO

*Basé sur les données World Bank récupérées via `scripts/fetch_data.py`, période 2000-2023.*

## Contexte

Cette analyse porte sur trois angles :

- les tendances économiques régionales sur 24 ans ;
- la relation entre aide publique au développement (APD) et croissance du PIB ;
- les écarts de richesse entre les 15 pays de la CEDEAO.

L'objectif n'est pas de tirer des conclusions causales définitives à partir d'un jeu de données macro-économiques agrégées, mais de dégager des lectures qui méritent d'être creusées.

## 1. Ce que montrent les tendances régionales

**La croissance du PIB CEDEAO est erratique mais structurellement positive**,
avec une seule véritable rupture sur toute la période : **2020**, seule année
de croissance négative (environ -0,5 %), suivie d'un rebond net en 2021-2022
(autour de 5-6 %). Le choc est net et isolé. Ce n'est pas une tendance de
fond, mais un accident conjoncturel clairement identifiable, cohérent avec le
choc mondial du Covid-19.

**L'inflation raconte une histoire différente.** Pendant 20 ans (2000-2020),
elle oscille dans une fourchette relativement contenue (4-9 %, avec des pics
ponctuels comme 2008 ou 2011). À partir de 2021, elle **change de régime** :
elle grimpe à ~11,7 % en 2022 et ~12,1 % en 2023, sans redescendre. Contrairement
à la croissance du PIB, ce n'est pas un pic isolé mais un plateau qui persiste
sur les deux dernières années disponibles. Ce qui suggère un choc plus
durable (probablement lié aux prix alimentaires et énergétiques mondiaux
post-Covid et post-invasion de l'Ukraine, à confirmer avec des données
sectorielles).

**L'APD suit une tendance de fond à la baisse.** Le pic régional se situe en
2007 (~14,5 % du RNB en moyenne), suivi d'une décrue quasi continue jusqu'à
un plancher autour de 6-7 % dans les années 2020, avec un sursaut ponctuel en
2020-2021 (~9 %) probablement lié aux réponses d'urgence Covid des bailleurs.
Sur le temps long, la région dépend donc proportionnellement moins de l'aide
extérieure qu'il y a 15 ans ; mais cette moyenne cache d'importantes
disparités entre pays (voir section 3).

## 2. Aide publique au développement et croissance

Le nuage de points 2023 ne fait apparaître **aucune relation linéaire nette**
entre le niveau d'APD reçu et la croissance du PIB. Le Nigeria et le Ghana
affichent une croissance correcte (3,1-3,3 %) avec très peu d'aide (moins de
2,1 % du RNB), deux économies plus diversifiées, avec un accès aux marchés
financiers internationaux. À l'autre bout, la Gambie combine le niveau d'aide
le plus élevé du groupe (14,6 % du RNB) et l'une des croissances les plus
fortes (5,9 %), tandis que le Niger, avec un niveau d'aide comparable à celui
du Burkina Faso (~7,6 %), affiche l'une des croissances les plus faibles
(2,6 %).

**Il faut résister à la tentation d'en tirer une conclusion causale.** Ce
graphique compare 15 points sur une seule année. Ce n'est ni un échantillon
suffisant, ni une fenêtre temporelle assez longue pour parler de corrélation
au sens statistique. Ce que ça suggère, sans le démontrer, c'est que l'aide
finance probablement des besoins structurels (santé, éducation, stabilité,
réponse à des crises sécuritaires) plutôt que la croissance de court terme. Ce qui est cohérent avec la nature même de l'APD, mais resterait à vérifier
avec une série longue (voir pistes ci-dessous).

## 3. Écarts de richesse entre pays de la CEDEAO

Le classement du PIB par habitant est dominé par le Cap-Vert (~4 800 US$),
loin devant tous les autres pays de la région (le deuxième, la Côte d'Ivoire,
est à ~2 600 US$). Ce résultat doit être lu avec prudence : Cabo Verde est un
petit État insulaire à faible population, dont l'économie orientée
tourisme/services produit un PIB par habitant élevé sans que cela reflète le
poids économique réel de la région. **C'est l'inverse du biais que l'on
retrouve dans les moyennes régionales agrégées**, où un géant comme le
Nigeria peut être noyé statistiquement malgré son poids économique dominant.

Sans surprise, les pays les plus dépendants de l'APD (Gambie, Liberia,
Guinée-Bissau, Niger, tous au-dessus de 7,5 % du RNB) figurent aussi parmi
les PIB par habitant les plus faibles de la région. Cette lecture croisée,
pays par pays, est plus parlante que la comparaison isolée aide/croissance
de la section précédente : elle montre une association plausible entre
dépendance à l'aide et niveau de richesse structurel, sans pour autant
établir un sens de causalité.

## Limite méthodologique à assumer

**La moyenne régionale simple traite tous les pays à égalité**, alors que le
Nigeria pèse à lui seul plus de 60 % du PIB total de la CEDEAO. Une évolution
molle de l'économie nigériane peut donc être largement diluée dans les
graphiques de tendance régionale (section 1), qui font une moyenne
non-pondérée pays par pays plutôt qu'une moyenne pondérée par le poids
économique réel. Cette limite ne rend pas l'analyse fausse, mais elle invite
à la prudence : les tendances "régionales" de ce rapport reflètent la
dynamique moyenne des 15 pays, pas nécessairement celle de l'économie
CEDEAO dans son ensemble.

## Pistes d'approfondissement

- **Pondérer par le PIB** plutôt que faire une moyenne simple pays par pays,
  pour obtenir une vraie tendance "poids économique régional".
- **Calculer une corrélation sur la série longue** (2000-2023) entre APD et
  croissance, plutôt que sur une seule année, pour voir si une relation
  plus lisible émerge sur le temps long, ou si l'absence de relation de la
  section 2 se confirme.
- **Décomposer l'inflation** par pays plutôt qu'en moyenne régionale, pour
  vérifier si le plateau post-2021 touche uniformément la région ou
  seulement certaines économies plus exposées aux importations alimentaires.
- **Croiser avec un indicateur de dette extérieure** (déjà collecté par
  `fetch_data.py` mais pas encore exploité dans `analyse.py`) pour voir si
  les pays les plus dépendants de l'aide sont aussi les plus endettés.
