# Enriquecimento socioeconômico: resultado da segunda versão

## Objetivo e avaliação

Acrescentar renda, desigualdade, vulnerabilidade, saneamento, escolaridade dos responsáveis e contexto econômico para verificar ganho preditivo. Foram reutilizados os dados individuais já autorizados, sem nova extração de alunos.

O desenvolvimento usa 61.503 alunos de treino e 15.163 de validação. Todos os municípios do teste v1 foram excluídos. Estes resultados são **somente de validação**, não um novo teste independente.

## Comparação observada

| Candidato | AP de validação | ROC-AUC de validação |
| --- | ---: | ---: |
| Regressão logística v1 congelada | 0,5587 | 0,6730 |
| Regressão logística enriquecida | 0,5578 | 0,6725 |
| Random Forest enriquecida | 0,5561 | 0,6694 |
| Indicador histórico municipal | 0,5388 | 0,6508 |

O enriquecimento **não apresentou ganho observado** pelo critério pré-definido. Isso não prova ausência de relação socioeconômica com alfabetização. As variáveis novas são agregadas, algumas antigas, e compartilham informação com município/UF e histórico educacional. A escolha permanece com a versão mais simples já treinada; não há justificativa empírica para substituí-la por um modelo mais complexo nesta rodada.

## Política ilustrativa de capacidade

Com um teto ilustrativo de 20% de alertas e preservando empates, a versão selecionada sinaliza 19,96% dos alunos da validação, com precisão de 60,11% e recall de 30,09%. Esse limiar exploratório não foi reavaliado no teste v1, e não é uma política aprovada por gestores.

O artefato `risk_v2.joblib` guarda essa configuração experimental. O modelo e a avaliação original v1 permanecem preservados. Não misturar resultados de validação deste limiar com os resultados do teste do limiar F2 original.

## SHAP e interpretação

Foi aplicado LinearExplainer ao modelo logístico selecionado: fundo de referência com 200 registros de treino e explicações para 500 de validação, semente 42. Nenhum aluno do teste foi explicado, e nenhum resultado individual foi exportado.

Os efeitos são em **log-odds do risco**, não pontos percentuais de probabilidade. Os efeitos de One-Hot e indicadores de ausência foram somados por atributo original antes da média de valores absolutos. A soma reconstruída foi conferida contra a função de decisão, com erro máximo de aproximadamente 4,44e-16.

UF, região e histórico municipal são correlacionados. A alocação da contribuição depende do fundo e da hipótese de independência do explainer; não demonstra causalidade. Ver `shap_global.csv`, `shap_metadata.json` e `images/v2/shap_global.png`.

## Qualidade e limites

Os indicadores sociais são de 2010 e o PIB é de 2021, sempre identificados como contexto histórico. Um município apresentou duas razões econômicas fora do intervalo adequado à interpretação de composição; os valores originais foram preservados em `economic_composition_unavailable.csv`, os atributos foram marcados como indisponíveis e a imputação permaneceu ajustada no treino.

As novas bases foram úteis para segmentação e diagnóstico territorial, mesmo sem ganho na classificação individual. Para melhorar a personalização, será necessário acesso legítimo a atributos individuais ou escolares anteriores ao desfecho, com qualidade, datas e governança adequadas. Não é correto inventar características ou usar a proficiência que define o próprio alvo para obter métricas maiores.
