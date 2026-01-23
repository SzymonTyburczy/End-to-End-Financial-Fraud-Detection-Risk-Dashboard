import xgboost as xgb
import optuna
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, f1_score
import os


class FraudTrainer:
    def __init__(self):
        """
        Initialization is now simple. We're not passing data here, we're just preparing space for the model.
        """
        self.model = None

    def train(self, X_train, y_train, X_test, y_test, params=None):
        """
        Main training method. Accepts ALREADY SPLIT data.
        """

        print(f" Starting training with the XGBoost model...")
        print(f"   Train shape: {X_train.shape}, Test shape: {X_test.shape}")

        ratio = float(y_train.value_counts()[0]) / y_train.value_counts()[1]

        default_params = {
            'n_estimators': 200,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'scale_pos_weight': ratio,
            'eval_metric': 'logloss',
            'n_jobs': -1
        }

        if params:
            default_params.update(params)

        self.model = xgb.XGBClassifier(**default_params)

        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)
        f1 = f1_score(y_test, preds)
        print(f" Training completed. F1 Score on the test set: {f1:.4f}")

        return self.model

    def optimize_hyperparameters(self, X_train, y_train, X_test, y_test, n_trials=10):
        """
            Optional: Using Optuna to find the best parameters.
        """

        def objective(trial):
            param = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 500),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
                'scale_pos_weight': trial.suggest_float('scale_pos_weight', 1, 100),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
                'n_jobs': -1
            }

            clf = xgb.XGBClassifier(**param)
            clf.fit(X_train, y_train)
            preds = clf.predict(X_test)
            return f1_score(y_test, preds)

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)

        print(f" Best parameters found: {study.best_params}")
        return study.best_params

    def save_model(self, path="models/final_model.pkl"):
        if self.model:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(self.model, path)
            print(f" Model saved in: {path}")
        else:
            print("No trained model found to save")