# Perfis territoriais, metas e cenários

## Diagnóstico municipal

A extensão usa indicadores oficiais da Gold e corrige localmente a compatibilidade entre códigos de rede e nomes das metas. A rede Municipal corresponde ao código 3; a rede Pública estadual/municipal corresponde a 5. Não misturar com Total, código 0, que inclui rede privada.

Há 5.448 linhas municipais de 2024 na Gold consultada. Destas, 5.232 possuem resultado e meta de 2024 comparáveis: **2.444 ficaram abaixo da meta (46,71%)**. As 216 sem comparação completa não são tratadas como metas atingidas. Há meta de 2030 em 5.352 linhas municipais.

Os arquivos `largest_observed_gaps_2024.csv`, `municipal_scenarios.csv` e `scenario_summary_uf.csv` apoiam a investigação de territórios. A primeira tabela é diagnóstico observado, não um ranking preditivo independente. Dados e metas usam o snapshot atual, possivelmente revisado.

## Dois perfis socioeconômicos

Foram agrupados 5.565 municípios; seis não tinham cobertura histórica suficiente. K-Means foi ajustado em atributos socioeconômicos e população, sem resultados ou metas de alfabetização na formação dos grupos. Cada município tem peso igual.

Entre k=2 e k=6, o critério silhouette selecionou dois grupos, com escore 0,3747. Nas três comparações entre sementes 7, 21 e 42, o Adjusted Rand Index foi 1,0. Isso indica estabilidade à inicialização testada, não estabilidade a mudanças de ano, população ou seleção de atributos. A projeção PCA é somente visual e representa aproximadamente 73,0% da variância nas duas primeiras componentes.

| Medida | Perfil 1 | Perfil 2 |
| --- | ---: | ---: |
| Municípios agrupados | 3122 | 2443 |
| Vulnerabilidade histórica mediana (%) | 25,57 | 66,90 |
| IDHM renda mediano de 2010 | 0,701 | 0,565 |
| Municípios com resultado municipal de 2024 | 3050 | 2394 |
| Média municipal não ponderada da alfabetização de 2024 (%) | 66,92 | 57,57 |
| Mediana do avanço anual necessário de 2024 a 2030 (p.p./ano) | 1,90 | 4,11 |

As diferenças educacionais foram descritas **depois** de formar os perfis. Não são estimativas causais nem indicadores nacionais ponderados por alunos. A composição de atributos correlacionados e o uso de contexto de 2010 influenciam os grupos; os nomes numéricos não são rótulos definitivos de vulnerabilidade atual.

## Referência temporal simples

Foi fixada uma regra de persistência: usar o resultado municipal de 2023 como estimativa de 2024. Nos 5.232 pares completos com meta, o MAE foi 12,45 p.p. e o RMSE 16,81 p.p. Para identificar municípios abaixo da meta de 2024, a precisão foi 47,11% e o recall 82,94%.

Esse é um backtest retrospectivo de **uma única transição anual**, com snapshots atuais. Mostra o erro de uma referência simples, não valida ARIMA ou uma projeção de longo prazo. Os números estão em `persistence_backtest.json`.

## Cenários para metas

O ponto de partida é o resultado de 2024. São calculados:

- Persistência: manter o resultado de 2024 e comparar com metas de 2025/2030.
- Ganho constante: repetir a diferença observada de 2023 a 2024, limitando a escala a 0-100; perdas também são mantidas nesse cenário.
- Avanço necessário: diferença positiva entre a meta e o resultado de 2024, dividida pelo horizonte.

O cenário 2025 é uma simulação retrospectiva; não é apresentado como futuro a partir de 2026. Os cenários 2030 são hipóteses, não previsões estatísticas validadas nesse horizonte. Município sem meta permanece sem avaliação, não aprovado.

## Brasil e UFs

`national_state_results.csv` preserva os anos dos resultados oficiais: não transforma o Brasil em média de municípios. Na extração, os valores nacionais são 55,9% em 2023, 59,2% em 2024 e 66,0% em 2025, com metas correspondentes conforme cada linha da fonte. Diferenças de arredondamento/revisão nas metas foram preservadas, não corrigidas manualmente.

`state_2024_public.csv` e o gráfico de lacunas comparam apenas a rede Pública (código 5), para UFs com resultado/meta disponíveis. Não concluir que UF ausente está sem risco, nem atribuir causalidade a uma lacuna.

## Aplicação em políticas públicas

Os produtos ajudam a investigar municípios com lacunas observadas e necessidades de avanço semelhantes, organizar discussões de cooperação e selecionar perguntas para avaliação pedagógica. Decisões de investimento exigem dados atuais, condições locais, análise de equidade e avaliação de intervenções; os perfis e escores não substituem esse trabalho.
