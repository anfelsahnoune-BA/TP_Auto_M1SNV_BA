TP Automatisation & Visualisation de Données — GEOparse (NCBI GEO)

Université de Batna 2 — Faculté des Sciences
Master 1 SNV – Biochimie Appliquée

Ce projet présente un TP complet d’automatisation, de téléchargement et de visualisation de données d’expression génique issues de la base publique NCBI GEO, en utilisant uniquement des outils Open Source.

🎯 Objectifs du TP

Automatiser le téléchargement d’un dataset GEO (GSE11121)

Extraire et nettoyer les données d’expression

Calculer des statistiques descriptives

Générer des visualisations :

Histogramme

Heatmap + clustering

Organiser un projet Python reproductible

🛠 Technologies utilisées
Outil	Rôle
Python 3	Programmation principale
GEOparse	Extraction des données GEO
Pandas	Manipulation des données
Matplotlib / Seaborn	Visualisation
Git & GitHub	Gestion de version
Git Bash	Terminal Unix sous Windows
📁 Structure du projet
TP_Auto_M1SNV_BA/
│── tp_geo_main.py        # Script principal du TP
│── .gitignore            # Empêche l’upload des gros dossiers
│── data/                 # Données GEO téléchargées (IGNORÉ)
│── results/              # Graphiques & résultats (IGNORÉ)
│── logs/                 # Journal d’exécution (IGNORÉ)


⚠️ Les dossiers data/, results/ et logs/ sont ignorés volontairement car trop volumineux pour GitHub.

▶️ Exécution du TP

Dans Git Bash :

cd TP_Auto_M1SNV_BA
python tp_geo_main.py


Les résultats sont générés dans :

results/hist_expression.png

results/heatmap_clustering.png

results/expression_cleaned.csv

📊 Visualisations générées

Histogramme de la distribution des valeurs d’expression génique

Heatmap + clustering hiérarchique sur 50 gènes échantillonnés

👩‍🏫 Encadrement

Travail réalisé dans le cadre du TP :
Logiciels Libres et Open Source – Biochimie Appliquée

Université Batna 2
Master 1 SNV – Biochimie Appliquée
