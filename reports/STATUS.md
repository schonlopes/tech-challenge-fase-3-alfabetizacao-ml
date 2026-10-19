# Estado do projeto - 19/10/2026

Extração autorizada e concluída: 92.389 registros válidos de alunos de 2024, distribuídos por 5.193 municípios. O snapshot está somente local, ignorado pelo Git. A amostra integra Silver individual, Gold municipal de 2023 e população IBGE de 2022. Não houve criação ou alteração de tabelas cloud nesta etapa.

O experimento inicial selecionou regressão logística. A segunda versão testou contexto socioeconômico, mas não superou o modelo anterior na validação. Seus municípios de teste foram excluídos do novo desenvolvimento. Há SHAP global, dois perfis territoriais, análise de metas e cenários com limites explícitos. Relatórios em `v1/`, `v2/` e `territorial/`.

Verificação: **25 testes aprovados**, incluindo contratos, integridade, grupos sem sobreposição, preparação sem vazamento, enriquecimento, metas ausentes, cenários, backtest e agregação de SHAP. Os testes artificiais verificam o software; os relatórios de resultados usam dados reais e distinguem validação e teste.

SQL, metadados reduzidos de jobs e hash do snapshot estão em `evidence/`. O experimento verifica o hash antes do treinamento. Após o bloqueio inicial, houve autorização específica do usuário para a extração. Uma falha de codificação do Windows foi corrigida recuperando o resultado do mesmo job, sem repetir a consulta de extração.

## Prints reais: concluídos

A primeira tentativa foi interrompida por limitação do controle da interface. Nesta etapa, o acesso pelo navegador à conta correta funcionou: cinco prints reais foram salvos e catalogados em `evidence/GCP_SCREENSHOTS.md`. Mostram tabela, particionamento e execução concluída de consulta. O treinamento de ML foi local. Uma captura adicional com dados da conta permanece privada e ignorada pelo Git.

## Versionamento

Três branches locais de desenvolvimento criadas. O plano de publicação e integração por PR está em `../docs/GIT_WORKFLOW.md`. Nenhum push, PR remoto ou integração à main foi realizado nesta etapa.

## Pendências de entrega

Revisão final, apresentação e roteiro executivo, gravação de vídeo de até cinco minutos e publicação do GitHub por PRs. A matriz de critérios está em `../docs/atendimento_requisitos.md`.

## Extração realizada

Origem: tabelas do projeto GCP da Fase 2 e população pública do IBGE.

Destino: arquivo Parquet local em `data/raw/alunos_gold_modelagem.parquet`, ignorado pelo Git.

Conteúdo: 92.389 registros (aproximadamente 5% dos alunos válidos de 2024), com identificador de linha em hash, classificação alfabetizado/não alfabetizado convertida para risco, município, rede e série; contexto municipal da Gold 2023 e população de 2022. Não exporta nomes, ID bruto do aluno/escola, proficiência individual ou credenciais. Mesmo pseudonimizados, são registros individuais educacionais.

Finalidade: treinar e avaliar a pipeline local. Nenhum upload ou publicação de microdados está previsto. A auditoria de rótulos passou sem divergências entre os casos válidos.
