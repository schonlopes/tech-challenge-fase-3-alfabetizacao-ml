# Reprodução, dados e credenciais

## Testes sem conta GCP

Os testes de software e a conferência do repositório não exigem acesso aos microdados, ao GCP ou ao modelo serializado. Criar o ambiente Python 3.11, instalar `requirements-lock.txt`, executar `python -m pytest -q` e `python scripts/check_repository.py`.

Esses testes não são uma nova avaliação do desempenho real: usam fixtures artificiais explicitamente identificadas nos testes.

## Demonstração completa sem nuvem

Após instalar `requirements-lock.txt`, executar na raiz do projeto:

```powershell
python -m src.demo
```

Um único comando cria dados **artificiais identificados como tal**, separa municípios, treina uma pequena logística, salva/carrega o modelo e produz escores. Também verifica igualdade das previsões antes/depois da serialização e aceitação de categoria inédita. Não consulta GCP, não precisa de microdados e **não produz evidência de desempenho educacional**. Semente fixa 42; um argumento `--seed` permite outra simulação.

A pasta criada é informada na tela: `runs/synthetic-demo-<id>`. Para escolher o nome, usar `--output-dir runs/demo-local` (a pasta não pode existir). Artefato: `models/demo.joblib`; entrada preparada: `data/new_features.csv`; saída: `data/predictions.csv`; resumo: `reports/demo.json`, todos dentro da execução.

## Previsão com modelo salvo

Exemplo após a demonstração, usando explicitamente a mesma pasta nos dois comandos:

```powershell
python -m src.demo --output-dir runs/demo-local
python -m src.predict --artifact runs/demo-local/models/demo.joblib --input runs/demo-local/data/new_features.csv --output-dir runs/previsao-demo
```

Para uma análise real, substituir os caminhos por um artefato confiável e um CSV/Parquet autorizado. Não misturar o modelo artificial com resultados reais. A entrada deve conter os atributos já preparados do artefato; não exige rótulo, identificação do aluno ou proficiência. Para o modelo original: `taxa_municipal_anterior`, `log_populacao_anterior`, `rede`, `serie`, `sigla_uf`, `regiao`. O log é `log1p(populacao_anterior)`; a taxa está entre 0 e 100. Usar os códigos originais da rede (`2` estadual, `3` municipal), não trocar por seus nomes. Os atributos enriquecidos, se usados por outro modelo, também precisam ter sido preparados conforme `enrichment.py`.

Numéricas ausentes são imputadas pelo modelo treinado; infinitos, texto não numérico, taxa fora da faixa, log negativo, entrada vazia ou atributos ausentes são recusados. Categorias novas são aceitas pelo encoder, mas isso não comprova generalização. O operador deve conferir anos e disponibilidade dos atributos antes do desfecho: o comando não reconstrói esse histórico a partir de escores ou de colunas já preparadas.

Por padrão só há escores. `--use-artifact-threshold` ativa um alerta de pesquisa, não uma intervenção automática. Consultar [modelo e política](modelo_e_politica.md). Arquivos serializados somente de origem confiável: joblib/pickle pode executar código. Saídas individuais são privadas, mesmo sem nome.

## Execuções isoladas e rastreabilidade

Treinamento v1/v2, análise territorial, diagnósticos de validação, SHAP, demonstração e previsão gravam novas pastas em `runs/`. Os resultados históricos em `reports/v1`, `reports/v2`, `reports/territorial`, `images/` e `models/` não são substituídos por esses comandos.

Cada execução registra `run.json` com horário UTC, versão Python/dependências, commit Git, indicação de árvore modificada, hashes dos arquivos Python e requisitos, hashes das entradas e parâmetros. No encerramento bem-sucedido registra `completed` e hashes dos arquivos de saída. Uma execução interrompida permanece `started`, não deve ser tratada como completa. A pasta jamais é reutilizada; uma colisão interrompe a execução. Para comparar resultados, usar os parâmetros e hashes, não os nomes/horários das pastas.

