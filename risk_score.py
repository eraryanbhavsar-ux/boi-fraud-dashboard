import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset

df = pd.read_csv("data/DataSet (1).csv")

df = df.drop("Unnamed: 0", axis=1)

# Target

y = df["F3924"]

# Features

X = df.drop("F3924", axis=1)

# Columns

numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns
categorical_cols = X.select_dtypes(include=["object", "string"]).columns

# Preprocessing

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value=0))
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ]
)

# Model

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

clf = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train

clf.fit(X_train, y_train)

# Risk Scores

risk_scores = clf.predict_proba(X_test)[:, 1] * 100

results = pd.DataFrame({
    "Actual": y_test.values,
    "Risk Score": risk_scores
})

print("\nTop 10 Risky Accounts\n")
print(results.sort_values("Risk Score", ascending=False).head(10))

results.to_csv("risk_scores.csv", index=False)

print("\nSaved risk_scores.csv")