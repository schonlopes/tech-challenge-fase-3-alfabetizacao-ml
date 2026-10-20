# Modelo de referência e política de decisão

## Decisão para a entrega

O **modelo de referência é a regressão logística original v1**, com os seis atributos originais e C=0,01. A comparação enriquecida não mostrou ganho observado na validação. A v2 reutilizou esse estimador; não é um novo modelo superior e não possui novo teste independente.

As métricas históricas permanecem em [experimento v1](../reports/v1/experiment.json). A comparação posterior está no [experimento v2](../reports/v2/experiment.json). Não selecionar novamente o modelo ou o limiar pelo desempenho no teste já observado.

## Separar estimador e decisão

| Uso | Regra | Evidência e limite |
| --- | --- | --- |
| Padrão da ferramenta de previsão | Somente probabilidade estimada de não alfabetização | Apoio analítico contextual; sem alerta automático, diagnóstico individual ou garantia de calibração em novas populações |
| Reprodução da política histórica v1 | Limiar F2 = 0,16, escolhido na validação | Avaliado no teste territorial de 2024: recall 99,07%, precisão 40,23% e 95,76% sinalizados; inadequado para alegar priorização seletiva |
| Alternativa experimental v2 | Limiar fixo ≈ 0,5102423842 | Aproximadamente 19,96% sinalizados na validação, precisão 60,11% e recall 30,09%; sem teste independente dessa política |

O limiar da v2 **não garante atender somente 20% de um novo lote**. A fração depende da distribuição de escores; empates podem inviabilizar uma fração exata. A ferramenta não recalcula limiares para forçar uma capacidade em dados novos. Isso exigiria outra política, declarada e avaliada separadamente.

Não há política aprovada para uso operacional com alunos. Antes de qualquer aplicação real: definir capacidade e consequências dos erros com educadores, verificar disponibilidade temporal dos atributos, proteção de dados, calibração e equidade, e avaliar em uma coorte independente. A decisão pedagógica continua humana; o escore não pode restringir direitos ou acesso a apoio.

## Artefatos e segurança

Os arquivos históricos locais são `models/risk_v1.joblib` e `models/risk_v2.joblib`. Novas execuções gravam seus próprios artefatos dentro de `runs/<id>/models`, sem substituir os históricos. A previsão exige informar o artefato explicitamente; não escolhe automaticamente o arquivo mais recente.

`python -m src.predict` exporta apenas o número sequencial da linha de entrada e o escore, preservando a ordem. A opção `--use-artifact-threshold` acrescenta `research_alert` e avisa sobre a limitação. O arquivo `reports/policy.json` da execução distingue evidência histórica, validação exploratória ou demonstração artificial.

**Joblib/pickle pode executar código ao carregar um arquivo.** Usar somente artefatos locais de origem confiável, com as dependências fixadas. Não carregar modelos recebidos de fontes desconhecidas.

Essas melhorias são de engenharia e clareza metodológica: não constituem novo resultado de desempenho real e não resolvem a antiguidade do contexto social ou a falta de atributos individuais.