`runs/` é ignorada pelo Git porque pode conter previsões e dados individuais. Para publicar uma evidência, selecionar apenas resumos agregados revisados, nunca a pasta inteira. O verificador de repositório recusa arquivos de `runs/` no índice. Os scripts de **extração** continuam responsáveis pelos snapshots e manifests de proveniência: não executar nova extração apenas para testar o software.

## Experimentos reais

Para repetir os experimentos reais, são necessários o snapshot autorizado com hash correspondente ou acesso legítimo às fontes de dados. Credenciais não acompanham o repositório. Os snapshots individuais e os modelos locais também não são publicados.

O projeto GCP original é privado. O código não concede acesso a terceiros. Um avaliador com acesso autorizado pode executar os scripts com o projeto original; outro operador pode reconstruir as camadas da Fase 2 no próprio projeto e informar `--project ID_DO_SEU_PROJETO` nos dois scripts de extração.

Referência de engenharia da Fase 2: [repositório do pipeline](https://github.com/schonlopes/tech-challenge-fase-2-alfabetizacao-data-pipeline). A estrutura exigida pela Fase 3 é documentada nos SQLs de extração, incluindo datasets `alfabetizacao_silver` e `alfabetizacao_gold`. O projeto operador também precisa de permissão de leitura das fontes públicas da Base dos Dados e de execução/faturamento de queries. Usar um projeto diferente não torna os snapshots idênticos: revisões de fontes podem alterar os dados.

## Ordem de execução

1. `python scripts/extract_gcp.py --project ID_DO_PROJETO --sample-percent 5`: auditoria e snapshot individual.
2. `python -m src.run --search-iterations 4 --output-dir runs/repro-v1`: repetição retrospectiva e artefato v1; não é um novo teste independente.
3. `python scripts/analyze_validation.py --artifact runs/repro-v1/models/risk_v1.joblib`: diagnósticos adicionais somente na validação.
4. `python scripts/extract_territorial.py --project ID_DO_PROJETO`: agregados socioeconômicos, indicadores e metas.
5. `python -m src.run_v2 --search-iterations 4 --baseline runs/repro-v1/models/risk_v1.joblib --output-dir runs/repro-v2`: comparação enriquecida sem os municípios do teste v1.
6. `python -m src.analyze_territories`: perfis e cenários municipais.
7. `python scripts/explain_shap.py --experiment-dir runs/repro-v2`: explicação global do modelo logístico selecionado, sem exportar indivíduos.

As pastas `runs/repro-v1` e `runs/repro-v2` devem ser novas; escolher outro nome em futuras repetições. Omitir `--output-dir` gera um nome único. O parâmetro `--baseline` é importante para vincular a v2 à execução correta; quando omitido, usa o artefato histórico local. Os diagnósticos e SHAP também aceitam `--output-dir` para isolar suas saídas.

Se outra fonte/versão selecionar uma floresta em vez de logística, o script de SHAP linear interrompe com uma mensagem: é necessário implementar uma explicação adequada ao novo estimador, em vez de gerar uma explicação incompatível.

Os scripts usam limites de bytes, consultas identificadas e manifests. O script de extração individual também aceita `--resume-audit-job` e `--resume-training-job`, verificando correspondência do SQL antes de recuperar um resultado já existente. Não reutilizar jobs de snapshots diferentes.

## Evidências e limitações

Os resultados versionados podem ser auditados sem repetir consultas: SQL, parâmetros, hashes, versões, métricas e prints reais estão documentados. A reprodução estatística dos resultados reais continua condicionada ao acesso legítimo à mesma base e ambiente.

Os prints são capturas de uma sessão real, não arquivos gerados pelo treinamento. `catalog_screenshots.py` apenas cataloga capturas existentes; não gera telas de GCP. A automação de CI prepara testes sem autenticação cloud e só será comprovada no GitHub após o push/PR.
