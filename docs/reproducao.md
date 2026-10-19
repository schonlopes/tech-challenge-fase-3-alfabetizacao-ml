# Reprodução, dados e credenciais

## Testes sem conta GCP

Os testes de software e a conferência do repositório não exigem acesso aos microdados, ao GCP ou ao modelo serializado. Criar o ambiente Python 3.11, instalar `requirements-lock.txt`, executar `python -m pytest -q` e `python scripts/check_repository.py`.

Esses testes não são uma nova avaliação do desempenho real: usam fixtures artificiais explicitamente identificadas nos testes.

## Experimentos reais

Para repetir os experimentos reais, são necessários o snapshot autorizado com hash correspondente ou acesso legítimo às fontes de dados. Credenciais não acompanham o repositório. Os snapshots individuais e os modelos locais também não são publicados.

O projeto GCP original é privado. O código não concede acesso a terceiros. Um avaliador com acesso autorizado pode executar os scripts com o projeto original; outro operador pode reconstruir as camadas da Fase 2 no próprio projeto e informar `--project ID_DO_SEU_PROJETO` nos dois scripts de extração.

Referência de engenharia da Fase 2: [repositório do pipeline](https://github.com/schonlopes/tech-challenge-fase-2-alfabetizacao-data-pipeline). A estrutura exigida pela Fase 3 é documentada nos SQLs de extração, incluindo datasets `alfabetizacao_silver` e `alfabetizacao_gold`. O projeto operador também precisa de permissão de leitura das fontes públicas da Base dos Dados e de execução/faturamento de queries. Usar um projeto diferente não torna os snapshots idênticos: revisões de fontes podem alterar os dados.

## Ordem de execução

1. `python scripts/extract_gcp.py --project ID_DO_PROJETO --sample-percent 5`: auditoria e snapshot individual.
2. `python -m src.run --search-iterations 4`: experimento original e artefato v1.
3. `python scripts/analyze_validation.py`: diagnósticos adicionais somente na validação.
4. `python scripts/extract_territorial.py --project ID_DO_PROJETO`: agregados socioeconômicos, indicadores e metas.
5. `python -m src.run_v2 --search-iterations 4`: comparação enriquecida sem os municípios do teste v1.
6. `python -m src.analyze_territories`: perfis e cenários municipais.
7. `python scripts/explain_shap.py`: explicação global do modelo logístico selecionado, sem exportar indivíduos.

Se outra fonte/versão selecionar uma floresta em vez de logística, o script de SHAP linear interrompe com uma mensagem: é necessário implementar uma explicação adequada ao novo estimador, em vez de gerar uma explicação incompatível.

Os scripts usam limites de bytes, consultas identificadas e manifests. O script de extração individual também aceita `--resume-audit-job` e `--resume-training-job`, verificando correspondência do SQL antes de recuperar um resultado já existente. Não reutilizar jobs de snapshots diferentes.

## Evidências e limitações

Os resultados versionados podem ser auditados sem repetir consultas: SQL, parâmetros, hashes, versões, métricas e prints reais estão documentados. A reprodução estatística dos resultados reais continua condicionada ao acesso legítimo à mesma base e ambiente.

Os prints são capturas de uma sessão real, não arquivos gerados pelo treinamento. `catalog_screenshots.py` apenas cataloga capturas existentes; não gera telas de GCP. A automação de CI prepara testes sem autenticação cloud e só será comprovada no GitHub após o push/PR.
