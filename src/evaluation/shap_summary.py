"""Aggregate transformed SHAP effects back to the original feature names."""
import numpy as np
import pandas as pd


def grouped_shap(transformed_names, values, original_features):
    values = np.asarray(values)
    if values.ndim != 2 or values.shape[1] != len(transformed_names):
        raise ValueError('Dimensões inesperadas nos valores SHAP.')
    grouped = np.zeros((len(values),len(original_features)))
    for j,name in enumerate(transformed_names):
        matches = [f for f in original_features if name in ('numeric__'+f,'numeric__missingindicator_'+f)
                   or name.startswith('categorical__'+f+'_')]
        if len(matches)!=1:
            raise ValueError('Não foi possível atribuir a transformação a uma variável: '+name)
        grouped[:,original_features.index(matches[0])] += values[:,j]
    np.testing.assert_allclose(grouped.sum(axis=1),values.sum(axis=1),atol=1e-10)
    summary = pd.DataFrame({'feature':original_features,
        'mean_abs_shap_log_odds':np.abs(grouped).mean(axis=0),
        'mean_signed_shap_log_odds':grouped.mean(axis=0)})
    return summary.sort_values('mean_abs_shap_log_odds',ascending=False)
