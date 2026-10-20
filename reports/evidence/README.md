# Evidências da primeira extração real

- `source_audit.json`: contagem por ano, fonte, presença e classe, sem registros individuais.
- `source_audit_job.json`: metadados reduzidos do job de auditoria, concluído com sucesso.
- `training_extract_job.json`: job de extração da amostra e contexto, concluído com sucesso; 92.389 linhas recuperadas.
- `snapshot_manifest.json`: hash do Parquet local, tamanho da amostra e descrição da origem.

As duas consultas processaram, respectivamente, 320.293.098 e 234.054.455 bytes. Os limites foram 2 GB por consulta. Os bytes faturáveis registrados são 320.864.256 e 234.881.024; esses valores não representam, por si só, uma cobrança monetária. A consulta de extração foi recuperada pelo mesmo job após correção de codificação, sem execução de uma segunda consulta de extração.

Os metadados não contêm nomes de alunos, credenciais ou dados de linhas. Os microdados ficam em `data/raw/`, fora do índice Git.

Esses arquivos comprovam os jobs consultados e a proveniência do snapshot. **Não são prints do console GCP.** Capturas reais ainda precisam ser adicionadas quando a interface estiver disponível.
