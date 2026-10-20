# Predição e inteligência analítica para alfabetização no Brasil

Tech Challenge da Fase 3. Projeto em desenvolvimento local, a partir da infraestrutura e da Gold da Fase 2.

## Problema e objetivo

Antecipar risco educacional para apoiar a priorização de acompanhamento pedagógico. O objetivo principal é classificação individual de alfabetização, acompanhada de análises territoriais. As previsões são apoio à decisão humana, não decisões automáticas sobre alunos.

## Estado atual

**Experimentos reais e análises executados em 19/10/2026**, com 92.389 alunos de 5.193 municípios e contexto público de 5.571 municípios. A classificação inclui preparação integrada, otimização e validação por município; a análise territorial inclui perfis, metas e cenários. **25 testes passaram**, e cinco prints reais do console GCP estão documentados. O projeto ainda depende da apresentação, vídeo e publicação com PRs para concluir a entrega.

Amostras sintéticas da Fase 2 e eventos simulados de Pub/Sub não serão utilizados para avaliar os modelos. Fixtures artificiais existem somente nos testes de software e não constituem evidência de desempenho educacional.

## Origem e limite da base

A Gold da Fase 2 é municipal. Para cumprir a unidade individual do enunciado, a Fase 3 cria uma **extensão Gold de modelagem local**, integrando alunos válidos da Silver com contexto histórico municipal da Gold. Não confundir essa extensão com uma tabela individual já existente na Gold da Fase 2.

Os microdados têm poucos atributos individuais. O modelo é, principalmente, um estimador de risco contextual; não deve ser apresentado como diagnóstico individual completo. Ausência de avaliação não é evidência de não alfabetização.

## Arquitetura e fluxo

```text
GCP Silver: alunos válidos de 2024 -----+
Gold Fase 2: contexto municipal 2023 ---+--> extensão Gold local (Parquet)
IBGE: população municipal de 2022 -----+              |
                                          separação por município
                                         /           |           \
                                      treino     validação      teste
                                         |           |           |
                                  busca com CV   modelo/limiar   avaliação final
                                         +-----------+-----------+
                                                     |
                                           métricas, gráficos e modelo
```

As consultas de extração são somente leitura: não criam nem substituem tabelas da Fase 2. Filtram os anos e as colunas e têm limite padrão de 2 GB faturáveis por consulta. O script faz duas consultas principais; o teto é um limite de processamento por consulta, não uma promessa de preço final. Jobs e hashes ficam registrados em `reports/evidence/`. Microdados e modelos locais são ignorados pelo Git.

O fluxo acima descreve o experimento v1. O enriquecimento v2 reutiliza somente treino/validação, sem novo teste final. IPEA 2010 e PIB 2021 entram como contexto histórico. Indicadores e metas agregados seguem um fluxo separado para perfis e cenários, sem alimentar o alvo individual. As consultas territoriais têm teto de 1 GB por consulta.

## Base e atributos

Amostra por hash de aproximadamente 5% dos 1.851.852 alunos elegíveis em 2024: 92.389 registros. Exclui ausentes, proficiência nula e origem simulada. O alvo é `risco=1` para não alfabetizado; a proficiência serve apenas à auditoria da coerência do rótulo. A presença não entra como atributo. A auditoria não encontrou divergências entre os rótulos válidos e o corte de 743 pontos.

Atributos iniciais: taxa municipal de alfabetização de 2023, log da população de 2022, rede, série, UF e região. Identificadores individuais não entram no modelo. O enriquecimento experimental acrescenta renda, desigualdade, vulnerabilidade, infraestrutura e composição econômica, com anos e limitações em [docs/fontes_e_disponibilidade.md](docs/fontes_e_disponibilidade.md).

## Modelagem e validação

