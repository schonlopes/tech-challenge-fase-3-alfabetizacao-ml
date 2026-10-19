# Auditoria inicial no GCP

Consulta somente leitura em 19/10/2026, projeto `tech-challenge-fase-2-506814`.

Confirmados 3.868.000 registros em `alfabetizacao_silver.alunos`:

| Ano | Presença / rótulo Silver | Registros | Sem proficiência |
| --- | --- | ---: | ---: |
| 2023 | Ausente / Nao | 244381 | 244381 |
| 2023 | Presente / Nao | 625631 | 249 |
| 2023 | Presente / Sim | 877427 | 0 |
| 2024 | Ausente / Nao | 267772 | 267772 |
| 2024 | Presente / Nao | 745669 | 936 |
| 2024 | Presente / Sim | 1107119 | 0 |
| 2026 | Presente / Nao, origem Pub/Sub | 1 | 0 |

A Gold possui cinco produtos: indicador municipal, evolução municipal, meta/resultado municipal, resumo por UF e monitoramento do stream. Nenhum é uma tabela individual de treinamento.

O SQL Silver da Fase 2 converte valores diferentes de Sim para Nao no rótulo; portanto, nem todo Nao é um desfecho válido observado. A primeira versão deverá excluir ausentes e proficiência nula, auditar rótulo versus corte de 743 e excluir Pub/Sub. Os resultados desta auditoria não alteram nem reexecutam a Fase 2.
