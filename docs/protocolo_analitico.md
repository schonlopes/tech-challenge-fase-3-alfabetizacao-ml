# Protocolo analítico v1

## Pergunta e população

Estimar P(não alfabetizado) para alunos avaliados em 2024, usando rede/série, contexto territorial, indicador municipal de 2023 e população municipal de 2022. Classe positiva = 1 = não alfabetizado. Excluir ausentes, proficiência ausente e origem simulada. A proficiência é utilizada somente para auditar a coerência do rótulo e nunca como preditor.

Trata-se de uma avaliação retrospectiva com separação territorial: treino, validação e teste são subconjuntos de municípios de 2024. Não demonstra generalização temporal para 2025. A disponibilidade efetiva do indicador de 2023 antes do momento de previsão de 2024 precisa ser verificada; até lá, chamar de estudo retrospectivo condicionado à disponibilidade do contexto histórico.

## Vazamento e validade

- Allowlist explícita de atributos; excluir ID de aluno/escola/município, proficiência, rótulo, presença, preenchimento de caderno, peso amostral, resultado contemporâneo municipal e derivações do alvo.
- Código de município é usado exclusivamente nas junções, nos agrupamentos e na separação territorial.
- Cada município pertence a um único conjunto, definido por SHA-256: 60% dos buckets para treino, 20% para validação e 20% para teste. Percentuais de alunos podem diferir.
- Pré-processamento ajustado dentro de cada fold do treino. Busca com GroupKFold por município. Comparação de candidatos e limiar somente na validação. O teste final é reservado ao candidato selecionado e ao baseline de referência.
- Alunos de 2023 não são usados como exemplos de treinamento nesta versão: não há contexto Gold de 2022 confirmado. A Gold 2023 serve como contexto histórico dos exemplos de 2024.
- A seleção é uma amostra determinística de aproximadamente 5% dos alunos elegíveis, pelo hash de ano e identificador. Não é um LIMIT de primeiras linhas. Não garante representatividade e não substitui desenho/peso amostral oficial.
- Não fazer inferência causal a partir de importância de variáveis.

## Métricas e escolha

Comparar DummyClassifier, baseline histórico municipal, regressão logística e Random Forest. Selecionar por average precision (área PR) na validação. Ajustar limiar no mesmo conjunto buscando o melhor F2 (maior peso para recall), sem interpretar isso como política ótima de alocação. Medir também recall, precisão, F1, ROC-AUC, Brier e matriz de confusão. Comparar com a prevalência do risco. Reportar incerteza por bootstrap de municípios e resultados por UF para o modelo escolhido.

Antes da primeira avaliação real: explorar o alvo somente no treino. Na avaliação final, medir também os dois baselines pré-definidos (Dummy e histórico) para permitir interpretar o ganho sobre a regra contextual simples. Essa comparação não altera a escolha do modelo, que já foi feita na validação. O snapshot padrão deve corresponder ao hash do manifest de extração.

As análises municipais do teste se referem à amostra avaliada. Não comparar diretamente probabilidades não ponderadas da amostra com metas oficiais, nem chamar isso de previsão validada de cumprimento de metas futuras.

## Evidências

Guardar SQL, SHA-256 do snapshot, número do job, bytes processados/faturados, perfil da fonte e metadados de execução. Os prints reais do console GCP ainda devem ser capturados e vinculados às evidências. Arquivos JSON de jobs não substituem prints. Não publicar microdados ou identificadores individuais no Git.

## Pendências além da v1

Enriquecimento socioeconômico propriamente dito (população não equivale a renda, vulnerabilidade ou infraestrutura); metas nacionais/estaduais em uma análise sem vazamento; segmentação de municípios; cenário temporal de metas futuras com histórico suficiente; SHAP se acrescentar valor além de importância por permutação; prints reais; apresentação e vídeo executivo; PRs reais no repositório remoto.
