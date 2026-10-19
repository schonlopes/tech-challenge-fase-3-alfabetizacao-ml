# Estado do projeto - 19/10/2026

Extração autorizada e concluída: 92.389 registros válidos de alunos de 2024, distribuídos por 5.193 municípios. O snapshot está somente local, ignorado pelo Git. A amostra integra Silver individual, Gold municipal de 2023 e população IBGE de 2022. Não houve criação ou alteração de tabelas cloud nesta etapa.

O experimento inicial selecionou regressão logística. A segunda versão testou contexto socioeconômico, mas não superou o modelo anterior na validação. Seus municípios de teste foram excluídos do novo desenvolvimento. Há SHAP global, dois perfis territoriais, análise de metas e cenários com limites explícitos. Relatórios em `v1/`, `v2/` e `territorial/`.

Verificação: **36 testes aprovados**, incluindo contratos, integridade, grupos sem sobreposição, preparação sem vazamento, enriquecimento, metas ausentes, cenários, backtest, agregação de SHAP, previsão sem refit, recarga do artefato, isolamento de saídas e demo sem nuvem. Os testes artificiais verificam o software; os relatórios de resultados usam dados reais e distinguem validação e teste.

SQL, metadados reduzidos de jobs e hash do snapshot estão em `evidence/`. O experimento verifica o hash antes do treinamento. Após o bloqueio inicial, houve autorização específica do usuário para a extração. Uma falha de codificação do Windows foi corrigida recuperando o resultado do mesmo job, sem repetir a consulta de extração.

## Prints reais: concluídos

A primeira tentativa foi interrompida por limitação do controle da interface. Nesta etapa, o acesso pelo navegador à conta correta funcionou: cinco prints reais foram salvos e catalogados em `evidence/GCP_SCREENSHOTS.md`. Mostram tabela, particionamento e execução concluída de consulta. O treinamento de ML foi local. Uma captura adicional com dados da conta permanece privada e ignorada pelo Git.

## Versionamento

Quatro branches locais de desenvolvimento criadas. A quarta, `feat/reproducible-inference`, contém as melhorias de engenharia e a política explícita do modelo. O plano de publicação e integração por PR está em `../docs/GIT_WORKFLOW.md`. Nenhum push, PR remoto ou integração à main foi realizado nesta etapa.

## Melhorias de engenharia

A logística original permanece a referência; escores são o padrão da ferramenta, sem alerta automático. Os limiares F2 histórico e de capacidade exploratória estão separados em [modelo e política](../docs/modelo_e_politica.md). Há demo artificial completa sem conta GCP, previsão CSV/Parquet por artefato confiável e manifests por execução. Novas saídas analíticas ficam em `runs/`, ignoradas pelo Git; os relatórios históricos não foram substituídos.

Foi conferida a equivalência exata entre a previsão direta da pipeline real v1 e a nova função de previsão nos 76.666 registros locais de desenvolvimento (treino/validação). Não houve novo treinamento, nova consulta cloud ou reavaliação do teste real. Essa checagem é de software, não uma nova estimativa de desempenho.

Uma cópia somente dos arquivos versionados, sem snapshots/modelos reais, também passou nos 36 testes e na demonstração/previsão. Foi usado o mesmo ambiente de dependências, não uma instalação independente. [Resumo da verificação de engenharia](VERIFICACAO_ENGENHARIA.md).

## Pendências de entrega

Revisão final, apresentação e roteiro executivo, gravação de vídeo de até cinco minutos e publicação do GitHub por PRs. A matriz de critérios está em `../docs/atendimento_requisitos.md`.

## Extração realizada

Origem: tabelas do projeto GCP da Fase 2 e população pública do IBGE.

Destino: arquivo Parquet local em `data/raw/alunos_gold_modelagem.parquet`, ignorado pelo Git.

Conteúdo: 92.389 registros (aproximadamente 5% dos alunos válidos de 2024), com identificador de linha em hash, classificação alfabetizado/não alfabetizado convertida para risco, município, rede e série; contexto municipal da Gold 2023 e população de 2022. Não exporta nomes, ID bruto do aluno/escola, proficiência individual ou credenciais. Mesmo pseudonimizados, são registros individuais educacionais.

Finalidade: treinar e avaliar a pipeline local. Nenhum upload ou publicação de microdados está previsto. A auditoria de rótulos passou sem divergências entre os casos válidos.
