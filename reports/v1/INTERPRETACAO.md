# Interpretação do primeiro experimento real

## População e separação

Estudo retrospectivo de alunos avaliados em 2024, com contexto municipal de 2023 e população municipal de 2022. Amostra determinística de aproximadamente 5%: 92.389 alunos, 5.193 municípios. Excluídos ausentes, proficiência ausente e eventos simulados. Os registros individuais pseudonimizados permanecem locais e fora do Git.

| Conjunto | Alunos | Municípios |
| --- | ---: | ---: |
| Treino | 61503 | 3074 |
| Validação | 15163 | 1086 |
| Teste | 15723 | 1033 |

Não há município compartilhado entre conjuntos. A taxa municipal histórica falta em 1,94% da amostra, tratada pelo pipeline; população e território estão preenchidos. A exploração de rótulos foi restrita ao treino.

## Seleção e teste

Na validação, a regressão logística obteve AP 0,5587 e a Random Forest 0,5581. A diferença observada é pequena e não prova superioridade estatística. A regra pré-definida selecionou a regressão logística. A busca no treino escolheu C=0,01. Ver `validation_comparison.csv` e arquivos `*_cv.csv`.

| Referência | AP no teste | ROC-AUC no teste | Brier (menor é melhor) |
| --- | ---: | ---: | ---: |
| Regressão logística | 0,5250 | 0,6560 | 0,2206 |
| Risco histórico municipal | 0,5086 | 0,6377 | 0,2259 |
| Frequência das classes | 0,3889 | 0,5000 | 0,2380 |

AP resume a curva precisão-recall; não é acurácia. A prevalência de não alfabetizados no teste é 38,89%. O ganho sobre o histórico simples é modesto. Em 100 reamostragens de municípios, os intervalos percentis de 95% são [0,5072; 0,5444] para AP e [0,6360; 0,6701] para ROC-AUC. Não houve teste pareado de diferença entre modelos; esses intervalos tampouco cobrem toda a incerteza do desenho da pesquisa original.

O teste contém municípios diferentes dos usados no desenvolvimento. Não avalia ano futuro nem acompanhamento longitudinal da mesma criança.

## Recall alto e limitação de priorização

O limiar 0,16 foi selecionado por F2 na validação. No teste, identifica 6.057 casos de risco e deixa 57 sem identificar, mas também sinaliza indevidamente 9.000 alunos alfabetizados; apenas 609 alfabetizados não são sinalizados. O resultado é recall de 99,07%, precisão de 40,23% e 95,76% dos alunos sinalizados.

Encontrar quase todos os casos ao sinalizar quase todos os alunos torna esse limiar inadequado, isoladamente, para uma equipe com capacidade limitada. Não apresentar recall como demonstração suficiente de utilidade operacional.

## Capacidade: análise exploratória somente na validação

Após congelar o teste, analisamos o modelo já treinado na validação, sem refit e sem nova avaliação no teste. Escores empatados são mantidos juntos, reduzindo eventualmente a capacidade efetiva.

| Teto de alunos sinalizados | Fração efetiva | Precisão | Recall |
| --- | ---: | ---: | ---: |
| 10% | 9,98% | 64,80% | 16,23% |
| 20% | 19,96% | 60,11% | 30,09% |
| 30% | 29,16% | 56,65% | 41,43% |

São resultados exploratórios de validação, não novos resultados de teste nem uma política de atendimento aprovada. Priorizar menos alunos aumenta a precisão, mas deixa mais casos fora da seleção. A decisão exige considerar recursos, equidade e avaliação pedagógica. Ver `validation_capacity_options.csv` e `scripts/analyze_validation.py`.

## Interpretação

A taxa municipal de 2023 tem a maior importância por permutação, seguida da UF. Série é constante e tem importância zero. População apresenta importância muito pequena nesta configuração. UF e região são correlacionadas, limitando interpretações isoladas.

A importância é calculada na mesma subamostra de até 5.000 registros de validação, com cinco repetições. A revisão corrigiu a primeira geração do gráfico, garantindo amostra idêntica no baseline e nas permutações. Essa correção não alterou o modelo, o limiar ou as métricas do teste.

O modelo aprende sobretudo risco contextual: alunos com contexto igual recebem escores iguais. Importância não demonstra causalidade nem permite concluir quais intervenções melhorariam alfabetização.

## Uso e limites

Os escores podem apoiar investigação territorial após validação adicional. Não são diagnóstico individual nem devem determinar acesso ou restrição a políticas educacionais.

`test_municipalities_min30.csv` contém somente municípios do teste com ao menos 30 alunos amostrados. Não é ranking nacional validado. Não comparar diretamente essas probabilidades com metas oficiais: a amostra não é ponderada e o produto difere do indicador oficial.

As referências temporais são anteriores ao desfecho, mas a disponibilidade efetiva dos indicadores antes da previsão ainda precisa ser comprovada. O enriquecimento socioeconômico, as metas futuras e os agrupamentos de municípios exigem etapas próprias.

## Próximos passos

1. Enriquecer contexto socioeconômico e infraestrutura com proveniência e datas, evitando o resultado contemporâneo como entrada.
2. Definir a política operacional na validação e verificar desempenho em novo teste independente. Não reutilizar este teste para escolher novas versões.
3. Avaliar generalização temporal quando houver histórico suficiente.
4. Produzir análise específica de metas e perfis territoriais, distinguindo descrição de previsão.
5. Capturar prints reais do GCP e finalizar documentação executiva, apresentação, vídeo e PRs.
