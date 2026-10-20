# Roteiro do vídeo executivo - Fase 3

Meta de gravação: **4min45s**, com 15 segundos de margem até o limite de cinco minutos.
Versão enxuta após a gravação anterior de 5min15s, informada pelo usuário. O novo tempo ainda é estimado. Ensaiar antes de gravar.
O PDF móvel usa fonte de 24 pontos. Continuação de página não significa trocar de slide.

## Slide 1 - Predição e inteligência analítica para alfabetização

Tempo: 00:00 a 00:18 (18 segundos).

Olá, sou Willian Schön Lopes. Este projeto usa dados de alfabetização para estimar risco educacional e analisar diferenças municipais, apoiando o acompanhamento pedagógico e o planejamento de políticas públicas. O foco é transformar dados públicos em apoio à decisão dos gestores.

## Slide 2 - Base individual com contexto histórico

Tempo: 00:18 a 00:56 (38 segundos).

O objetivo é classificar se um aluno foi considerado alfabetizado ou não. Integrei os alunos válidos da Silver ao contexto municipal da Gold, criando uma extensão local de modelagem. A Gold original é municipal, por isso essa integração individual foi necessária. A amostra reúne cerca de 92 mil alunos de 2024, em mais de cinco mil municípios, com indicador de 2023 e população de 2022. Excluí ausentes e proficiência inválida. A proficiência individual não entra como preditora.

## Slide 3 - Validação com municípios separados

Tempo: 00:56 a 01:38 (42 segundos).

Mantive cada município em um único conjunto de treino, validação ou teste, reduzindo o vazamento territorial. A pipeline integra imputação por mediana, transformação da população, padronização e codificação das categorias. As transformações são ajustadas somente com os dados de treino. Comparei referências simples, regressão logística e floresta aleatória. A busca de hiperparâmetros usa validação cruzada por município somente no treino. Escolhi o modelo na validação. O teste mede generalização territorial em 2024, ainda sem comprovar previsão para anos futuros.

## Slide 4 - Desempenho e escolha do modelo

Tempo: 01:38 a 02:20 (42 segundos).

A logística foi selecionada. No teste, a precisão média foi de aproximadamente zero vírgula cinquenta e três, contra zero vírgula cinquenta e um do histórico. A área sob a curva ROC foi de zero vírgula sessenta e seis. O ganho é modesto, e precisão média não é acurácia. O enriquecimento socioeconômico não melhorou a validação. Mantive o modelo mais simples, sem reutilizar o teste.

## Slide 5 - Risco contextual e limites da priorização

Tempo: 02:20 a 03:03 (43 segundos).

O SHAP aponta o histórico municipal como maior influência, seguido pela localização. O modelo estima principalmente risco contextual, sem explicar causalidade. O limiar de alto recall sinaliza quase 96 por cento dos alunos e não oferece priorização seletiva. A alternativa de cerca de 20 por cento foi analisada apenas na validação, sem teste independente. Por isso, a ferramenta entrega escores por padrão, mantendo a decisão pedagógica sob responsabilidade humana.

## Slide 6 - Perfis territoriais e metas

Tempo: 03:03 a 03:48 (45 segundos).

Identifiquei dois perfis municipais sem usar alfabetização na formação dos grupos. Esses perfis ajudam a comparar municípios com características semelhantes. As médias municipais observadas ficaram próximas de 67 e 58 por cento. São médias não ponderadas, sem interpretação causal. O contexto social é de 2010, uma limitação importante. Entre os municípios com dados comparáveis, 2.444 de 5.232 ficaram abaixo da meta de 2024. Os cenários até 2030 apoiam a discussão do avanço necessário, mas não são previsões validadas.

## Slide 7 - Execução comprovada e reprodução

Tempo: 03:48 a 04:20 (32 segundos).

Esta captura comprova uma consulta concluída no BigQuery, com consumo controlado. Dados e consultas ficam no GCP, mas o treinamento foi local. Há 36 testes aprovados, demonstração artificial sem credenciais e previsão com modelo salvo. As execuções preservam versões e hashes. Commits e branches documentam a evolução, sem publicar os registros individuais.

## Slide 8 - Apoio ao planejamento educacional

Tempo: 04:20 a 04:45 (25 segundos).

A solução apoia o acompanhamento pedagógico, o planejamento territorial e o monitoramento de metas. Antes do uso operacional, precisamos atualizar o contexto, avaliar uma nova coorte e pactuar critérios com educadores. O valor está em oferecer uma base auditável para decisões públicas, preservando a avaliação humana. Obrigado.

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
