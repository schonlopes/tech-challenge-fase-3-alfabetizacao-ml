-- Retrospective study: 2024 students, municipal context from 2023 and population 2022.
-- No cloud table is created or modified. Gold modeling extension is stored locally.
WITH population AS (
  SELECT id_municipio, populacao
  FROM `basedosdados.br_ibge_populacao.municipio`
  WHERE ano = 2022
), history AS (
  SELECT id_municipio, rede, serie, sigla_uf, regiao, nome_municipio,
         taxa_alfabetizacao AS taxa_municipal_anterior
  FROM `__PROJECT__.alfabetizacao_gold.indicador_municipio`
  WHERE ano = 2023
)
SELECT
  TO_HEX(SHA256(TO_JSON_STRING(STRUCT(a.ano, a.id_aluno)))) AS row_id,
  a.ano, a.id_municipio, a.rede, a.serie,
  -- Geography for municipalities without Gold historical result.
  d.sigla_uf, d.regiao, d.nome_municipio,
  2023 AS ano_contexto, h.taxa_municipal_anterior,
  2022 AS ano_populacao, p.populacao AS populacao_anterior,
  CASE WHEN a.alfabetizado = 'Nao' THEN 1 ELSE 0 END AS risco,
  a._source AS origem
FROM `__PROJECT__.alfabetizacao_silver.alunos` a
LEFT JOIN history h
  ON a.id_municipio = h.id_municipio AND a.rede = h.rede AND a.serie = h.serie
LEFT JOIN `__PROJECT__.alfabetizacao_silver.dim_municipio` d
  ON a.id_municipio = d.id_municipio
LEFT JOIN population p ON a.id_municipio = p.id_municipio
WHERE a.ano = 2024
  AND a._source = 'basedosdados.br_inep_avaliacao_alfabetizacao.alunos'
  AND a.presenca = 'Presente'
  AND a.proficiencia IS NOT NULL
  AND a.alfabetizado IN ('Sim', 'Nao')
  AND MOD(MOD(FARM_FINGERPRINT(TO_JSON_STRING(STRUCT(a.ano, a.id_aluno))), 100) + 100, 100) < __PERCENT__
ORDER BY row_id
