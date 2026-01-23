import pandas as pd
import numpy as np


class FeatureEngineer:
    def __init__(self):
        self.known_types = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main preprocessing function. It creates modifies original fraud_dataset so model can be trained.
        Using
        """

        df = df.copy()
        df['errorBalanceOrig'] = df['newbalanceOrig'] + df['amount'] - df['oldbalanceOrg']
        df['errorBalanceDest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']


        if 'type' in df.columns:
            dummies = pd.get_dummies(df['type'], prefix='type')
            df = pd.concat([df, dummies], axis=1)

            for t in self.known_types:
                col_name = f'type_{t}'
                if col_name not in df.columns:
                    df[col_name] = 0

        cols_to_drop = ['nameOrig', 'nameDest', 'isFlaggedFraud', 'type']

        existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
        df = df.drop(columns=existing_cols_to_drop)

        return df