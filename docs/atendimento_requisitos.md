# Atendimento à proposta da Fase 3

Avaliação local em 19/10/2026. Esta matriz distingue implementação, evidência e pendências; não é garantia de nota.

| Critério | Situação | Evidência |
| --- | --- | --- |
| Problema educacional e classificação individual | Implementado com limites | README, alvo individual válido e `reports/v1/INTERPRETACAO.md` |
| Utilizar a Gold da Fase 2 | Implementado por extensão explícita | Gold municipal integrada à Silver individual; SQL, jobs e manifest; não alegar Gold individual pré-existente |
| EDA e hipóteses orientando a modelagem | Implementado | Distribuições e faltantes no treino; hipóteses abaixo |
| Imputação, transformação e encoding | Implementado | Pipeline, ColumnTransformer, mediana, indicadores de ausência, log, scaling e One-Hot |
| Evitar vazamento | Implementado com limitações históricas documentadas | Allowlist, grupos por município, datas, ausência/proficiência excluídas dos atributos, hash e testes |
| Treinamento, otimização e validação | Implementado | Dummy/histórico/logística/floresta, busca com GroupKFold, validação e teste v1, comparação v2 sem novo teste |
| Replicabilidade e generalização | Demonstrado no escopo territorial | Dependências fixadas, sementes, demo sem nuvem, escores com artefato salvo, execuções isoladas e 36 testes; generalização temporal individual não demonstrada |
| Interpretabilidade | Implementado | Permutação e SHAP global com conferência de aditividade; não causal |
| Fatores associados e territórios de risco | Implementado como apoio analítico | Importâncias, recortes por UF, lacunas oficiais de metas e relatórios |
| Regiões/municípios com padrões semelhantes | Implementado | K-Means por município, silhouette, estabilidade entre sementes, PCA e perfis |
| Metas futuras | Cenários explícitos e referência retrospectiva | Persistência/ganho constante, avanço necessário, backtest 2023-2024; sem previsão validada para 2030 |
| Metas nacionais/estaduais/municipais | Implementado | Anos e redes separados; normalização dos códigos; não produzir Brasil por média simples |
| Enriquecimento externo | Implementado | IPEA 2010, PIB 2021 e população 2022, com proveniência e limites de atualização |
| Estrutura, README, código e documentação | Implementado localmente | Pastas exigidas, scripts reproduzíveis e relatórios; a proposta aceita scripts ou notebooks |
| Histórico e branches Git | Implementado localmente | Commits reais e cinco branches; `GIT_WORKFLOW.md` |
| Repositório remoto e PRs | Pendente | Planejadas cinco PRs em sequência; ainda não publicadas |
| Evidência visual do GCP (feedback da Fase 2) | Adicionada | Cinco prints reais em `reports/evidence/GCP_SCREENSHOTS.md` |
| Vídeo executivo até 5 minutos | Concluído | Vídeo final conferido: 292,5s no MKV original e 292,4s no MP4 publicado; oito slides e roteiro de 507 palavras |

## Hipóteses e decisões decorrentes

1. Histórico municipal pode ajudar a antecipar risco contextual. O primeiro experimento observou ganho sobre a frequência das classes, mas o efeito operacional do limiar F2 foi insuficiente para priorização seletiva.
2. Renda, vulnerabilidade e infraestrutura históricas poderiam acrescentar informação. A comparação v2 não mostrou ganho de AP na validação; por isso, mantivemos a referência mais simples em vez de escolher automaticamente um modelo mais complexo.
3. Municípios com contexto parecido podem compartilhar desafios. A segmentação sem usar alfabetização na formação dos grupos encontrou dois perfis, com diferenças educacionais posteriores descritas sem causalidade.
4. Um resultado estável no tempo seria uma referência de previsão. A checagem de persistência 2023-2024 apresentou erro relevante; por isso, os cenários de 2030 são apresentados como hipóteses, não como previsão confiável de longo prazo.

## Limitações que devem aparecer também na apresentação

Poucos atributos individuais; contexto social de 2010; métricas individuais não ponderadas; resultado agregado oficial diferente da amostra; teste individual apenas territorial em 2024; snapshots revisados sem reprodução estrita de disponibilidade histórica; limiar operacional v2 avaliado somente na validação; perfis e SHAP sem significado causal.
