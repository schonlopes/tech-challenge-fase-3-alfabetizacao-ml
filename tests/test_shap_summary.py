import numpy as np
import pytest
from src.evaluation.shap_summary import grouped_shap


def test_shap_grouping_preserves_signed_sum_before_absolute_aggregation():
    values = np.array([[0.1,0.2,0.3,-0.1],[0.2,0.1,-0.3,0.1]])
    names = ['numeric__income','numeric__missingindicator_income',
             'categorical__network_A','categorical__network_B']
    summary = grouped_shap(names,values,['income','network']).set_index('feature')
    assert summary.loc['income','mean_abs_shap_log_odds']==pytest.approx(0.3)
    assert summary.loc['network','mean_abs_shap_log_odds']==pytest.approx(0.2)


def test_shap_grouping_rejects_unassigned_effects():
    with pytest.raises(ValueError,match='atribuir'):
        grouped_shap(['unexpected'],np.array([[1.]]),['income'])
