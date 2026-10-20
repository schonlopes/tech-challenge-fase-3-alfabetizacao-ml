-- Descriptive official municipal indicators and targets, never model inputs in this version.
SELECT m.ano, m.id_municipio, m.nome_municipio, m.sigla_uf, m.regiao,
  m.rede, m.serie, m.taxa_alfabetizacao,
  t24.meta AS meta_2024, t25.meta AS meta_2025, t30.meta AS meta_2030
FROM `__PROJECT__.alfabetizacao_gold.indicador_municipio` m
LEFT JOIN `__PROJECT__.alfabetizacao_gold.meta_resultado_municipio` t24
  ON m.id_municipio=t24.id_municipio AND m.rede=CASE LOWER(TRIM(t24.rede)) WHEN 'municipal' THEN '3' ELSE TRIM(t24.rede) END AND t24.ano_meta=2024
LEFT JOIN `__PROJECT__.alfabetizacao_gold.meta_resultado_municipio` t25
  ON m.id_municipio=t25.id_municipio AND m.rede=CASE LOWER(TRIM(t25.rede)) WHEN 'municipal' THEN '3' ELSE TRIM(t25.rede) END AND t25.ano_meta=2025
LEFT JOIN `__PROJECT__.alfabetizacao_gold.meta_resultado_municipio` t30
  ON m.id_municipio=t30.id_municipio AND m.rede=CASE LOWER(TRIM(t30.rede)) WHEN 'municipal' THEN '3' ELSE TRIM(t30.rede) END AND t30.ano_meta=2030
WHERE m.ano IN (2023,2024)
ORDER BY ano,id_municipio,rede,serie