- Baselines: DummyClassifier com prevalência do treino e risco histórico municipal (`1 - taxa anterior/100`).
- Candidatos: regressão logística e Random Forest. A escolha final depende dos resultados, não de preferência prévia por maior complexidade.
- Numéricas: imputação por mediana e escalonamento. Categóricas: imputação e One-Hot Encoding que aceita categorias novas.
- As transformações ficam em Pipeline/ColumnTransformer; nenhum ajuste usa validação ou teste.
- Município é a unidade de separação: buckets determinísticos de 60%/20%/20% para treino/validação/teste; busca de hiperparâmetros com GroupKFold em três folds no treino.
- Seleção por average precision na validação; limiar por F2 na validação. O teste é usado somente após essa seleção.
- Relatórios: AP, ROC-AUC, precisão, recall, F1/F2, Brier, matriz de confusão, calibração, fração de alertas, bootstrap por município e recortes por UF.
- Interpretação: permutação e SHAP global na validação, sem exportar explicações individuais. Contribuições SHAP são em log-odds, não pontos percentuais de probabilidade; nenhuma técnica demonstra causalidade.

## Como reproduzir

Python 3.11 ou superior. Dentro desta pasta, no PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe -m pytest -q

# Requer Google Cloud SDK, sessão autenticada e autorização de acesso/extração.
.venv\Scripts\python.exe scripts/extract_gcp.py --sample-percent 5
.venv\Scripts\python.exe -m src.run --search-iterations 4
.venv\Scripts\python.exe scripts/analyze_validation.py

