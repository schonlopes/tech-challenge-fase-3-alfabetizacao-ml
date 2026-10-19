# Estado da primeira versão - 19/10/2026

Extração autorizada e concluída: 92.389 registros válidos de alunos de 2024, distribuídos por 5.193 municípios. O snapshot está somente local, ignorado pelo Git. A amostra integra Silver individual, Gold municipal de 2023 e população IBGE de 2022. Não houve criação ou alteração de tabelas cloud nesta etapa.

O experimento real terminou com a seleção da regressão logística na validação. Resultados e limitações em `v1/INTERPRETACAO.md`. A versão não está pronta para entrega final: enriquecimento socioeconômico, outras respostas de negócio, prints reais, apresentação e vídeo continuam pendentes.

Verificação: **14 testes aprovados**, incluindo contrato, fontes, datas, integridade do snapshot, grupos sem sobreposição, preparação sem ajuste fora do treino, permutação de atributo constante e execução integrada com fixture artificial. Os testes artificiais verificam o software; as métricas em `v1/` vêm exclusivamente do experimento real.

SQL, metadados reduzidos de jobs e hash do snapshot estão em `evidence/`. O experimento verifica o hash antes do treinamento. Após o bloqueio inicial, houve autorização específica do usuário para a extração. Uma falha de codificação do Windows foi corrigida recuperando o resultado do mesmo job, sem repetir a consulta de extração.

## Prints reais: pendentes

A tentativa de captura via navegador foi interrompida porque o controle da interface não conseguiu determinar a URL com segurança. Nenhum print de console foi obtido. Os JSONs são evidência técnica e não substituem as capturas solicitadas pelo professor. Não há imagem simulada apresentada como print real.

## Versionamento

Branches locais de implementação e experimento criadas. O plano de publicação e integração por PR está em `../docs/GIT_WORKFLOW.md`. Nenhum push, PR remoto ou integração à main foi realizado nesta etapa.

## Extração realizada

Origem: tabelas do projeto GCP da Fase 2 e população pública do IBGE.

Destino: arquivo Parquet local em `data/raw/alunos_gold_modelagem.parquet`, ignorado pelo Git.

Conteúdo: 92.389 registros (aproximadamente 5% dos alunos válidos de 2024), com identificador de linha em hash, classificação alfabetizado/não alfabetizado convertida para risco, município, rede e série; contexto municipal da Gold 2023 e população de 2022. Não exporta nomes, ID bruto do aluno/escola, proficiência individual ou credenciais. Mesmo pseudonimizados, são registros individuais educacionais.

Finalidade: treinar e avaliar a pipeline local. Nenhum upload ou publicação de microdados está previsto. A auditoria de rótulos passou sem divergências entre os casos válidos.
