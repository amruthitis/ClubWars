import joblib
import numpy as np

model = joblib.load("ml/reliability_model.pkl")

def predict_reliability():
    X = np.array([[0, 0, 2]])
    return float(model.predict_proba(X)[0][1])
