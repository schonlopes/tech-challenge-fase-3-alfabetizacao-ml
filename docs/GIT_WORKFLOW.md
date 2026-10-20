# Versionamento e integração

O projeto utiliza um repositório Git próprio. Os commits registram a evolução do código, dos experimentos e da documentação técnica.

## Branches de desenvolvimento

| Branch | Finalidade | Ordem de integração |
| --- | --- | --- |
| `main` | Escopo, auditoria inicial e documentação de partida | Base principal |
| `feat/individual-risk-baseline` | Código da pipeline, testes, correções de extração e protocolo de validação | PR 1 para `main` |
| `feat/real-data-experiment` | Proveniência dos dados, resultados reais, gráficos e interpretação do primeiro experimento | PR 2 para `main`, depois da integração da PR 1 |
| `feat/socioeconomic-territorial-analysis` | Enriquecimento, compatibilidade de redes, perfis, metas, SHAP e prints reais | PR 3 para `main`, depois da integração da PR 2 |
| `feat/reproducible-inference` | Política de decisão explícita, demo sem nuvem, previsão e execuções isoladas | PR 4 para `main`, depois da integração da PR 3 |
| `feat/executive-presentation` | Slides executivos, gráficos, evidência GCP e roteiro de até cinco minutos | PR 5 para `main`, depois da integração da PR 4 |

A segunda branch foi criada a partir da primeira, a terceira a partir da segunda, a quarta a partir da terceira e a quinta a partir da quarta. As dependências seguem essa ordem de integração. Os commits de implementação permanecem acessíveis no histórico. Novos enriquecimentos e análises devem utilizar outras branches a partir da base adequada, com PRs que expliquem as respectivas decisões.

## Procedimento de integração

1. Publicar `main` e a branch de implementação no repositório da Fase 3.
2. Abrir PR da implementação com objetivo, decisões sobre vazamento e validação, testes e limitações.
3. Revisar e integrar a primeira PR preservando o histórico de commits.
4. Publicar a branch do experimento, conferir o diff contra a `main` atualizada e abrir a segunda PR com evidências e resultados reais.
5. Publicar a terceira branch e abrir a PR de enriquecimento e análise territorial após integrar a segunda.
6. Publicar a quarta branch e abrir a PR de reprodução/previsão após integrar a terceira.
7. Publicar a quinta branch e abrir a PR dos materiais executivos após integrar a quarta. Conferir a versão dos slides e a gravação antes da entrega.
8. Registrar em cada PR o objetivo, as decisões técnicas, os testes e as limitações das alterações.

As PRs e suas integrações devem ser verificadas no histórico do repositório remoto. A tabela descreve a organização das mudanças e não substitui os registros de revisão e merge do GitHub.

O workflow executa testes, compilação e conferência do repositório em push/PR, sem credenciais GCP ou extração de microdados. A execução remota deve ser verificada na seção Actions do GitHub. As ações seguem os exemplos oficiais de [checkout](https://github.com/actions/checkout) e [setup-python](https://github.com/actions/setup-python).

## O que versionar

Código, SQL, documentação, versões de dependências, testes, relatórios agregados, gráficos e registros reduzidos dos jobs. Conferir o conteúdo antes do push.

## O que manter somente local

Snapshots com registros individuais, IDs pseudonimizados de linhas, modelos serializados, ambientes virtuais, arquivos de credenciais e resultados privados, incluindo `runs/`. As pastas correspondentes estão no `.gitignore`. Evitar `git add -A` sem conferir o diff e os arquivos adicionados.

## Conferência antes do envio

`git status`, `git diff --cached --stat`, revisão do conteúdo adicionado, testes e confirmação de que `data/raw`, `data/processed`, `.venv` e `models` continuam fora do índice. A criação e a integração das PRs precisam refletir o que efetivamente aconteceu.
