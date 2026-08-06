import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

print("Loading dataset...")

# Load dataset
df = pd.read_csv("data/DataSet (1).csv")
# Remove index column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

print("Dataset Shape:", df.shape)

# -----------------------------
# DATA CLEANING
# -----------------------------

# Convert everything to numeric
df = df.apply(pd.to_numeric, errors="coerce")

# Fill missing values
df = df.fillna(df.median())
# Extra cleanup for PCA

df = df.replace([float("inf"), float("-inf")], 0)

df = df.fillna(0)

print("Missing values handled")

# -----------------------------
# FEATURE SCALING
# -----------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(df)
import numpy as np

X_scaled = np.nan_to_num(
    X_scaled,
    nan=0.0,
    posinf=0.0,
    neginf=0.0
)
print("NaN count after cleanup:", np.isnan(X_scaled).sum())
print("Feature scaling completed")

print("Feature scaling completed")

# -----------------------------
# ANOMALY DETECTION MODEL
# -----------------------------

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

print("Checking PCA input...")
print("NaN values:", np.isnan(X_scaled).sum())
print("Infinite values:", np.isinf(X_scaled).sum())

print("Running PCA...")

pca = PCA(
    n_components=50,
    random_state=42
)
X_pca = pca.fit_transform(X_scaled)

print("PCA completed")

print("Training Isolation Forest...")

model = IsolationForest(
    n_estimators=500,
    contamination=0.02,
    random_state=42,
    n_jobs=-1
)

model.fit(X_pca)

scores = model.decision_function(X_pca)

print("Running Fraud Clustering...")

kmeans = KMeans(
    n_clusters=8,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X_pca)

risk_scores = (
    (scores.max() - scores)
    /
    (scores.max() - scores.min())
) * 100

risk_df = pd.DataFrame({
    "Account ID": range(len(df)),
    "Risk Score": risk_scores.round(2),
    "Cluster": clusters
})

# -----------------------------
# RISK LEVELS
# -----------------------------

risk_df["Risk Level"] = np.where(
    risk_df["Risk Score"] >= 70,
    "High",
    np.where(
        risk_df["Risk Score"] >= 40,
        "Medium",
        "Low"
    )
)

# -----------------------------
# SAVE OUTPUT
# -----------------------------

risk_df.to_csv(
    "risk_scores.csv",
    index=False
)

print("\nRisk scores generated successfully")
print("\nTop 20 risky accounts:\n")

print(
    risk_df.sort_values(
        "Risk Score",
        ascending=False
    ).head(20)
)

print("\nSaved file: risk_scores.csv")