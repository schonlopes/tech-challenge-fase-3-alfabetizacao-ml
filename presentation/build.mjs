import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
// Use the desktop's bundled runtime, without adding dependencies to the ML environment.
const runtime = process.env.FASE3_RUNTIME || 'C:/Users/schon/.cache/codex-runtimes/codex-primary-runtime/dependencies';
process.env.RUNTIME_NODE_MODULES ??= path.join(runtime,'node/node_modules');
const skill = process.env.FASE3_SLIDES_SKILL || 'C:/Users/schon/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(runtime,'node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const root=path.resolve(import.meta.dirname,'..');
const content=JSON.parse(await fs.readFile(path.join(root,'presentation/content.json'),'utf8'));
const build=path.join(root,'runs/presentation-build');
const output=path.join(root,'output/presentation');
await fs.mkdir(build,{recursive:true}); await fs.mkdir(output,{recursive:true});
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={ink:'#162D3C',teal:'#087D80',muted:'#526572',gold:'#B88A34',silver:'#617B8B',paper:'#FAFAF6',white:'#FFFFFF',light:'#DFE7E8',rose:'#AC4F48'};
const font='Arial';
function text(s,value,x,y,w,h,size=26,color=C.ink,bold=false){
  const a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  a.text=value; a.text.insets=0; a.text.style={typeface:font,fontSize:size,bold,color};return a;
}
function slide(i,dark=false){
  const s=p.slides.add();s.background.fill=dark?C.ink:C.paper;
  if(i>0)text(s,content.slides[i].title,64,42,1144,66,42,dark?C.white:C.ink,true);
  text(s,`Tech Challenge Fase 3     ${i+1}/8`,64,678,600,22,16,dark?'#BCD1DA':C.muted);
  const c=content.slides[i];s.speakerNotes.text=`${c.interval}\n\n${c.speech}\n\nFontes locais: ${c.sources.join('; ')}.\n${i===6?'A captura é real. Treinamento local. PRs remotas ainda pendentes; não afirmar publicação concluída.':''}`;
  return s;
}
function foot(s,value){text(s,value,64,626,1144,42,18,C.muted);}
function node(s,title,subtitle,x,y,w,h,color){
  const a=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:C.paper,line:{fill:color,width:2}});
  text(s,title,x+18,y+16,w-36,40,27,color,true);
  text(s,subtitle,x+18,y+62,w-36,h-70,23,C.ink);return a;
}
function link(s,a,b){s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:C.muted,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});}
function bar(s,categories,values,x,y,w,h,{max=1,fmt='0.000',color=C.teal,points,labels=true,title}={}){
 const ch=s.charts.add('bar',{
  position:{left:x,top:y,width:w,height:h},categories,
  // Six decimals are more than displayed and fit Excel's 15-digit numeric precision.
  series:[{name:title||'Valor',values:values.map(v=>Number(v.toFixed(6))),fill:color,points}],
  barOptions:{direction:'bar',grouping:'clustered',gapWidth:90},hasLegend:false,
  xAxis:{visible:true,majorGridlines:null,textStyle:{fontSize:23,fill:C.ink},line:{fill:'none',width:0}},
  yAxis:{visible:true,min:0,max,majorUnit:max>1?20:(max>0.6?0.2:0.1),numberFormatCode:max>1?'0': '0.0',
    majorGridlines:{fill:C.light,width:1},textStyle:{fontSize:18,fill:C.muted},line:{fill:'none',width:0}},
  dataLabels:{showValue:labels,position:'outEnd',numberFormatCode:fmt,textStyle:{fontSize:24,fill:C.ink,bold:true}},
  chartFill:C.paper,plotAreaFill:C.paper,chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}
 });applyPresentationChartFont(ch,{fontFamily:font});return ch;
}
// 1. Minimal cover, with native editable text.
{
 const s=slide(0,true);
 text(s,'ALFABETIZAÇÃO NO BRASIL',64,91,1100,42,26,'#72D0C0',true);
 text(s,'Predição e\ninteligência analítica',64,190,1140,190,70,C.white,true);
 text(s,'Risco educacional e planejamento de políticas públicas',68,426,1070,76,31,'#D8E5EA');
 text(s,content.author,68,559,950,40,26,C.white);
}
// 2. Native source-to-model diagram; connectors do not cross text.
{
 const s=slide(1);
 text(s,'92.389',64,126,400,74,66,C.teal,true);
 text(s,'alunos válidos de 2024',64,205,490,40,29);
 text(s,'5.193 municípios',742,146,460,60,43,C.ink,true);
 const a=node(s,'Silver individual','Alunos válidos de 2024',64,290,340,130,C.silver);
 const b=node(s,'Gold de modelagem','Extensão local individual',472,290,340,130,C.gold);
 const c=node(s,'Modelo de risco','Não alfabetização = 1',880,290,330,130,C.teal);
 link(s,a,b);link(s,b,c);
 text(s,'Contexto anterior ao desfecho',64,468,1060,38,28,C.ink,true);
 text(s,'Gold municipal de 2023 e população IBGE de 2022',64,515,1120,54,27,C.muted);
 foot(s,'A Gold da Fase 2 é municipal. A integração individual é uma extensão local, com microdados privados.');
}
// 3. Split counts and the model workflow, with no opaque accuracy claims.
{
 const s=slide(2);
 const xs=[64,472,880];
 for(const [i,[name,rows,towns]] of [['Treino','61.503','3.074 municípios'],['Validação','15.163','1.086 municípios'],['Teste','15.723','1.033 municípios']].entries()){
  text(s,name,xs[i],145,330,42,29,C.teal,true);
  text(s,rows,xs[i],202,330,70,53,C.ink,true);
  text(s,towns,xs[i],282,330,38,24,C.muted);
 }
 text(s,'Pré-processamento integrado ao estimador',64,362,1136,48,31,C.ink,true);
 text(s,'Mediana e ausências, log da população, escala e One-Hot Encoding',64,424,1136,74,27);
 text(s,'Busca com GroupKFold no treino. Escolha na validação.',64,520,1136,48,27,C.teal,true);
 foot(s,'Municípios sem sobreposição. Proficiência excluída dos atributos. Teste territorial em 2024, não temporal.');
}
// 4. Native chart with complete literal values from the frozen report.
{
 const s=slide(3);
 text(s,'Average precision no teste',64,130,720,44,28,C.ink,true);
 bar(s,['Referência constante','Histórico municipal','Logística selecionada'],[0.38885708834191945,0.5085724,0.5250128869679892],54,195,742,344,
  {max:0.65,points:[{idx:0,fill:C.light},{idx:1,fill:C.silver},{idx:2,fill:C.teal}]});
 text(s,'0,656',870,157,330,82,65,C.teal,true);
 text(s,'ROC-AUC no teste',870,246,330,56,26);
 text(s,'Enriquecimento v2',870,352,330,45,28,C.ink,true);
 text(s,'Sem ganho observado\nna validação',870,410,330,98,28,C.muted);
 text(s,'Referência mantida:\nlogística original',870,523,330,70,26,C.teal,true);
 foot(s,'AP não é acurácia. Ganho sobre o histórico sem teste pareado de significância. Fonte: experimento v1.');
}
// 5. Native SHAP chart. Distinct decision policies, visibly labeled.
{
 const s=slide(4);
 text(s,'Influência global no modelo',64,130,700,44,28,C.ink,true);
 bar(s,['Histórico municipal','UF','Região','Rede','População (log)'],
  [0.40017030500128903,0.16716287408171937,0.08545309944104476,0.027775035096229233,0.00819531886086609],54,191,706,349,
  {max:0.52,fmt:'0.00',color:C.teal});
 text(s,'95,76%',838,140,370,82,63,C.rose,true);
 text(s,'sinalizados pelo limiar F2\nno teste histórico',838,232,370,96,27);
 text(s,'Alternativa de até 20%',838,376,370,42,27,C.teal,true);
 text(s,'Somente na validação.\nSem teste independente.',838,430,370,100,27,C.muted);
 text(s,'Padrão: escores sem alerta automático',64,557,1144,45,31,C.teal,true);
 foot(s,'SHAP médio absoluto em log-odds, na validação. Série constante: efeito zero. Importância não implica causalidade.');
}
// 6. Descriptive profiles plus a directly comparable observed target gap.
{
 const s=slide(5);
 text(s,'Alfabetização média municipal em 2024',64,130,740,42,28,C.ink,true);
 bar(s,['Perfil 1','Perfil 2'],[66.91777704918033,57.56520050125313],66,198,690,278,
  {max:100,fmt:'0.0"%"',points:[{idx:0,fill:C.teal},{idx:1,fill:C.gold}]});
 text(s,'3.122 municípios no perfil 1\n2.443 municípios no perfil 2',86,492,660,80,26,C.muted);
 text(s,'2.444 / 5.232',804,151,410,66,46,C.rose,true);
 text(s,'municípios abaixo\nda meta de 2024',804,237,405,86,30);
 text(s,'Cenários até 2030',804,383,410,43,29,C.teal,true);
 text(s,'Apoio à discussão do\navanço necessário',804,441,410,85,27,C.muted);
 foot(s,'Perfis sem alfabetização na formação. Médias não ponderadas. Contexto social de 2010. Cenários sem validação preditiva.');
}
// 7. The screenshot is an existing real capture, not a reconstructed interface.
{
 const s=slide(6);
 const bytes=await fs.readFile(path.join(root,'images/evidence/gcp_query_processing_controls.png'));
 s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:'Captura real do BigQuery com consulta concluída e limite de bytes',fit:'contain',position:{left:64,top:160,width:760,height:428}});
 text(s,'Consulta concluída',870,150,340,45,28,C.teal,true);
 text(s,'1,87 MB processados\nTeto de 1 GB na consulta',870,210,340,90,25);
 text(s,'36 testes aprovados',870,344,340,46,29,C.ink,true);
 text(s,'Demo sem GCP\nPrevisão com modelo salvo\nHashes por execução',870,414,340,138,25,C.muted);
 foot(s,'Captura real de 19/10/2026. Dados e consultas no GCP. Treinamento local. Microdados fora do Git.');
}
// 8. Closing belongs last, after the evidence.
{
 const s=slide(7,true);
 text(s,'Acompanhamento pedagógico',64,160,1144,55,40,C.white,true);
 text(s,'Escores como apoio ao diagnóstico humano',64,220,1144,45,27,'#C5D7DE');
 text(s,'Planejamento territorial',64,318,1144,55,40,'#72D0C0',true);
 text(s,'Perfis municipais e monitoramento de metas',64,378,1144,48,27,'#C5D7DE');
 text(s,'Antes do uso operacional',64,488,1144,43,30,C.white,true);
 text(s,'Atualizar o contexto e validar em uma nova coorte',64,545,1144,66,29,'#C5D7DE');
}
for(let i=0;i<p.slides.items.length;i++){
 const s=p.slides.items[i];
 const file=path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`);
 const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(file,new Uint8Array(await png.arrayBuffer()));
 const layout=await s.export({format:'layout'});await fs.writeFile(path.join(build,`slide-${i+1}.layout.json`),await layout.text());
}
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
const final=path.join(output,process.env.FASE3_DECK_NAME||'Alfabetizacao_Fase3.pptx');
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,
 pythonExecutable:path.join(runtime,'python/python.exe'),
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:8,requiredNativeChartOwnerSlides:[4,5,6],materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,
 receiptPath:path.join(build,`validation-${Date.now()}.json`)});
// Render the actual finalized package, including its embedded chart workbooks.
const reopened=await PresentationFile.importPptx(await FileBlob.load(final));
for(const [i,s] of reopened.slides.items.entries()){
 const png=await reopened.export({slide:s,format:'png',scale:1.5});
 await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log(`PPTX: ${final}`);
