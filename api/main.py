from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import sys
import os
from pathlib import Path
from api.schema import Transaction
from src.rules import FraudRulesEngine

rules_engine = FraudRulesEngine()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features import FeatureEngineer

app = FastAPI(title="Fraud Detection API", version="1.0")

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "production_model.pkl"

print(f"Loading model from: {MODEL_PATH}")
try:
    model = joblib.load(MODEL_PATH)
    print("Model successfully loaded.")
except Exception as e:
    print(f"Error occured during model loading: {e}")
    model = None

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}


@app.post("/predict")
def predict_fraud(txn: Transaction):

    txn_dict = txn.dict()
    print(f"🔍 DEBUG: Amount={txn_dict.get('amount')} | OldBalance={txn_dict.get('oldbalanceOrg')}")
    print(f"🔍 KEYS: {txn_dict.keys()}")
    rule_verdict = rules_engine.check_hard_rules(txn_dict)

    if rule_verdict:
        return rule_verdict

    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    data = {k: [v] for k, v in txn.dict().items()}
    df = pd.DataFrame(data)

    fe = FeatureEngineer()
    try:
        df_processed = fe.preprocess(df)
        if hasattr(model, "feature_names_in_"):
            expected_cols = model.feature_names_in_
        else:
            expected_cols = model.get_booster().feature_names

        cols_to_remove = [col for col in df_processed.columns if col not in expected_cols]
        if cols_to_remove:
            df_processed = df_processed.drop(columns=cols_to_remove)

        for col in expected_cols:
            if col not in df_processed.columns:
                df_processed[col] = 0

        df_processed = df_processed[expected_cols]

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Processing error: {str(e)}")

    try:
        prediction = model.predict(df_processed)[0]
        probability = model.predict_proba(df_processed)[0][1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    result = "FRAUD" if prediction == 1 else "LEGIT"

    return {
        "prediction": result,
        "fraud_probability": float(probability),
        "details": "Reviewed by XGBoost"
    }