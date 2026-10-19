"""Leakage-safe candidates, including a strong historical municipal reference."""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.preprocessing.dataset import NUMERIC, CATEGORICAL


class HistoricalRateBaseline(ClassifierMixin, BaseEstimator):
    """Risk = 1 - past municipality literacy rate; fallback fitted on training only."""
    def fit(self, X, y):
        self.default_ = float(np.mean(y))
        self.classes_ = np.array([0, 1])
        self.n_features_in_ = X.shape[1]
        return self

    def predict_proba(self, X):
        risk = 1 - X['taxa_municipal_anterior'].astype(float).to_numpy() / 100
        risk = np.clip(np.where(np.isfinite(risk), risk, self.default_), 0, 1)
        return np.column_stack([1-risk, risk])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


def preprocessing():
    numerical = Pipeline([
        ('imputer', SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True)),
        ('scale', StandardScaler()),
    ])
    categorical = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent', keep_empty_features=True)),
        ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    return ColumnTransformer([('numeric', numerical, NUMERIC),
                              ('categorical', categorical, CATEGORICAL)], remainder='drop')


def candidates(seed=42):
    return {
        'dummy': (DummyClassifier(strategy='prior'), None),
        'historical_rate': (HistoricalRateBaseline(), None),
        'logistic': (Pipeline([('prepare', preprocessing()),
                              ('model', LogisticRegression(max_iter=1500, random_state=seed))]),
                     {'model__C': [0.01, 0.1, 1.0, 10.0]}),
        'random_forest': (Pipeline([('prepare', preprocessing()),
                                   ('model', RandomForestClassifier(n_estimators=150,
                                        n_jobs=1, random_state=seed))]),
                          {'model__max_depth': [5, 10, None],
                           'model__min_samples_leaf': [30, 100, 300],
                           'model__max_features': ['sqrt', 1.0]}),
    }
