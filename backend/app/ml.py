import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


MODEL_PATH = os.path.join(BASE_DIR, "..", "ml", "reliability_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_reliability():
    X = np.array([[0, 0, 2]])
    return float(model.predict_proba(X)[0][1])
