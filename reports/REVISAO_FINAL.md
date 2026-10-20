# Revisão final da entrega - 20/10/2026

## Código e dados

- 36 testes aprovados no ambiente local, compilação concluída e dependências sem inconsistências em `pip check`.
- Todas as versões de `requirements-lock.txt` foram localizadas no PyPI. Os releases oficiais consultados de checkout e setup-python mantêm a versão principal v7 utilizada no workflow.
- A verificação do histórico Git não encontrou arquivos de microdados/modelos privados nem correspondências dos padrões comuns de tokens GitHub, chaves privadas e chaves de API Google utilizados na varredura. Essa checagem não é garantia universal de ausência de segredos.
- A configuração ignora snapshots individuais, modelos, saídas privadas de execução e PDFs auxiliares. Não foram executadas novas consultas GCP nem novos treinamentos reais na revisão.

## Apresentação e vídeo

- O PPTX é estruturalmente legível e contém oito slides.
- O vídeo original contém imagem 1920x1080, codec H.264, áudio AAC estéreo e duração de **292,5 segundos**, inferior ao teto de 300 segundos.
- O MP4 utiliza as trilhas originais H.264/AAC com `faststart`, sem recodificação. Tem **292,4 segundos** e fica abaixo de 100 MiB.
- A inspeção visual por amostras cobre os slides de dados, validação, métricas, SHAP, perfis, GCP e encerramento. As métricas visíveis correspondem aos relatórios, e o apresentador não cobre os dados principais nessas amostras.
- A trilha de áudio foi decodificada com sucesso e contém sinal. Não foi feita transcrição automática integral nem certificação subjetiva da qualidade de escuta.
- Os materiais executivos da entrega são o vídeo MP4, os slides editáveis e o roteiro em Markdown.

## Critérios e limites

A entrega mantém as distinções entre teste territorial de 2024, comparação v2 somente na validação e cenários não validados de longo prazo. O alto recall vem acompanhado do volume elevado de alertas. Os prints GCP comprovam consultas/dados na nuvem, e não treinamento cloud. O contexto social é de 2010 e o modelo não está aprovado para decisões automáticas sobre alunos.

A publicação e as PRs são registradas em [versionamento](../docs/GIT_WORKFLOW.md). O resultado remoto do workflow deve ser conferido no GitHub; os testes locais, isoladamente, não comprovam sua execução remota.
