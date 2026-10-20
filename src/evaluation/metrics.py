"""Evaluation with an explicit positive class and grouped uncertainty."""
import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix,
    f1_score, fbeta_score, precision_score, recall_score, roc_auc_score)


def choose_threshold(y_validation, probabilities):
    thresholds = np.linspace(0.01, 0.99, 99)
    scores = [fbeta_score(y_validation, probabilities >= t, beta=2, zero_division=0)
              for t in thresholds]
    # A tie prioritizes the higher threshold, limiting unnecessary alerts.
    return float(thresholds[np.flatnonzero(np.isclose(scores, max(scores)))[-1]])


def evaluate(y, probabilities, threshold):
    y = np.asarray(y)
    if np.unique(y).size != 2:
        raise ValueError('Avaliação requer duas classes.')
    predicted = probabilities >= threshold
    return {
        'rows': len(y), 'risk_prevalence': float(y.mean()), 'threshold': float(threshold),
        'average_precision': float(average_precision_score(y, probabilities)),
        'roc_auc': float(roc_auc_score(y, probabilities)),
        'brier': float(brier_score_loss(y, probabilities)),
        'precision': float(precision_score(y, predicted, zero_division=0)),
        'recall': float(recall_score(y, predicted, zero_division=0)),
        'f1': float(f1_score(y, predicted, zero_division=0)),
        'f2': float(fbeta_score(y, predicted, beta=2, zero_division=0)),
        'alert_rate': float(predicted.mean()),
        'confusion_matrix': confusion_matrix(y, predicted, labels=[0, 1]).tolist(),
    }


def grouped_bootstrap(y, probabilities, municipalities, seed=42, repetitions=100):
    groups, indices = np.unique(np.asarray(municipalities), return_inverse=True)
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    ap, auc = [], []
    for _ in range(repetitions):
        multiplicities = np.bincount(rng.integers(0, len(groups), size=len(groups)), minlength=len(groups))
        weights = multiplicities[indices]
        if np.unique(y[weights > 0]).size != 2:
            continue
        ap.append(average_precision_score(y, probabilities, sample_weight=weights))
        auc.append(roc_auc_score(y, probabilities, sample_weight=weights))
    if not ap:
        raise ValueError('Bootstrap não gerou amostras com duas classes.')
    return {'unit': 'municipality', 'repetitions': len(ap),
            'average_precision_95': np.quantile(ap, [0.025, 0.975]).tolist(),
            'roc_auc_95': np.quantile(auc, [0.025, 0.975]).tolist()}


def subgroup_metrics(frame, probabilities, threshold):
    data = frame.assign(probability=probabilities)
    records = []
    for uf, part in data.groupby('sigla_uf', dropna=False):
        if len(part) >= 100 and part.risco.nunique() == 2:
            records.append({'sigla_uf': uf, **evaluate(part.risco, part.probability.to_numpy(), threshold)})
    return pd.DataFrame(records).drop(columns=['confusion_matrix'], errors='ignore')
