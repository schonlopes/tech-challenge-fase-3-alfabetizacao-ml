# Fontes, datas e interpretação dos atributos

| Fonte | Referência usada | Uso e limite |
| --- | --- | --- |
| Silver alunos da Fase 2 | 2024 | Alvo individual, rede e série; casos válidos, sem proficiência como entrada |
| Gold indicador municipal | 2023 | Contexto preditivo histórico; não resultado contemporâneo |
| IBGE população | 2022 | Contexto demográfico municipal |
| IPEA Atlas de Vulnerabilidade Social | 2010, totais municipais | Renda, desigualdade, vulnerabilidade e infraestrutura históricas; não diagnóstico atual |
| IBGE PIB municipal | 2021 | Economia e composição setorial; não renda disponível das famílias |
| Gold municipal e metas | 2023/2024; metas 2024/2025/2030 | Diagnóstico e cenários agregados; não atributos do classificador |
| Gold UF e metas nacionais | Anos de resultado explícitos na fonte | Agregados oficiais, sem substituir o Brasil por média simples de municípios |

## Fontes primárias consultadas em 19/10/2026

- [IPEA AVS no catálogo da Base dos Dados](https://basedosdados.org/dataset/1dd6317a-8e79-4a67-bb78-bc5fef214b4d): cobertura histórica 2000-2010; o esquema do BigQuery e o perfil de dimensões fundamentam a seleção de 2010 e totais por sexo, raça e localização, unidade geral.
- [Inep: Avaliação da Alfabetização](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao): primeira divulgação do indicador em maio de 2024. Assim, ano de referência 2023 não implica disponibilidade no início de 2024.
- [Inep: resultados e atualizações](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao/resultados): a página registra revisões posteriores. O snapshot atual não garante valores idênticos aos publicados originalmente.
- [IBGE: divulgação econômica de dezembro de 2023](https://agenciadenoticias.ibge.gov.br/agencia-noticias.html?ano=2023&editoria=economicas&mes=12): divulgação do PIB municipal de 2021 em 15/12/2023.
- Dicionário público `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`, consultado por job registrado em `reports/evidence/network_dictionary_job.json`, para os códigos de rede.

## Limite da reprodução histórica

O estudo usa referências anteriores ao desfecho, mas snapshots extraídos em 2026. Para afirmar previsão operacional que teria sido possível em uma data específica de 2024, seria necessário reconstruir as versões e as datas de acesso disponíveis naquele momento. Por isso, o projeto permanece identificado como retrospectivo.

As metas atuais podem conter atualizações de snapshots mais recentes; sua análise é diagnóstica. Cenários para 2025 partindo de 2024 são uma simulação retrospectiva, não uma previsão de futuro feita em 2026. Os cenários de 2030 são hipóteses de persistência/ganho constante, não resultados de um modelo temporal validado nesse horizonte.

## Qualidade econômica

Na fonte extraída, Cachoeira Dourada (5204250) apresenta razões setoriais de aproximadamente -0,257 e 2,096. O código não as considera proporções válidas de composição; mantém os valores originais na auditoria e trata esses atributos como ausentes, com imputação aprendida no treino. Não presume que todo o registro econômico ou município esteja incorreto, nem altera a fonte original.
