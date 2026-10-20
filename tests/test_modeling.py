import numpy as np
import pandas as pd
from src.evaluation.metrics import choose_threshold, evaluate
from src.modeling.pipelines import candidates
from src.preprocessing.dataset import FEATURES
from src.evaluation.interpretation import validation_importance
from scripts.analyze_validation import capacity_options


def test_pipeline_imputes_and_accepts_unseen_categories_without_using_target():
    train = pd.DataFrame({
        'taxa_municipal_anterior':[40.,60.,np.nan,70.,40.,90.],
        'log_populacao_anterior':[3.,4.,5.,np.nan,4.,6.],
        'rede':['Municipal']*6, 'serie':['2']*6,
        'sigla_uf':['SP','SP','RJ','RJ','SP','RJ'], 'regiao':['Sudeste']*6,
        'proficiencia':[500.,850.,600.,900.,450.,950.]})
    estimator = candidates()['logistic'][0]
    estimator.fit(train, [1,0,1,0,1,0])
    imputer = estimator.named_steps['prepare'].named_transformers_['numeric'].named_steps['imputer']
    learned = imputer.statistics_.copy()
    future = train.iloc[:2].copy()
    future['sigla_uf'] = 'UF_NOVA'
    future['proficiencia'] = -999999.
    p = estimator.predict_proba(future)
    assert np.isfinite(p).all()
    np.testing.assert_array_equal(imputer.statistics_, learned)
    np.testing.assert_allclose(p, estimator.predict_proba(future[FEATURES]))


def test_threshold_comes_from_validation_and_metrics_keep_positive_class():
    y = np.array([0,0,1,1]); p = np.array([0.1,0.2,0.6,0.9])
    threshold = choose_threshold(y, p)
    result = evaluate(y, p, threshold)
    assert result['recall'] == 1
    assert result['confusion_matrix'] == [[2,0],[0,2]]


def test_historical_baseline_uses_train_only_fallback():
    baseline = candidates()['historical_rate'][0]
    baseline.fit(pd.DataFrame({'taxa_municipal_anterior':[70.,np.nan]}), [1,0])
    p = baseline.predict_proba(pd.DataFrame({'taxa_municipal_anterior':[80.,np.nan]}))[:,1]
    np.testing.assert_allclose(p, [0.2,0.5])


def test_permutation_constant_feature_is_exactly_zero():
    train = pd.DataFrame({'taxa_municipal_anterior':[20.,40.,60.,80.,90.,30.],
        'log_populacao_anterior':[3.,4.,5.,4.,3.,6.],
        'rede':['Municipal']*6, 'serie':['2']*6, 'sigla_uf':['SP']*6, 'regiao':['Sudeste']*6})
    y = pd.Series([1,1,0,0,0,1])
    model = candidates()['logistic'][0].fit(train, y)
    effects = validation_importance(model, train, y).set_index('feature')
    assert effects.loc['serie','importance'] == 0
    assert effects.loc['serie','std'] == 0


def test_capacity_respects_tied_scores_and_budget():
    y = np.tile([0,1], 10)
    probability = np.repeat([0.1,0.3,0.6,0.9], 5)
    options = capacity_options(y, probability)
    assert (options.alert_rate <= options.maximum_alert_fraction).all()
    assert options.iloc[0].alert_rate == 0  # Top tied group exceeds a 10% budget.
