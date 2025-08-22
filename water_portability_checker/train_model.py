import pandas as pd

from sklearn.utils import resample
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

## Data Balancing 

# Combine features and target to handle together
df_upsampling = pd.concat([x, y], axis=1)

# Separate majority and minority classes
class_counts = df_upsampling['Potability'].value_counts()

maj_class = class_counts.idxmax()
min_class = class_counts.idxmin()

df_majority = df_upsampling[df_upsampling['Potability'] == maj_class]
df_minority = df_upsampling[df_upsampling['Potability'] == min_class]

# Upsample minority to match majority count
df_minority_upsampled = resample(
    df_minority,
    replace=True,                  # Sample with replacement
    n_samples=len(df_majority),    # Match majority count
    random_state=42
)

# Combine majority and upsampled minority
df_balanced = pd.concat([df_majority, df_minority_upsampled])

# Shuffle the balanced dataset
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

X_bal = df_balanced.iloc[:, :-1]
y_bal = df_balanced['Potability']

# Data Splitting
x_train, x_test, y_train, y_test = train_test_split(X_bal, y_bal, train_size = 0.8, random_state = 42)

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("rf", RandomForestClassifier(random_state=42))
])


pipe.fit(x_train, y_train)
y_pred = pipe.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {acc * 100:.2f}%")

# Save model + metadata (feature order) for safe reuse
bundle: Dict = {
    "model": pipe,
    "features": FEATURES,
    "test_accuracy": acc,
}
joblib.dump(bundle, MODEL_PATH)
print(f"Saved: {MODEL_PATH}")