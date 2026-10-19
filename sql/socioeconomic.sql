-- Public municipal aggregates only; historical socioeconomic context, not student data.
WITH social AS (
  SELECT id_municipio, 2010 AS ano_social, ivs_renda_trabalho,
    idhm_r AS idhm_renda, indice_gini, proporcao_vulneravel,
    proporcao_sem_agua_esgoto, proporcao_responsavel_fundamental_incompleto
  FROM `basedosdados.br_ipea_avs.municipio`
  WHERE ano = 2010 AND raca_cor = 'total' AND sexo = 'total'
    AND localizacao = 'total' AND udh = 'geral'
), economic AS (
  SELECT id_municipio, 2021 AS ano_pib, pib,
    SAFE_DIVIDE(va_adespss, va) AS fracao_va_administracao,
    SAFE_DIVIDE(va_industria, va) AS fracao_va_industria
  FROM `basedosdados.br_ibge_pib.municipio` WHERE ano = 2021
)
SELECT d.id_municipio, d.nome_municipio, d.sigla_uf, d.regiao,
  s.* EXCEPT(id_municipio), e.* EXCEPT(id_municipio)
FROM `__PROJECT__.alfabetizacao_silver.dim_municipio` d
LEFT JOIN social s USING(id_municipio)
LEFT JOIN economic e USING(id_municipio)
ORDER BY id_municipio
