# Protocolo v2 - enriquecimento e análises territoriais

Definido antes do treinamento desta versão, em 19/10/2026.

## Proteção do teste observado

O teste v1 já foi avaliado e não constitui mais um teste cego para uma nova versão. Os seus municípios ficarão excluídos do desenvolvimento supervisionado v2. Não haverá novo score final v2 no teste v1 nem alegação de um novo teste independente.

Reutilizar o treino e a validação municipais v1 para comparação exploratória com e sem contexto socioeconômico, mantendo a separação dos municípios. Comparar regressão logística e Random Forest com espaços e semente pré-definidos; escolher pelo average precision da validação. Aplicar a regra operacional exploratória de no máximo 20% de alertas, respeitando empates. A escolha de 20% é ilustrativa, não capacidade real informada por gestor.

Os resultados v2 serão explicitamente de validação. O teste v1 continua documentado como evidência do modelo original. Uma alegação de desempenho final da nova versão dependerá de novos dados independentes. Aumentar métricas no teste observado não é objetivo deste desenvolvimento.

## Enriquecimento

Reutilizar o snapshot individual autorizado, sem nova extração de alunos. Baixar somente agregados públicos municipais:

- IPEA AVS, 2010: renda/trabalho, IDHM renda, Gini, vulnerabilidade, infraestrutura sanitária e escolaridade dos responsáveis. Filtrar total de raça, sexo e localização, e unidade `geral`, evitando multiplicar alunos por subgrupos.
- IBGE PIB municipal, 2021: log do PIB na unidade da fonte e participações da indústria e da administração no valor adicionado.

Não interpretar o PIB como renda disponível de famílias. Não usar os indicadores de 2010 como estimativas atuais. Os atributos serão imputados no treino dentro do pipeline. Verificar unicidade municipal antes de qualquer junção. O snapshot v1 permanece inalterado; a extensão v2 é local e tem manifest próprio.

## Análise não supervisionada

Formar perfis de municípios com base no contexto socioeconômico e tamanho populacional, sem resultado/risco/meta de alfabetização na formação dos grupos. K-Means com k de 2 a 6; padronização e imputação. Escolher k por silhouette, verificar estabilidade por Adjusted Rand Index entre sementes e usar PCA apenas para visualização. A formação usa municípios, cada um com peso igual, não linhas de alunos.

Depois da formação dos perfis, descrever seus indicadores municipais e lacunas de metas. Isso é análise exploratória de todos os municípios disponíveis, não avaliação do classificador. Não usar esses resultados para reajustar o teste supervisionado.

## Metas e tempo

Usar indicadores oficiais Gold para comparar resultados com metas, separando redes e anos. Não produzir indicador nacional como média simples de municípios. Para 2025 e 2030, construir cenários explícitos: persistência do resultado de 2024, manutenção do ganho 2023-2024 e avanço anual necessário. Não tratar dois pontos anuais como série suficiente para ARIMA ou previsão temporal validada. Não chamar cenário de ganho constante de predição causal ou promessa de desempenho.

Registrar faltantes, municípios sem meta, anos de referência e limites. As metas são descritivas/estratégicas; não entram como atributos no modelo de alunos.

Antes da análise adicional: avaliar uma referência temporal fixa de persistência (resultado municipal de 2023 como previsão de 2024), sem escolher parâmetros ou municípios pelo desempenho. Calcular MAE/RMSE em pontos percentuais e classificação de ficar abaixo da meta de 2024. Essa checagem retrospectiva de um único período não valida extrapolações para 2030 e não garante reprodução das versões disponíveis à época.

Uma observação econômica apresentou razões setoriais fora do intervalo interpretável de 0 a 1. Preservar o valor original para auditoria e marcar os dois atributos derivados como indisponíveis, sem truncá-los a extremos; a imputação continua dentro do pipeline. Não excluir o município ou imputar usando o alvo.

## Evidências e Git

Branch própria `feat/socioeconomic-territorial-analysis`. Preservar as versões e relatórios v1. Publicar futuramente por PR após as branches anteriores, conforme o encadeamento real de dependências. Registrar consultas, hashes, testes e limitações. Prints reais ainda serão necessários quando o controle seguro da interface estiver disponível.
