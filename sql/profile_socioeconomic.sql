SELECT ano, raca_cor, sexo, localizacao, udh, COUNT(*) AS rows_count
FROM `basedosdados.br_ipea_avs.municipio`
WHERE ano = 2010
GROUP BY 1,2,3,4,5
ORDER BY rows_count DESC
LIMIT 100
