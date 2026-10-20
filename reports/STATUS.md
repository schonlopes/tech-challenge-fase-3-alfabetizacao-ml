# Síntese técnica do projeto

## Base analítica

A amostra contém 92.389 alunos válidos de 2024, distribuídos por 5.193 municípios. A extensão Gold de modelagem integra registros individuais da Silver, contexto municipal da Gold de 2023 e população IBGE de 2022. O snapshot individual permanece privado e fora do Git.

SQL, hashes, contagens e metadados de consultas estão em `evidence/`. Cinco capturas reais do console GCP comprovam tabelas e consultas. O treinamento dos modelos ocorre localmente.

## Modelagem e análise territorial

A regressão logística original é o modelo de referência. O enriquecimento socioeconômico não melhorou o desempenho observado na validação. Os municípios do teste v1 foram excluídos do desenvolvimento v2.

Os relatórios incluem métricas, bootstrap por município, recortes por UF, permutação, SHAP global, perfis municipais, comparação de metas e cenários. As limitações de atualização do contexto, generalização temporal e uso operacional estão explicitadas nas interpretações.

## Qualidade e reprodução

Os 36 testes verificam contratos, separação de grupos, prevenção de vazamento, enriquecimento, metas ausentes, cenários, backtest, SHAP, serialização, inferência e isolamento de execuções. As demonstrações artificiais verificam o software e não representam desempenho educacional.

As previsões da ferramenta e da pipeline original foram idênticas nos 76.666 registros locais de desenvolvimento utilizados na conferência. Os resultados históricos foram preservados. Cada nova execução registra parâmetros, dependências, hashes e versão do código.

[Verificação de engenharia](VERIFICACAO_ENGENHARIA.md) e [revisão da entrega](REVISAO_FINAL.md).

## Materiais executivos

O vídeo tem aproximadamente 4min52s, dentro do limite de cinco minutos. A apresentação contém oito slides, com resultados, limitações e evidência real do GCP. Os materiais estão em `output/`, e o roteiro em `docs/roteiro_video.md`.

## Versionamento e privacidade

As branches separam implementação, experimento real, enriquecimento territorial, inferência e apresentação. A política de integração está em [versionamento](../docs/GIT_WORKFLOW.md).

Não são versionados microdados, modelos serializados, ambientes virtuais, credenciais ou resultados individuais. Os relatórios públicos contêm métricas e agregados, sem identificação de alunos.
