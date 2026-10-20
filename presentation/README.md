# Materiais da apresentação executiva

Fonte editorial: `content.json`, com títulos, falas, tempos e fontes locais. A fala foi enxugada após a gravação inicial de 5min15s. O PowerPoint final incorpora as alterações do autor e deve ser preservado; não regenerá-lo automaticamente sobre essas alterações.

Entregáveis: [slides editáveis](../output/presentation/Alfabetizacao_Fase3.pptx), [vídeo MP4](../output/video/Apresentacao_Executiva_Fase3.mp4) e [roteiro editável](../docs/roteiro_video.md). Os PDFs auxiliares foram excluídos pelo autor e não fazem parte da árvore final de entrega. Versões anteriores permanecem recuperáveis no histórico Git.

Oito slides, roteiro de **507 palavras**, gravação final com **292,5 segundos no MKV original** e **292,4 segundos no MP4**. A cópia MP4 permite distribuição mais compatível, com as mesmas trilhas H.264/AAC e sem recodificação. O MKV original permanece somente na pasta local do Tech Challenge.

## Conteúdo e evidências

Problema educacional, integração individual/histórica, prevenção de vazamento, escolhas de modelagem, desempenho, SHAP, perfis municipais, metas, evidência real do GCP e aplicação estratégica. A captura não representa treinamento cloud. AP não é acurácia; a v2 não tem novo teste independente; os cenários de 2030 não são previsões validadas.

Gráficos e diagrama são objetos editáveis no PPTX. Os gráficos têm planilhas incorporadas com valores arredondados a seis casas, suficientes para a precisão exibida. Os relatórios científicos preservam a precisão original.

## Reprodução dos materiais

Estes geradores são auxiliares de apresentação, separados das dependências do pipeline de ML. `build.mjs` usa o Node e `@oai/artifact-tool` do runtime de documentos do Codex, além dos validadores da skill Presentations. Em outra instalação, informar `FASE3_RUNTIME` (pasta de dependências) e `FASE3_SLIDES_SKILL` (pasta da skill), sem alterar o ambiente de ML.

Executar o gerador Node e, depois, `build_pdf.py` com um Python que tenha ReportLab e pypdf e a fonte Arial disponível. O gerador PDF usa os renders da apresentação reaberta a partir do pacote final. Os caminhos das fontes PDF são os do Windows atual e precisam ser ajustados em outra plataforma.

Para atualizar **somente o roteiro**, preservando o PPTX e o PDF dos slides, executar `build_pdf.py --script-only --phone-name Roteiro_Leitura_iPhone_Fase3_Enxuto.pdf`. A referência de 584 palavras e 315 segundos é informação da gravação relatada pelo usuário, não medição automatizada do vídeo.

O finalizador recusa substituir um PPTX final existente. Para uma nova revisão, escolher outro nome por `FASE3_DECK_NAME`. Renders, manifests de tempo e registros de validação permanecem privados em `runs/presentation-build`; pastas temporárias `.chart-data-*` também são ignoradas. Os materiais não dependem dos microdados dos alunos.

Esses geradores não gravam vídeos nem criam PRs. O registro de publicação fica em `../docs/GIT_WORKFLOW.md`. A geração de PDFs continua disponível como opção de apoio, mas a pasta `output/pdf/` é ignorada e não integra a entrega final.