# Complementos v2: somente agregados públicos novos; snapshot individual reutilizado.
.venv\Scripts\python.exe scripts/extract_territorial.py
.venv\Scripts\python.exe -m src.run_v2 --search-iterations 4
.venv\Scripts\python.exe -m src.analyze_territories
.venv\Scripts\python.exe scripts/explain_shap.py
```

É possível usar `requirements.txt` para versões compatíveis; `requirements-lock.txt` registra o ambiente atual, incluindo SHAP. A extração exige acesso ao projeto `tech-challenge-fase-2-506814` e às fontes públicas referenciadas. Nenhuma credencial deve ser colocada no repositório. O treinamento é local; as consultas e tabelas de origem ficam no GCP.

Os testes podem ser repetidos sem conta cloud. Os experimentos reais exigem acesso legítimo ao snapshot/projeto; os scripts de extração aceitam `--project` para uma reconstrução própria das camadas. [Acesso e reprodução detalhados](docs/reproducao.md).

## Resultados e aplicação prática

Treino: 61.503 alunos / 3.074 municípios. Validação: 15.163 / 1.086. Teste: 15.723 / 1.033. Nenhum município pertence a mais de um conjunto. A EDA de rótulos foi restrita ao treino.

| Modelo ou referência | Average precision no teste | ROC-AUC no teste |
| --- | ---: | ---: |
| Regressão logística selecionada | 0,5250 | 0,6560 |
| Indicador histórico municipal | 0,5086 | 0,6377 |
| Frequência das classes no treino | 0,3889 | 0,5000 |

No teste, 38,89% dos alunos avaliados pertencem à classe de risco. O intervalo de 95% por bootstrap de municípios é aproximadamente [0,5072; 0,5444] para AP e [0,6360; 0,6701] para ROC-AUC. O ganho sobre o histórico é observado nesta amostra; não foi realizado teste pareado de significância da diferença.

**Limitação operacional importante:** o limiar F2 de 0,16 produz recall de 99,07%, mas precisão de 40,23% e sinaliza 95,76% dos alunos. Portanto, esse limiar é pouco seletivo e não serve, sozinho, para priorização de recursos escassos. O relatório discute alternativas exploratórias de capacidade usando somente a validação; elas não foram utilizadas para reajustar o resultado do teste.

Resultados detalhados em [reports/v1/INTERPRETACAO.md](reports/v1/INTERPRETACAO.md), métricas em [reports/v1/experiment.json](reports/v1/experiment.json) e oito gráficos em `images/v1/`. A análise municipal do teste disponibiliza apenas agregados com pelo menos 30 alunos amostrados, com finalidade exploratória.

O contexto municipal anterior é o atributo de maior importância por permutação. Isso indica dependência do modelo em padrões territoriais, não causalidade ou identificação completa de fatores individuais.

Após validação, os escores poderão apoiar a triagem de territórios para investigação e planejamento pedagógico. O contexto municipal compartilhado por muitos alunos limita a personalização; não usar para rotular definitivamente crianças, negar atendimento ou atribuir responsabilidade individual.

## Enriquecimento, perfis e metas

O enriquecimento socioeconômico não melhorou o AP observado na validação: 0,5587 no modelo original, 0,5578 na logística enriquecida e 0,5561 na floresta enriquecida. Mantivemos a referência mais simples, sem reavaliar o teste original. A alternativa de até 20% de alertas é exploratória de validação; não é a mesma política do limiar F2 do teste v1. [Interpretação da v2](reports/v2/INTERPRETACAO.md).

A segmentação de 5.565 municípios selecionou dois perfis (silhouette 0,3747), sem usar alfabetização para formar os grupos. As médias municipais não ponderadas de alfabetização de 2024 são 66,92% e 57,57%, descritas somente depois da formação dos perfis. Isso não identifica efeito causal de renda ou vulnerabilidade.

Na Gold consultada, 2.444 dos 5.232 municípios com resultado e meta comparáveis ficaram abaixo da meta de 2024. Há cenários de persistência/ganho constante e cálculo do avanço anual necessário para 2030. Uma referência retrospectiva de persistência 2023-2024 obteve MAE de 12,45 p.p.; isso não valida uma projeção até 2030. [Interpretação territorial](reports/territorial/INTERPRETACAO.md).

A junção de metas foi corrigida localmente: `Municipal` corresponde ao código `3`, e `Pública` ao `5`; a incompatibilidade anterior deixava metas sem associação. [Diagnóstico e correção](docs/correcao_redes.md). As tabelas cloud da Fase 2 não foram substituídas.

## Evidências reais de GCP

[Cinco capturas reais do console](reports/evidence/GCP_SCREENSHOTS.md) mostram a Gold, as partições e a consulta concluída, com horários, bytes e linhas processadas. Os prints comprovam a execução de dados/consultas na nuvem; não afirmam que o treinamento local ocorreu no GCP. Jobs e hashes complementam as imagens.

## Limitações e próximos passos

Esta versão é retrospectiva em 2024, com teste em municípios separados. Não demonstra generalização individual para anos futuros ou cumprimento futuro de metas. A primeira divulgação do indicador de 2023 ocorreu em maio de 2024, mas o snapshot atual pode conter revisões; uma reprodução estritamente histórica exigiria versões disponíveis à época. As métricas individuais são amostrais e não ponderadas, diferentes dos indicadores oficiais. O contexto social de 2010 é antigo, e a escassez de atributos individuais limita a personalização.

Pendentes para entrega: revisão final, apresentação e roteiro de até cinco minutos, gravação do vídeo e publicação por PRs. Para evolução científica: novos dados independentes, atributos individuais/escolares anteriores ao desfecho e validação temporal mais ampla. [Checklist de atendimento](docs/atendimento_requisitos.md).

## Organização e Git

```text
data/           snapshots e extensão Gold local (ignorados no Git)
sql/            consultas rastreáveis de auditoria e extração
scripts/        extração do GCP
src/            preprocessing, modeling, evaluation, visualization e execução
tests/          contratos, vazamento e execução integrada com fixtures artificiais
notebooks/      orientação de navegação dos scripts analíticos
reports/        auditoria, evidências e resultados
images/         gráficos reproduzíveis
docs/           protocolo e decisões
```

O Git local registra escopo, implementação, correções, experimentos e interpretação em commits próprios. Existem três branches de desenvolvimento, incluindo `feat/socioeconomic-territorial-analysis`. O plano das três PRs e a ordem de integração estão em [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md). A publicação no GitHub e as PRs serão feitas em etapa posterior; não são apresentadas como concluídas.
