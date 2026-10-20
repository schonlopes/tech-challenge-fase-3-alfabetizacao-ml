# Materiais da apresentação executiva

Fonte editorial: `content.json`, com títulos, falas, tempos e fontes locais. Em 20/10/2026, a fala foi enxugada após o usuário informar uma gravação de 5min15s. O roteiro e o novo PDF usam a fala revisada. O PowerPoint aberto com alterações locais foi preservado, portanto suas notas ainda podem conter a versão anterior. Não regenerar o deck automaticamente sobre as alterações do usuário.

Saídas finais: `../output/presentation/Alfabetizacao_Fase3.pptx`, `../output/pdf/Apresentacao_Alfabetizacao_Fase3.pdf` e `../output/pdf/Roteiro_Leitura_iPhone_Fase3_Enxuto.pdf`. O PDF de roteiro anterior foi mantido para referência. A versão editável revisada está em `../docs/roteiro_video.md`.

Oito slides, **507 palavras**, meta estimada de 4min45s. A projeção proporcional à gravação anterior é de cerca de 4min34s, sem garantir a duração da nova gravação. O usuário precisa ensaiar com cronômetro. O roteiro móvel usa fonte de 24 pontos e páginas em proporção de tela de celular. Páginas de continuação mantêm o slide atual.

## Conteúdo e evidências

Problema educacional, integração individual/histórica, prevenção de vazamento, escolhas de modelagem, desempenho, SHAP, perfis municipais, metas, evidência real do GCP e aplicação estratégica. A captura não representa treinamento cloud. AP não é acurácia; a v2 não tem novo teste independente; os cenários de 2030 não são previsões validadas.

Gráficos e diagrama são objetos editáveis no PPTX. Os gráficos têm planilhas incorporadas com valores arredondados a seis casas, suficientes para a precisão exibida. Os relatórios científicos preservam a precisão original. O PDF de slides é uma exportação visual das páginas renderizadas, sem editabilidade dos gráficos.

## Reprodução dos materiais

Estes geradores são auxiliares de apresentação, separados das dependências do pipeline de ML. `build.mjs` usa o Node e `@oai/artifact-tool` do runtime de documentos do Codex, além dos validadores da skill Presentations. Em outra instalação, informar `FASE3_RUNTIME` (pasta de dependências) e `FASE3_SLIDES_SKILL` (pasta da skill), sem alterar o ambiente de ML.

Executar o gerador Node e, depois, `build_pdf.py` com um Python que tenha ReportLab e pypdf e a fonte Arial disponível. O gerador PDF usa os renders da apresentação reaberta a partir do pacote final. Os caminhos das fontes PDF são os do Windows atual e precisam ser ajustados em outra plataforma.

Para atualizar **somente o roteiro**, preservando o PPTX e o PDF dos slides, executar `build_pdf.py --script-only --phone-name Roteiro_Leitura_iPhone_Fase3_Enxuto.pdf`. A referência de 584 palavras e 315 segundos é informação da gravação relatada pelo usuário, não medição automatizada do vídeo.

O finalizador recusa substituir um PPTX final existente. Para uma nova revisão, escolher outro nome por `FASE3_DECK_NAME`. Renders, manifests de tempo e registros de validação permanecem privados em `runs/presentation-build`; pastas temporárias `.chart-data-*` também são ignoradas. Os materiais não dependem dos microdados dos alunos.

As PRs remotas e a gravação não são geradas por esses comandos. Os slides não afirmam que essas etapas já ocorreram.
