# Visualizações

`python -m src.run` gera os gráficos de EDA, comparação na validação, matriz de confusão, curvas PR/ROC, calibração e importância por permutação em `images/v1/`. A primeira execução real está disponível nessa pasta. Os gráficos de EDA usam somente o treino.

`python scripts/analyze_validation.py` refaz a importância e produz a tabela exploratória de capacidade usando somente a validação, sem treinar novamente o modelo ou avaliar o teste.
