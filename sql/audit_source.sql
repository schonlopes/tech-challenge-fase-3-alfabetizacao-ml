SELECT
  ano, _source AS origem, presenca, alfabetizado,
  COUNT(*) AS registros,
  COUNTIF(proficiencia IS NULL) AS sem_proficiencia,
  COUNTIF(presenca = 'Presente' AND proficiencia IS NOT NULL) AS elegiveis,
  COUNTIF(presenca = 'Presente' AND proficiencia IS NOT NULL
    AND ((alfabetizado = 'Sim') != (proficiencia >= 743))) AS divergencias_rotulo
FROM `__PROJECT__.alfabetizacao_silver.alunos`
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
