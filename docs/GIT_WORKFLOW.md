# Versionamento e publicação futura

O desenvolvimento desta Fase 3 tem um repositório Git próprio. Os commits são feitos conforme o trabalho acontece, sem reconstrução artificial de histórico.

## Ramos locais

| Branch | Finalidade | Integração futura |
| --- | --- | --- |
| `main` | Escopo, auditoria inicial e documentação de partida | Base principal |
| `feat/individual-risk-baseline` | Código da pipeline, testes, correções de extração e protocolo de validação | PR 1 para `main` |
| `feat/real-data-experiment` | Proveniência dos dados, resultados reais, gráficos e interpretação do primeiro experimento | PR 2 para `main`, depois da integração da PR 1 |
| `feat/socioeconomic-territorial-analysis` | Enriquecimento, compatibilidade de redes, perfis, metas, SHAP e prints reais | PR 3 para `main`, depois da integração da PR 2 |

A segunda branch foi criada a partir da primeira, e a terceira a partir da segunda. As dependências serão integradas nessa ordem. Os commits de implementação permanecerão acessíveis no histórico. Novos enriquecimentos e análises devem utilizar outras branches a partir da base adequada, com PRs que expliquem as respectivas decisões.

## PRs futuras

1. Publicar `main` e a branch de implementação no repositório da Fase 3.
2. Abrir PR da implementação com objetivo, decisões sobre vazamento e validação, testes e limitações.
3. Revisar e integrar a primeira PR preservando o histórico de commits.
4. Publicar a branch do experimento, conferir o diff contra a `main` atualizada e abrir a segunda PR com evidências e resultados reais.
5. Publicar a terceira branch e abrir a PR de enriquecimento e análise territorial após integrar a segunda.
6. Para cada nova mudança, registrar revisão e justificativas pertinentes. Não fabricar comentários, aprovações, colaboração ou cronologia.

As PRs acima são **planejadas**, não foram criadas. Nenhum envio ao GitHub foi realizado nesta etapa.

Foi preparado um workflow para testes, compilação e conferência do repositório em push/PR, sem credenciais GCP ou extração de microdados. A execução remota desse workflow só poderá ser comprovada após a publicação. As ações seguem os exemplos oficiais de [checkout](https://github.com/actions/checkout) e [setup-python](https://github.com/actions/setup-python).

## O que versionar

Código, SQL, documentação, versões de dependências, testes, relatórios agregados, gráficos e registros reduzidos dos jobs. Conferir o conteúdo antes do push.

## O que manter somente local

Snapshots com registros individuais, IDs pseudonimizados de linhas, modelos serializados, ambientes virtuais, arquivos de credenciais e resultados privados. As pastas correspondentes estão no `.gitignore`. Evitar `git add -A` sem conferir o diff e os arquivos adicionados.

## Conferência antes do envio

`git status`, `git diff --cached --stat`, revisão do conteúdo adicionado, testes e confirmação de que `data/raw`, `data/processed`, `.venv` e `models` continuam fora do índice. A criação e a integração das PRs precisam refletir o que efetivamente aconteceu.
