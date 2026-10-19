-- Keep the reference year: national base-year results are not current-year outcomes.
WITH state_targets AS (
  SELECT * FROM `__PROJECT__.alfabetizacao_silver.meta_alfabetizacao_uf`
  QUALIFY ROW_NUMBER() OVER(PARTITION BY sigla_uf,rede ORDER BY ano DESC)=1
)
SELECT 'Brasil' AS abrangencia, b.ano AS ano_resultado, 'BR' AS sigla_uf, b.rede,
  b.taxa_alfabetizacao AS resultado, b.meta_alfabetizacao_2024 AS meta_2024,
  b.meta_alfabetizacao_2025 AS meta_2025, b.meta_alfabetizacao_2030 AS meta_2030
FROM `__PROJECT__.alfabetizacao_silver.meta_alfabetizacao_brasil` b
UNION ALL
SELECT 'UF', g.ano, g.sigla_uf,g.rede,g.taxa_alfabetizacao,
  t.meta_alfabetizacao_2024,t.meta_alfabetizacao_2025,t.meta_alfabetizacao_2030
FROM `__PROJECT__.alfabetizacao_gold.resumo_uf` g
LEFT JOIN state_targets t ON g.sigla_uf=t.sigla_uf AND g.rede=t.rede
WHERE g.ano IN (2023,2024)
