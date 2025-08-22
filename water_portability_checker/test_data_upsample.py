import pandas as pd
from sklearn.utils import resample
from sklearn.model_selection import train_test_split

CSV_PATH = "water_potability.csv"

# Load and clean
df_water = pd.read_csv(CSV_PATH)
df_clean = df_water.fillna(df_water.mean())

X = df_clean.iloc[:, :-1]
y = df_clean['Potability']

# Combine features and target to handle together
df = pd.concat([X, y], axis=1)

# Separate majority and minority classes
class_counts = df['Potability'].value_counts()
print(f"Before: {class_counts}")
maj_class = class_counts.idxmax()
min_class = class_counts.idxmin()

df_majority = df[df['Potability'] == maj_class]
df_minority = df[df['Potability'] == min_class]

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

print(f"After: {df_balanced['Potability'].value_counts()}")

# Now split into X and y
X_bal = df_balanced.iloc[:, :-1]
y_bal = df_balanced['Potability']

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(
    X_bal, y_bal, train_size=0.8, random_state=42, stratify=y_bal
)

print("Balanced class counts:", y_bal.value_counts().to_dict())
print("Train class counts:", y_train.value_counts().to_dict())
print("Test class counts:", y_test.value_counts().to_dict())
