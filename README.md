# Predição e inteligência analítica para alfabetização no Brasil

Tech Challenge da Fase 3. Projeto em desenvolvimento local, a partir da infraestrutura e da Gold da Fase 2.

## Problema e objetivo

Antecipar risco educacional para apoiar a priorização de acompanhamento pedagógico. O objetivo principal é classificação individual de alfabetização, acompanhada de análises territoriais. As previsões são apoio à decisão humana, não decisões automáticas sobre alunos.

## Estado atual

Auditoria de dados reais no GCP e preparação da primeira versão reproduzível. Resultados publicados nesta pasta serão identificados por versão e origem; amostras sintéticas da Fase 2 e eventos simulados de Pub/Sub não serão utilizados para avaliar os modelos.

## Origem e limite da base

A Gold da Fase 2 é municipal. Para cumprir a unidade individual do enunciado, a Fase 3 cria uma **extensão Gold de modelagem local**, integrando alunos válidos da Silver com contexto histórico municipal da Gold. Não confundir essa extensão com uma tabela individual já existente na Gold da Fase 2.

Os microdados têm poucos atributos individuais. O primeiro modelo será, principalmente, um estimador de risco contextual; não deve ser apresentado como diagnóstico individual completo. Ausência de avaliação não é evidência de não alfabetização.

## Desenvolvimento

O protocolo e os requisitos estão em `docs/`. Scripts executáveis e instruções serão acrescentados nos commits de implementação. A publicação no GitHub e as PRs serão feitas em etapa posterior, preservando o histórico real de desenvolvimento.
