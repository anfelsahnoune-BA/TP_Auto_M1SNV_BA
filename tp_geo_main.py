# ============================================================
# Universite de Batna 2
# TP M1 SNV - Automatisation & Visualisation GEO
# ============================================================

import GEOparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
geo_id = "GSE11121"
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOG_FILE = os.path.join(BASE_DIR, "logs", "tp_geo_log.txt")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# LOG FUNCTION
# ============================================================
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] {msg}"
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# ============================================================
# ETAPE 1 : TELECHARGEMENT GEO
# ============================================================
log(f"Telechargement du dataset {geo_id} depuis NCBI GEO...")
gse = GEOparse.get_GEO(geo=geo_id, destdir=DATA_DIR)
log("Telechargement termine.")

# ============================================================
# ETAPE 2 : METADONNEES
# ============================================================
title = gse.metadata.get("title", ["Titre non disponible"])[0]
log(f"Titre de l'etude : {title}")
log(f"Nombre d'echantillons : {len(gse.gsms)}")

# ============================================================
# ETAPE 3 : EXTRACTION DES DONNEES
# ============================================================
log("Extraction et fusion des donnees d'expression...")

tables = []
for gsm_name, gsm in gse.gsms.items():
    df = gsm.table.copy()

    # detection colonne ID
    id_col = None
    for candidate in ["ID_REF", "ID", "Gene", "GENE_SYMBOL", "SPOT_ID"]:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col is None or "VALUE" not in df.columns:
        log(f"Echantillon ignore (colonnes manquantes) : {gsm_name}")
        continue

    df = df[[id_col, "VALUE"]].set_index(id_col)
    df.rename(columns={"VALUE": gsm_name}, inplace=True)
    tables.append(df)

if not tables:
    raise ValueError("Aucune table valide trouvee. Verifiez le GEO ID.")

expression_data = pd.concat(tables, axis=1).dropna()
expression_data["mean_expression"] = expression_data.mean(axis=1)
log(f"Fusion reussie : {expression_data.shape[0]} genes et {expression_data.shape[1]-1} echantillons.")

# ============================================================
# Universite de Batna 2
# TP M1 SNV - Automatisation & Visualisation GEO
# ============================================================

import GEOparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
geo_id = "GSE11121"
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOG_FILE = os.path.join(BASE_DIR, "logs", "tp_geo_log.txt")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# LOG FUNCTION
# ============================================================
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] {msg}"
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# ============================================================
# ETAPE 1 : TELECHARGEMENT GEO
# ============================================================
log(f"Telechargement du dataset {geo_id} depuis NCBI GEO...")
gse = GEOparse.get_GEO(geo=geo_id, destdir=DATA_DIR)
log("Telechargement termine.")

# ============================================================
# ETAPE 2 : METADONNEES
# ============================================================
title = gse.metadata.get("title", ["Titre non disponible"])[0]
log(f"Titre de l'etude : {title}")
log(f"Nombre d'echantillons : {len(gse.gsms)}")

# ============================================================
# ETAPE 3 : EXTRACTION DES DONNEES
# ============================================================
log("Extraction et fusion des donnees d'expression...")

tables = []
for gsm_name, gsm in gse.gsms.items():
    df = gsm.table.copy()

    # detection colonne ID
    id_col = None
    for candidate in ["ID_REF", "ID", "Gene", "GENE_SYMBOL", "SPOT_ID"]:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col is None or "VALUE" not in df.columns:
        log(f"Echantillon ignore (colonnes manquantes) : {gsm_name}")
        continue

    df = df[[id_col, "VALUE"]].set_index(id_col)
    df.rename(columns={"VALUE": gsm_name}, inplace=True)
    tables.append(df)

if not tables:
    raise ValueError("Aucune table valide trouvee. Verifiez le GEO ID.")

expression_data = pd.concat(tables, axis=1).dropna()
expression_data["mean_expression"] = expression_data.mean(axis=1)
log(f"Fusion reussie : {expression_data.shape[0]} genes et {expression_data.shape[1]-1} echantillons.")

# ============================================================
# ETAPE 4 : STATISTIQUES
# ============================================================
log("Calcul des statistiques descriptives...")
stats = expression_data["mean_expression"].describe()
stats.to_csv(os.path.join(RESULTS_DIR, "summary_stats.txt"), sep="\t")
log("Statistiques enregistrees dans results/summary_stats.txt")

# ============================================================
# ETAPE 5 : HISTOGRAMME
# ============================================================
plt.figure(figsize=(10, 5))
sns.histplot(expression_data["mean_expression"], bins=50, kde=True)
plt.title("Distribution des niveaux moyens d'expression genique")
plt.xlabel("Expression moyenne")
plt.ylabel("Frequence")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hist_expression.png"))
plt.close()
log("Histogramme sauvegarde dans results/hist_expression.png")

# ============================================================
# ETAPE 6 : HEATMAP + CLUSTERING
# ============================================================
log("Generation de la heatmap avec clustering...")

subset = expression_data.drop(columns=["mean_expression"]).sample(
    n=min(50, len(expression_data)), random_state=42
)

sns.clustermap(
    subset,
    cmap="coolwarm",
    metric="euclidean",
    method="average",
    figsize=(10, 10)
)

plt.savefig(os.path.join(RESULTS_DIR, "heatmap_clustering.png"))
plt.close()
log("Heatmap sauvegardee dans results/heatmap_clustering.png")

# ============================================================
# ETAPE 7 : EXPORTATION
# ============================================================
expression_data.to_csv(os.path.join(RESULTS_DIR, "expression_cleaned.csv"))
log("Donnees exportees dans results/expression_cleaned.csv")

log("TP execute avec succes ! Consultez le dossier results/.")

