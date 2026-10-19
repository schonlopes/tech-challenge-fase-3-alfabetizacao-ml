"""Export the checked slide renders and a large-type phone reading script."""
import json
from pathlib import Path
import re

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CONTENT = json.loads((ROOT/'presentation/content.json').read_text(encoding='utf-8'))
OUTPUT = ROOT/'output/pdf'
OUTPUT.mkdir(parents=True,exist_ok=True)
BUILD = ROOT/'runs/presentation-build'
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
INK = HexColor('#162D3C')
MUTED = HexColor('#526572')
TEAL = HexColor('#087D80')


def lines(text, width, font='Arial', size=24):
    result=[]
    current=''
    for word in text.split():
        candidate=(current+' '+word).strip()
        if current and pdfmetrics.stringWidth(candidate,font,size)>width:
            result.append(current)
            current=word
        else:
            current=candidate
    if current:
        result.append(current)
    return result


def draw_lines(c, wrapped, x, y, size, leading, font='Arial', color=INK):
    c.setFillColor(color)
    c.setFont(font,size)
    for line in wrapped:
        c.drawString(x,y,line)
        y-=leading
    return y


def reading_pages(speech, capacity):
    """Keep complete sentences together and balance neighboring continuation pages."""
    sentences=[lines(sentence,330) for sentence in re.split(r'(?<=[.!?])\s+',speech)]
    groups=[[]]
    for sentence in sentences:
        if len(sentence)>capacity:
            raise ValueError('Frase longa demais para a leitura móvel; revisar a redação.')
        if sum(map(len,groups[-1]))+len(sentence)>capacity:
            groups.append([])
        groups[-1].append(sentence)
    if len(groups)>1:
        previous,last=groups[-2:]
        while len(previous)>1:
            before,after=sum(map(len,previous)),sum(map(len,last))
            moving=len(previous[-1])
            if after+moving>capacity or abs(before-moving-after-moving)>=abs(before-after):
                break
            last.insert(0,previous.pop())
    return [[line for sentence in group for line in sentence] for group in groups]


def main():
    deck=OUTPUT/'Apresentacao_Alfabetizacao_Fase3.pdf'
    c=canvas.Canvas(str(deck),pagesize=(960,540))
    c.setTitle(CONTENT['title'])
    c.setAuthor(CONTENT['author'])
    for i in range(1,9):
        c.drawImage(ImageReader(BUILD/f'slide-{i:02}.png'),0,0,width=960,height=540)
        c.showPage()
    c.save()

    phone=OUTPUT/'Roteiro_Leitura_iPhone_Fase3.pdf'
    c=canvas.Canvas(str(phone),pagesize=(390,844))
    c.setTitle('Roteiro de gravação - Fase 3')
    c.setAuthor(CONTENT['author'])
    c.setFillColor(HexColor('#FAFAF6'));c.rect(0,0,390,844,fill=1,stroke=0)
    draw_lines(c,['ROTEIRO DE GRAVAÇÃO'],30,790,17,26,'Arial-Bold',TEAL)
    y=draw_lines(c,['Tech Challenge','Fase 3'],30,724,31,42,'Arial-Bold')
    instructions=[
        'Meta: 4 minutos e 45 segundos. Limite: 5 minutos.',
        'Os próximos textos são as falas, na mesma ordem dos oito slides.',
        'Leia em ritmo natural. Faça uma pausa curta ao trocar de slide.',
        'Se houver uma página de continuação, mantenha o mesmo slide na tela.',
        'Ensaie com cronômetro. O tempo final depende do seu ritmo de fala.'
    ]
    for paragraph in instructions:
        y=draw_lines(c,lines(paragraph,330,size=22),30,y-30,22,30)
    c.showPage()
    timings=[]
    md=['# Roteiro do vídeo executivo - Fase 3',
        '', 'Meta de gravação: **4min45s**, com 15 segundos de margem até o limite de cinco minutos.',
        'O tempo é estimado, não cronometrado por uma gravação real. Ensaiar antes de gravar.',
        'O PDF móvel usa fonte de 24 pontos. Continuação de página não significa trocar de slide.', '']
    page_count=1
    for i,s in enumerate(CONTENT['slides'],1):
        title_lines=lines(s['title'],330,'Arial-Bold',18)
        start_y=744-len(title_lines)*24
        per_page=int((start_y-90)//34)+1
        for j,wrapped in enumerate(reading_pages(s['speech'],per_page)):
            c.setFillColor(HexColor('#FAFAF6'));c.rect(0,0,390,844,fill=1,stroke=0)
            label=f'SLIDE {i} DE 8'+('  /  CONTINUAÇÃO' if j else '')
            draw_lines(c,[label],30,800,15,24,'Arial-Bold',TEAL)
            draw_lines(c,title_lines,30,762,18,24,'Arial-Bold')
            draw_lines(c,wrapped,30,start_y-10,24,34)
            draw_lines(c,[s['interval']+'   /   '+str(s['seconds'])+' segundos'],30,35,13,18,'Arial',MUTED)
            c.showPage();page_count+=1
        words=len(s['speech'].split())
        timings.append({'slide':i,'seconds':s['seconds'],'words':words,'words_per_minute':round(words/s['seconds']*60,1)})
        md += [f'## Slide {i} - {s["title"]}', '',f'Tempo: {s["interval"]} ({s["seconds"]} segundos).', '',s['speech'],'']
    c.save()
    md += ['## Orientações para gravação','',
        '- Use a apresentação em tela cheia e mantenha o roteiro no celular próximo à câmera.',
        '- Desative notificações e teste o áudio antes de iniciar.',
        '- Não leia as notas de fonte, os rodapés ou os números dos slides.',
        '- AP: fale "precisão média". ROC-AUC: "área sob a curva ROC". SHAP: "shép".',
        '- Gold: "gôuld". Silver: "sílver". GroupKFold: "validação cruzada por município".',
        '- Prefira os arredondamentos já escritos no roteiro para não alongar a fala.',
        '- A captura do GCP é real, mas não representa treinamento na nuvem.',
        '- Antes da entrega, concluir a publicação e as PRs e confirmar os links do vídeo e repositório.',
        '- Se o ensaio ultrapassar cinco minutos, reduzir a fala antes de gravar. Não acelerar a ponto de prejudicar a compreensão.', '']
    (ROOT/'docs/roteiro_video.md').write_text('\n'.join(md),encoding='utf-8')
    total=sum(t['words'] for t in timings)
    (BUILD/'timing.json').write_text(json.dumps({'target_seconds':285,'total_words':total,
        'average_words_per_minute':round(total/285*60,1),'timings':timings,
        'phone_pages':page_count,'timing_is_estimated':True},indent=2),encoding='utf-8')
    assert len(PdfReader(deck).pages)==8
    assert len(PdfReader(phone).pages)==page_count
    for s in CONTENT['slides']:
        for source in s['sources']:
            if not (ROOT/source).exists():
                raise ValueError('Fonte inexistente: '+source)
    print(f'{total} palavras; meta 285 segundos; {page_count} páginas no roteiro móvel.')


if __name__=='__main__':
    main()
