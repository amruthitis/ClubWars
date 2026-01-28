import pandas as pd

# =========================
# 1. LOAD DATASET
# =========================
df = pd.read_csv(r"H:\Logistics\ml\data\cargo2000.csv")

print("Dataset shape:", df.shape)
print("\nSample rows:")
print(df.head(3))

# =========================
# 2. DELAY FEATURES
# =========================
# Delay = actual - planned

df["i1_dep_delay"] = df["i1_dep_1_e"] - df["i1_dep_1_p"]
df["i1_rcf_delay"] = df["i1_rcf_1_e"] - df["i1_rcf_1_p"]

# Fill missing delays with 0 (means leg didn't exist)
df["i1_dep_delay"] = df["i1_dep_delay"].fillna(0)
df["i1_rcf_delay"] = df["i1_rcf_delay"].fillna(0)

print("\nIncoming leg 1 delays:")
print(df[["i1_dep_delay", "i1_rcf_delay"]].head())

# =========================
# 3. FIX HOPS DATA TYPES
# =========================
# CSV may store hops as strings → convert to numbers

for col in ["i1_hops", "i2_hops", "i3_hops", "o_hops"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =========================
# 4. ROUTE COMPLEXITY FEATURE
# =========================
df["total_hops"] = (
    df["i1_hops"]
    + df["i2_hops"]
    + df["i3_hops"]
    + df["o_hops"]
)

print("\nTotal hops preview:")
print(df["total_hops"].head())

# =========================
# 5. FEATURE MATRIX (X)
# =========================
features = [
    "i1_dep_delay",
    "i1_rcf_delay",
    "total_hops"
]

X = df[features]

print("\nFeature preview (X):")
print(X.head())

# =========================
# 6. TARGET VARIABLE (y)
# =========================
# Final delivery delay decides success

df["final_delay"] = df["o_dlv_e"] - df["o_dlv_p"]
df["on_time"] = (df["final_delay"] <= 0).astype(int)

y = df["on_time"]

print("\nTarget distribution:")
print(y.value_counts())

print("\nML data ready ✅")

# =========================
# 7. TRAIN / TEST SPLIT
# =========================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

# =========================
# 8. MODEL CREATION & TRAINING
# =========================
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    eval_metric="logloss",
    random_state=42
)

model.fit(X_train, y_train)

print("Model trained ✅")

# =========================
# 9. EVALUATION
# =========================
from sklearn.metrics import accuracy_score, roc_auc_score

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# =========================
# 10. SAVE MODEL
# =========================
import joblib

joblib.dump(model, "reliability_model.pkl")
print("Reliability model saved ✅")

print("\nSample reliability scores (probability of on-time):")
print(y_prob[:5])

"""
MODEL ROLE:
------------
This XGBoost model predicts the probability of on-time delivery
based on early-route delay behavior and route complexity.

The output probability is used as a RELIABILITY SCORE
to rank feasible container options after rule-based filtering.
"""

