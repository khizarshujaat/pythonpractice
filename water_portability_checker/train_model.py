import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
from typing import List, Dict

# --- Expected feature order (lowercase) ---
FEATURES: List[str] = [
    "ph",
    "hardness",
    "solids",
    "chloramines",
    "sulfate",
    "conductivity",
    "organic_carbon",
    "trihalomethanes",
    "turbidity",
]

CSV_PATH = "water_potability.csv"
MODEL_PATH = "water_potability_rf.pkl"

df_water = pd.read_csv(CSV_PATH)

df_clean = df_water.fillna(df_water.mean())

# x are features
x = df_clean[list(df_clean.columns)[0: -1]]

# y = output
y = df_clean['Potability']

#Data Splitting
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, random_state = 42)


pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("rf", RandomForestClassifier(random_state=42))
])


pipe.fit(x_train, y_train)
y_pred = pipe.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {acc:.4f}")

# Save model + metadata (feature order) for safe reuse
bundle: Dict = {
    "model": pipe,
    "features": FEATURES,
    "test_accuracy": acc,
}
joblib.dump(bundle, MODEL_PATH)
print(f"Saved: {MODEL_PATH}")