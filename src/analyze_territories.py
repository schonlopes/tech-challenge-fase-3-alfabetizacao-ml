"""Municipal profiles and explicit scenarios from public aggregates, not individual predictions."""
import json
from pathlib import Path
from itertools import combinations
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler
from src.preprocessing.enrichment import SOCIAL, numeric_social, read_territorial
from src.evaluation.territorial import scenarios, persistence_backtest
from src.visualization.figures import plt, save

ROOT = Path(__file__).resolve().parents[1]
CLUSTER_FEATURES = SOCIAL + ['log_populacao_2022','fracao_va_administracao','fracao_va_industria']


def main():
    reports, images = ROOT/'reports/territorial', ROOT/'images/territorial'
    reports.mkdir(parents=True,exist_ok=True); images.mkdir(parents=True,exist_ok=True)
    social = numeric_social(read_territorial(ROOT,'socioeconomic'))
    gold = read_territorial(ROOT,'municipal_gold')
    goals = read_territorial(ROOT,'national_state_targets')
    current = scenarios(gold)
    current.to_csv(reports/'municipal_scenarios.csv',index=False)
    (reports/'persistence_backtest.json').write_text(json.dumps(persistence_backtest(current),indent=2),encoding='utf-8')
    key = ['abrangencia','ano_resultado','sigla_uf','rede']
    if goals.duplicated(key).any():
        raise ValueError('Resultados nacionais/estaduais duplicados.')
    for name in ['ano_resultado','resultado','meta_2024','meta_2025','meta_2030']:
        goals[name] = pd.to_numeric(goals[name],errors='raise')
    goals['gap_2024_pp'] = (goals.resultado-goals.meta_2024).where(goals.ano_resultado.eq(2024))
    goals.to_csv(reports/'national_state_results.csv',index=False)
    public_state = goals[goals.abrangencia.eq('UF') & goals.ano_resultado.eq(2024) & goals.rede.eq('5')]
    public_state.sort_values('gap_2024_pp').to_csv(reports/'state_2024_public.csv',index=False)
    current.sort_values('gap_meta_2024_pp').head(30).to_csv(reports/'largest_observed_gaps_2024.csv',index=False)

    # One row/municipality, no literacy outcome or target included in clustering.
    eligible = social[social[CLUSTER_FEATURES].notna().mean(axis=1).ge(0.7)].copy()
    excluded = social[~social.id_municipio.isin(eligible.id_municipio)]
    excluded[['id_municipio','nome_municipio','sigla_uf']].to_csv(reports/'profile_exclusions.csv',index=False)
    imputer = SimpleImputer(strategy='median',keep_empty_features=True)
    scaler = StandardScaler()
    X = scaler.fit_transform(imputer.fit_transform(eligible[CLUSTER_FEATURES]))
    choices, fitted = [], {}
    for k in range(2,min(7,len(eligible))):
        model = KMeans(n_clusters=k,n_init=20,random_state=42).fit(X)
        score = float(silhouette_score(X,model.labels_,sample_size=min(2500,len(X)),random_state=42))
        choices.append({'k':k,'silhouette':score,'inertia':float(model.inertia_)})
        fitted[k] = model
    selection = pd.DataFrame(choices).sort_values(['silhouette','k'],ascending=[False,True])
    selection.to_csv(reports/'cluster_selection.csv',index=False)
    selected = int(selection.iloc[0].k)
    model = fitted[selected]
    raw = model.labels_
    ordering = eligible.assign(raw=raw).groupby('raw').proporcao_vulneravel.median().sort_values().index
    mapping = {int(old):i+1 for i,old in enumerate(ordering)}
    eligible['cluster'] = [mapping[int(value)] for value in raw]
    repeats = [KMeans(n_clusters=selected,n_init=20,random_state=seed).fit_predict(X) for seed in [7,21]]
    stability = [float(adjusted_rand_score(a,b)) for a,b in combinations([raw]+repeats,2)]
    projection = PCA(n_components=2,random_state=42).fit(X)
    points = projection.transform(X)
    eligible['pca_1'],eligible['pca_2'] = points[:,0],points[:,1]
    contextual = eligible.merge(current[['id_municipio','resultado_2024','gap_meta_2024_pp',
        'ganho_anual_necessario_2030_pp','abaixo_meta_persistencia_2030']],on='id_municipio',how='left',validate='one_to_one')
    contextual.to_csv(reports/'municipal_profiles.csv',index=False)
    summary = contextual.groupby('cluster').agg(
        municipios=('id_municipio','size'),com_resultado_2024=('resultado_2024','count'),
        vulnerabilidade_mediana_2010=('proporcao_vulneravel','median'),
        idhm_renda_mediano_2010=('idhm_renda','median'),
        gini_mediano_2010=('indice_gini','median'),
        resultado_2024_media_municipal_nao_ponderada=('resultado_2024','mean'),
        ganho_anual_necessario_2030_mediano_pp=('ganho_anual_necessario_2030_pp','median'))
    summary.to_csv(reports/'profile_summary.csv')
    current.groupby('sigla_uf').agg(municipios=('id_municipio','size'),
        com_meta_2030=('meta_2030','count'),
        fracao_abaixo_meta_persistencia_2030=('abaixo_meta_persistencia_2030','mean'),
        ganho_anual_necessario_2030_mediano_pp=('ganho_anual_necessario_2030_pp','median')).to_csv(reports/'scenario_summary_uf.csv')

    fig,ax = plt.subplots(figsize=(8,4))
    ordered = pd.DataFrame(choices)
    ax.plot(ordered.k,ordered.silhouette,'o-',color='#0D5E7D')
    ax.set(title='Escolha exploratória do número de perfis',xlabel='Número de grupos (k)',ylabel='Silhouette')
    save(fig,images/'cluster_selection.png')
    fig,ax = plt.subplots(figsize=(9,5))
    palette = ['#0D5E7D','#D6A650','#499E8D','#AE6378','#7884B8','#7B644C']
    for i,group in eligible.groupby('cluster'):
        ax.scatter(group.pca_1,group.pca_2,s=10,alpha=0.5,label=f'Perfil {i} (n={len(group)})',color=palette[int(i)-1])
    ax.set(title='Perfis socioeconômicos municipais - PCA para visualização',
        xlabel=f'PC1 ({projection.explained_variance_ratio_[0]:.1%} da variância)',
        ylabel=f'PC2 ({projection.explained_variance_ratio_[1]:.1%} da variância)')
    ax.legend(fontsize=9)
    save(fig,images/'municipal_profiles_pca.png')
    fig,axes = plt.subplots(1,2,figsize=(11,4))
    current.gap_meta_2024_pp.dropna().hist(bins=30,ax=axes[0],color='#0D5E7D')
    axes[0].axvline(0,ls='--',color='#AE6378')
    axes[0].set(title='Resultado menos meta municipal de 2024',xlabel='Diferença (pontos percentuais)',ylabel='Municípios')
    current.ganho_anual_necessario_2030_pp.dropna().hist(bins=30,ax=axes[1],color='#499E8D')
    axes[1].set(title='Avanço anual necessário de 2024 a 2030',xlabel='Pontos percentuais/ano (cenário)',ylabel='Municípios')
    save(fig,images/'municipal_goals_scenarios.png')
    state = public_state.dropna(subset=['gap_2024_pp']).sort_values('gap_2024_pp')
    fig,ax = plt.subplots(figsize=(9,4))
    ax.bar(state.sigla_uf,state.gap_2024_pp,color=np.where(state.gap_2024_pp.ge(0),'#499E8D','#AE6378'))
    ax.axhline(0,color='#123047',lw=0.7)
    ax.set(title='UF: resultado público menos meta de 2024',ylabel='Pontos percentuais',xlabel='UF com resultado e meta disponíveis')
    save(fig,images/'state_gaps_2024.png')
    country = goals[goals.abrangencia.eq('Brasil')].sort_values('ano_resultado')
    fig,ax = plt.subplots(figsize=(7,4))
    ax.plot(country.ano_resultado,country.resultado,'o-',color='#0D5E7D',label='Resultado oficial da fonte')
    ax.set_xticks(country.ano_resultado)
    ax.set(title='Brasil: resultados agregados na fonte',xlabel='Ano de referência',ylabel='Alfabetização (%)')
    ax.legend()
    save(fig,images/'national_results.png')
    joblib.dump({'imputer':imputer,'scaler':scaler,'model':model,'pca':projection,
        'label_mapping':mapping,'features':CLUSTER_FEATURES},ROOT/'models/municipal_profiles.joblib')
    known = current.resultado_2024.notna() & current.meta_2024.notna()
    result = {'municipalities_with_2024_rows':len(current),
        'with_observed_2024_and_target':int(known.sum()),
        'below_2024_target':int((current.loc[known,'gap_meta_2024_pp']<0).sum()),
        'with_2030_target':int(current.meta_2030.notna().sum()),
        'profiled_municipalities':len(eligible),'excluded_profiles':len(excluded),
        'chosen_k':selected,'silhouette':float(selection.iloc[0].silhouette),
        'stability_ari':stability,'pca_explained_variance':projection.explained_variance_ratio_.tolist(),
        'social_reference':2010,'economic_reference':2021,'population_reference':2022,
        'scenario_base_year':2024,'forecasts_statistically_validated':False,
        'outcomes_or_targets_in_cluster_features':False,'cluster_features':CLUSTER_FEATURES}
    (reports/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
