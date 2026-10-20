# Predição e inteligência analítica para alfabetização no Brasil

Tech Challenge da Fase 3. Projeto em desenvolvimento local, a partir da infraestrutura e da Gold da Fase 2.

## Problema e objetivo

Antecipar risco educacional para apoiar a priorização de acompanhamento pedagógico. O objetivo principal é classificação individual de alfabetização, acompanhada de análises territoriais. As previsões são apoio à decisão humana, não decisões automáticas sobre alunos.

## Estado atual

Auditoria de dados reais no GCP realizada. A primeira implementação local contém extração limitada por custo, contrato, EDA, pré-processamento, otimização por validação agrupada e avaliação com teste territorial. **O experimento real ainda não foi executado**: a extração local dos microdados aguarda autorização específica após bloqueio da revisão automática de permissões. Não há métricas de desempenho a reportar.

Amostras sintéticas da Fase 2 e eventos simulados de Pub/Sub não serão utilizados para avaliar os modelos. Fixtures artificiais existem somente nos testes de software e não constituem evidência de desempenho educacional.

## Origem e limite da base

A Gold da Fase 2 é municipal. Para cumprir a unidade individual do enunciado, a Fase 3 cria uma **extensão Gold de modelagem local**, integrando alunos válidos da Silver com contexto histórico municipal da Gold. Não confundir essa extensão com uma tabela individual já existente na Gold da Fase 2.

Os microdados têm poucos atributos individuais. O primeiro modelo será, principalmente, um estimador de risco contextual; não deve ser apresentado como diagnóstico individual completo. Ausência de avaliação não é evidência de não alfabetização.

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

## Base e atributos

Amostra por hash de aproximadamente 5% dos alunos elegíveis em 2024. Exclui ausentes, proficiência nula e origem simulada. O alvo é `risco=1` para não alfabetizado; a proficiência serve apenas à auditoria da coerência do rótulo. A presença não entra como atributo.

Atributos iniciais: taxa municipal de alfabetização de 2023, log da população de 2022, rede, série, UF e região. Identificadores individuais não entram no modelo. A população é contexto demográfico; o enriquecimento socioeconômico propriamente dito ainda está pendente.

## Modelagem e validação

- Baselines: DummyClassifier com prevalência do treino e risco histórico municipal (`1 - taxa anterior/100`).
- Candidatos: regressão logística e Random Forest. A escolha final depende dos resultados, não de preferência prévia por maior complexidade.
- Numéricas: imputação por mediana e escalonamento. Categóricas: imputação e One-Hot Encoding que aceita categorias novas.
- As transformações ficam em Pipeline/ColumnTransformer; nenhum ajuste usa validação ou teste.
- Município é a unidade de separação: buckets determinísticos de 60%/20%/20% para treino/validação/teste; busca de hiperparâmetros com GroupKFold em três folds no treino.
- Seleção por average precision na validação; limiar por F2 na validação. O teste é usado somente após essa seleção.
- Relatórios: AP, ROC-AUC, precisão, recall, F1/F2, Brier, matriz de confusão, calibração, fração de alertas, bootstrap por município e recortes por UF.
- Interpretação: importância por permutação na validação. Não é evidência de causalidade.

## Como reproduzir

Python 3.11 ou superior. Dentro desta pasta, no PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe -m pytest -q

# Requer Google Cloud SDK, sessão autenticada e autorização de acesso/extração.
.venv\Scripts\python.exe scripts/extract_gcp.py --sample-percent 5
.venv\Scripts\python.exe -m src.run --search-iterations 4
```

É possível usar `requirements.txt` para uma instalação com versões compatíveis; `requirements-lock.txt` registra o ambiente utilizado nos testes iniciais. A extração exige acesso ao projeto `tech-challenge-fase-2-506814` e às fontes públicas referenciadas. Nenhuma credencial deve ser colocada no repositório.

## Resultados e aplicação prática

Ainda pendentes de execução real. O fluxo está preparado para produzir os resultados em `reports/v1/` e oito gráficos em `images/v1/`. A análise municipal do teste publica apenas agregados com pelo menos 30 alunos amostrados, com finalidade exploratória.

Após validação, os escores poderão apoiar a triagem de territórios para investigação e planejamento pedagógico. O contexto municipal compartilhado por muitos alunos limita a personalização; não usar para rotular definitivamente crianças, negar atendimento ou atribuir responsabilidade individual.

## Limitações e próximos passos

Esta versão é retrospectiva em 2024, com teste em municípios separados. Não demonstra previsão de 2025 ou cumprimento futuro de metas. A disponibilidade dos indicadores históricos antes do momento de previsão precisa ser comprovada. Os resultados serão amostrais e não ponderados; não equivalem aos indicadores oficiais. A escassez de atributos individuais limita a previsão individual.

Pendentes: enriquecimento socioeconômico, análise das metas nacionais/estaduais, agrupamentos territoriais, viabilidade de previsão temporal, prints reais do console, revisão dos resultados, apresentação e vídeo. O detalhamento está em `docs/protocolo_analitico.md`.

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

O Git local foi iniciado com um commit de escopo/auditoria e uma branch de desenvolvimento de funcionalidades. Os commits acompanham trabalho real. A publicação no GitHub e as PRs serão feitas em etapa posterior; não são apresentadas como concluídas.
