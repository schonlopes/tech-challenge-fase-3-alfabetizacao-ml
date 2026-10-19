# Roteiro do vídeo executivo - Fase 3

Meta de gravação: **4min45s**, com 15 segundos de margem até o limite de cinco minutos.
O tempo é estimado, não cronometrado por uma gravação real. Ensaiar antes de gravar.
O PDF móvel usa fonte de 24 pontos. Continuação de página não significa trocar de slide.

## Slide 1 - Predição e inteligência analítica para alfabetização

Tempo: 00:00 a 00:18 (18 segundos).

Olá, sou Willian Schön Lopes. Neste projeto, utilizei os dados de alfabetização para estimar risco educacional e analisar diferenças entre municípios. A proposta é apoiar gestores na organização do acompanhamento pedagógico e no planejamento de políticas públicas, com evidências e limites explícitos.

## Slide 2 - Base individual com contexto histórico

Tempo: 00:18 a 00:56 (38 segundos).

O desafio principal é classificar se um aluno foi considerado alfabetizado ou não. Como a Gold da fase anterior era municipal, construí uma extensão local de modelagem, integrando os alunos válidos da Silver ao contexto histórico da Gold. A amostra contém cerca de 92 mil alunos de 2024, em mais de cinco mil municípios. Utilizei o indicador municipal de 2023 e a população de 2022. Excluí ausentes e registros sem proficiência válida. A proficiência individual não entra como variável preditora.

## Slide 3 - Validação com municípios separados

Tempo: 00:56 a 01:38 (42 segundos).

A separação entre treino, validação e teste mantém cada município em um único conjunto, reduzindo o vazamento territorial. A pipeline integra imputação por mediana, transformação da população, padronização e codificação das categorias. Comparei referências simples, regressão logística e floresta aleatória. A busca de hiperparâmetros usa validação cruzada por município apenas no treino. Escolhi o modelo na validação e preservei o teste para a avaliação original. Essa separação mede generalização territorial em 2024, mas ainda não comprova previsão para anos futuros.

## Slide 4 - Desempenho e escolha do modelo

Tempo: 01:38 a 02:20 (42 segundos).

A regressão logística foi a referência selecionada. No teste, sua precisão média, ou average precision, foi de aproximadamente zero vírgula cinquenta e três, contra zero vírgula cinquenta e um do indicador histórico. A área sob a curva ROC foi de zero vírgula sessenta e seis. O ganho observado é modesto e não significa cinquenta e três por cento de acurácia. Depois, acrescentei contexto socioeconômico e econômico. Como não houve melhora na validação, mantive o modelo mais simples, sem reutilizar o teste para essa escolha.

## Slide 5 - Risco contextual e limites da priorização

Tempo: 02:20 a 03:03 (43 segundos).

A análise SHAP mostra que o histórico municipal tem maior influência nas previsões, seguido pela localização. Isso reforça que o modelo estima principalmente risco contextual e não explica causalidade. Também há uma limitação operacional importante: o limiar que busca alto recall sinaliza quase 96 por cento dos alunos. Portanto, não oferece uma priorização seletiva. A alternativa de sinalizar cerca de 20 por cento foi explorada somente na validação. Por isso, a ferramenta entrega escores por padrão e mantém qualquer decisão pedagógica sob responsabilidade humana.

## Slide 6 - Perfis territoriais e metas

Tempo: 03:03 a 03:48 (45 segundos).

Na análise territorial, identifiquei dois perfis entre mais de cinco mil municípios, sem utilizar alfabetização para formar os grupos. Depois, observei médias municipais de alfabetização próximas de 67 e 58 por cento. São médias não ponderadas e associações, não efeitos causais. O contexto social utilizado é de 2010, o que limita sua atualização. Além disso, 2.444 dos 5.232 municípios com dados comparáveis ficaram abaixo da meta de 2024. Os cenários até 2030 ajudam a discutir o avanço necessário, mas não são previsões estatisticamente validadas.

## Slide 7 - Execução comprovada e reprodução

Tempo: 03:48 a 04:20 (32 segundos).

Esta captura mostra uma consulta realmente concluída no BigQuery, com processamento e limite de consumo registrados. Os dados e as consultas ficam no GCP, enquanto o treinamento ocorreu localmente. O projeto conta com 36 testes aprovados, demonstração artificial sem credenciais e previsão com o modelo salvo. Cada execução preserva parâmetros, versões e hashes. O histórico de commits e as branches locais documentam a evolução, sem publicar os registros individuais dos alunos.

## Slide 8 - Apoio ao planejamento educacional

Tempo: 04:20 a 04:45 (25 segundos).

O valor estratégico está em combinar acompanhamento pedagógico com planejamento territorial e monitoramento de metas. A solução oferece uma base auditável para discutir onde aprofundar diagnósticos e como distribuir apoio. Antes do uso operacional, precisamos atualizar o contexto, avaliar uma nova coorte e pactuar critérios com os educadores. A tecnologia apoia a decisão pública, preservando a avaliação humana. Obrigado.

## Orientações para gravação

- Use a apresentação em tela cheia e mantenha o roteiro no celular próximo à câmera.
- Desative notificações e teste o áudio antes de iniciar.
- Não leia as notas de fonte, os rodapés ou os números dos slides.
- AP: fale "precisão média". ROC-AUC: "área sob a curva ROC". SHAP: "shép".
- Gold: "gôuld". Silver: "sílver". GroupKFold: "validação cruzada por município".
- Prefira os arredondamentos já escritos no roteiro para não alongar a fala.
- A captura do GCP é real, mas não representa treinamento na nuvem.
- Antes da entrega, concluir a publicação e as PRs e confirmar os links do vídeo e repositório.
- Se o ensaio ultrapassar cinco minutos, reduzir a fala antes de gravar. Não acelerar a ponto de prejudicar a compreensão.
