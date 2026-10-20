SELECT 'municipal_gold' AS fonte, rede, COUNT(*) AS registros
FROM `__PROJECT__.alfabetizacao_gold.indicador_municipio` GROUP BY rede
UNION ALL
SELECT 'municipal_targets', rede, COUNT(*)
FROM `__PROJECT__.alfabetizacao_gold.meta_resultado_municipio` GROUP BY rede
UNION ALL
SELECT 'state_targets', rede, COUNT(*)
FROM `__PROJECT__.alfabetizacao_silver.meta_alfabetizacao_uf` GROUP BY rede
