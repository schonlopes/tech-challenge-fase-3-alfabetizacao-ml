# Estado da primeira versão

Código de extração, contrato, preparação, validação territorial, comparação, otimização e relatórios implementado localmente. A extração dos microdados para o computador foi bloqueada pela revisão automática de permissões, aguardando autorização específica do usuário para o payload. Até a extração e execução reais, **não existem resultados de desempenho nesta versão**.

Verificação em 19/10/2026: `python -m pytest -q` concluiu com **10 testes aprovados**, incluindo execução integrada dos quatro candidatos e geração dos oito gráficos dentro de uma pasta temporária, usando exclusivamente uma fixture artificial. Isso demonstra o funcionamento do software, não a qualidade preditiva nos dados educacionais reais. A consulta de extração ainda não foi validada em execução.

Auditoria inicial do GCP está em `docs/auditoria_inicial.md`. As evidências de consultas e o manifest do snapshot serão gravados em `reports/evidence/` somente após execução bem-sucedida. Capturas reais do console ainda estão pendentes.

## Extração aguardando autorização

Origem: tabelas do projeto GCP da Fase 2 e população pública do IBGE.

Destino: arquivo Parquet local em `data/raw/alunos_gold_modelagem.parquet`, ignorado pelo Git.

Conteúdo: aproximadamente 5% dos alunos válidos de 2024 (estimativa de 92 mil registros), com identificador de linha em hash, classificação alfabetizado/não alfabetizado convertida para risco, município, rede e série; contexto municipal da Gold 2023 e população de 2022. Não exporta nomes, ID bruto do aluno/escola, proficiência individual ou credenciais. Mesmo pseudonimizados, são registros individuais educacionais.

Finalidade: treinar e avaliar a pipeline local. Nenhum upload ou publicação de microdados está previsto. O primeiro passo após a autorização é executar a auditoria de rótulos; divergências interrompem a extração para revisão.
