# Verificação local das melhorias de engenharia — 19/10/2026

Escopo: política explícita, demonstração sem conta cloud, previsão com artefato salvo e isolamento/rastreabilidade de execuções. Não constitui novo experimento de desempenho educacional.

## Conferências executadas

- **36 testes aprovados** no ambiente local Python 3.11, com dependências fixadas. Incluem execução integrada v1 artificial, ausência de municípios sobrepostos, previsão sem refit, recarga exata, contratos, categorias inéditas, separação de políticas e recusa de reutilização de pasta.
- A demonstração artificial e o comando de previsão foram executados separadamente, sem GCP. A entrada usada no segundo comando foi o CSV produzido pelo primeiro, verificando a passagem pelo formato de intercâmbio.
- Uma cópia exportada somente dos arquivos versionados no commit `e591323` também passou nos **36 testes**, na demonstração e na previsão. Não recebeu os snapshots, artefatos reais nem `.git`; reutilizou o mesmo interpretador e dependências instaladas. Isso verifica independência de arquivos privados, **não** uma instalação nova ou execução remota Linux.
- O modelo real v1 foi carregado para gerar escores nos **76.666 registros locais de desenvolvimento (treino/validação)**. A função nova e a chamada direta à pipeline deram probabilidades exatamente iguais. Sem novo treinamento, consulta cloud, cálculo de desempenho ou acesso ao teste real nessa checagem. As saídas individuais permaneceram em `runs/`, fora do Git.
- SHAP global foi reexecutado na validação em uma nova pasta: 500 observações explicadas, zero do teste, erro máximo de aditividade `4,44e-16`. Nenhuma explicação individual foi exportada.
- Compilação dos módulos concluída e `pip check` sem dependências quebradas.
- Conferência do repositório: índice sem arquivos privados, links existentes e cinco screenshots íntegros.
- Nenhuma alteração nos resultados históricos de `reports/v1`, `reports/v2`, `reports/territorial` ou respectivos gráficos, comparados ao commit anterior `ecc4cf9`.

## Evidências locais e privacidade

Os manifests de execução e os arquivos de teste manual ficam em `runs/`, com hashes, parâmetros, versão do código e indicação de conclusão. Não publicar essa pasta inteira: inclui escores e pode conter dados individuais ou modelos. O resumo acima é a evidência agregada para versionamento.

O workflow inclui a demonstração artificial, os testes e a conferência do repositório. A execução remota deve ser verificada na seção Actions do GitHub. As métricas científicas históricas permanecem preservadas.

## Limitações preservadas

Não houve nova coorte independente, atualização dos indicadores sociais de 2010, enriquecimento com atributos individuais adicionais ou teste pareado do ganho frente ao histórico. A política de capacidade continua exploratória de validação. Esses pontos não são resolvidos por uma melhoria de engenharia e não devem ser apresentados como concluídos.
