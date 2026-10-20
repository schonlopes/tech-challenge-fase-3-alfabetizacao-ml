# Compatibilidade de redes na extensão analítica da Fase 3

A primeira extração de indicadores e metas da Gold retornou 23.995 linhas e zero metas associadas. A auditoria agregada encontrou códigos `0`, `2`, `3` e `5` nos indicadores, mas o texto `Municipal` nas metas municipais e `Pública` nas estaduais.

O dicionário público `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario` confirma: 3 = Municipal; 5 = Pública (Estadual e Municipal); 0 = Total (inclui rede privada); 2 = Estadual. Não juntar Total com Pública.

A extensão local normaliza `Municipal` para `3` e `Pública` para `5` nas junções. Os testes devem rejeitar junções sem correspondência de metas nas redes esperadas e duplicações de chaves. As tabelas da Fase 2 no GCP não foram alteradas.

Isso afeta a análise de metas, não o resultado do classificador v1: suas entradas eram contexto histórico municipal, população e categorias, sem metas contemporâneas ou futuras.

Os primeiros jobs sem normalização foram preservados com o sufixo `_before_network_fix`. Os jobs corrigidos e manifests atualizados documentam a nova extração. As metas de snapshots recentes são utilizadas como diagnóstico atual dos agregados e cenários; não são atributos do modelo nem evidência de disponibilidade histórica das metas revisadas.
