"""Permutation effects use the identical sample for baseline and shuffled scores."""
import pandas as pd
from sklearn.inspection import permutation_importance


def validation_importance(estimator, X, y, seed=42):
    selected = X.sample(n=min(5000, len(X)), random_state=seed)
    result = permutation_importance(estimator, selected, y.loc[selected.index],
        scoring='average_precision', n_repeats=5, random_state=seed, n_jobs=1,
        max_samples=1.0)
    return pd.DataFrame({'feature':list(X.columns), 'importance':result.importances_mean,
                         'std':result.importances_std})
