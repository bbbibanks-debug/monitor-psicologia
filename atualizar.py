import requests
from bs4 import BeautifulSoup
import os
import functools
import re
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÕES DO TRADUTOR E KEYWORDS ---
def carregar_keywords():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

keywords = carregar_keywords()
noticias_filtradas_urgentes = []

def traduzir_texto(texto):
    if not texto or len(texto) < 12: return ""
    try: return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return ""

# --- INÍCIO DO SEU SCRIPT ORIGINAL ---
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime("%d%m%Yday%H%Mtime")
namefile = "index.html"

# Mapping original exato
links = ["https://verywellmind.com", "https://psychologytoday.com", 
"https://scientificamerican.com", "https://nih.gov",
"https://apa.org", "https://apa.org", 
"https://google.com", 
"https://sbponline.org.br", "https://neurosciencenews.com", "https://positivepsychology.com", 
"https://psychcentral.com", "http://iqscorner.com", "https://happierhuman.com", 
"https://psychnewsdaily.com", "https://psychiatrictimes.com", "https://psychologicalscience.org", 
"https://cfp.org.br", "https://scielo.br", "https://crpsp.org",
"https://elpais.com", "https://globo.com", "https://medicalxpress.com",
"https://psychreg.org", "https://uol.com.br", "https://libsyn.com", 
"https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", 
"https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://bigthink.com"]
import requests
from bs4 import BeautifulSoup
import os
import functools
import re
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- RECURSOS EXCLUSIVOS SOLICITADOS ---
def carregar_keywords():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

keywords = carregar_keywords()
noticias_filtradas_urgentes = []

def traduzir_texto(texto):
    if not texto or len(texto) < 12: return ""
    try: return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return ""

# --- INÍCIO DO SEU SCRIPT ORIGINAL ---
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime("%d%m%Yday%H%Mtime")
namefile = "index.html"

# Mapping original exato do seu PDF
links = [
    "https://verywellmind.com", "https://psychologytoday.com", 
    "https://scientificamerican.com", "https://nih.gov",
    "https://apa.org", "https://apa.org", 
    "https://google.com",
    "https://sbponline.org.br", "https://neurosciencenews.com", "https://positivepsychology.com", "https://psychcentral.com",
    "http://iqscorner.com", "https://happierhuman.com", "https://psychnewsdaily.com", "https://psychiatrictimes.com",
    "https://psychologicalscience.org", "https://cfp.org.br", "https://scielo.br", "https://crpsp.org",
    "https://elpais.com", "https://globo.com", "https://medicalxpress.com",
    "https://psychreg.org", "https://uol.com.br", "https://libsyn.com",
    "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br",
    "https://bigthink.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

responder = [None] * len(links)
parser = [None] * len(links)

for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Erro no link {links[x]}: {e}")

# Criação da HTML com o nome do Arquivo
file = open(namefile, "w", encoding="utf-8")
file.write('<!DOCTYPE html>')
file.write('<html lang="pt-br">')
file.write('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
file.write('<title>PSI LINKS BOARD</title>')
file.write('<style>.sub-tra { font-size: 0.82rem; color: #6c757d; display: block; margin-bottom: 8px; margin-left: 10px; } #btnVoltarTopo { position: fixed; bottom: 20px; right: 20px; display: none; z-index: 99; border: none; background-color: #17a2b8; color: white; padding: 10px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; }</style>')
file.write('</head>')

# Criação do Body, Container e Botões em Grade Estrita Horizontal Nativa do Bootstrap
file.write('<body><button onclick="irParaOTopo()" id="btnVoltarTopo">▲ Topo</button><div class="container" id="myGroup">')
file.write(f'<h1> PSI MONITOR <span class="text-muted" style="font-size:1rem; font-weight:normal; margin-left:12px;">| Varredura: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</span></h1><p>')

file.write('<a class="btn btn-space btn-danger btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseExample">🎯 PALAVRAS-CHAVE ATIVAS</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">VeryWell Mind</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample1" role="button" aria-expanded="false" aria-controls="collapseExample">Psychology Today</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false" aria-controls="collapseExample">Scientific American</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample3" role="button" aria-expanded="false" aria-controls="collapseExample">The National Institute of Mental Health (NIMH)</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample4" role="button" aria-expanded="false" aria-controls="collapseExample">APA PsyPort</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample5" role="button" aria-expanded="false" aria-controls="collapseExample">APA Monitor</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample6" role="button" aria-expanded="false" aria-controls="collapseExample">Google Notícias</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample7" role="button" aria-expanded="false" aria-controls="collapseExample">SBP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample8" role="button" aria-expanded="false" aria-controls="collapseExample">Neuroscience</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample9" role="button" aria-expanded="false" aria-controls="collapseExample">Positive Psychology</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample10" role="button" aria-expanded="false" aria-controls="collapseExample">Positive Psychcentral</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample11" role="button" aria-expanded="false" aria-controls="collapseExample">IQ`s Corner</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample12" role="button" aria-expanded="false" aria-controls="collapseExample">Happier Human</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample13" role="button" aria-expanded="false" aria-controls="collapseExample">PsyNewsDaily</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample14" role="button" aria-expanded="false" aria-controls="collapseExample">Psychiatric Times</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample15" role="button" aria-expanded="false" aria-controls="collapseExample">APS</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample16" role="button" aria-expanded="false" aria-controls="collapseExample">CFP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample17" role="button" aria-expanded="false" aria-controls="collapseExample">Psicologia USP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample18" role="button" aria-expanded="false" aria-controls="collapseExample">Conselho Regional de Psicologia SP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample19" role="button" aria-expanded="false" aria-controls="collapseExample">El País Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample20" role="button" aria-expanded="false" aria-controls="collapseExample">G1 Saúde Mental</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample21" role="button" aria-expanded="false" aria-controls="collapseExample">Medical Xpress</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample22" role="button" aria-expanded="false" aria-controls="collapseExample">Psychreg</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample23" role="button" aria-expanded="false" aria-controls="collapseExample">Folha Equilíbrio Mente</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample24" role="button" aria-expanded="false" aria-controls="collapseExample">PsychCrunch</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample25" role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Neurociência</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample26" role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample27" role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Relações</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample28" role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Saúde</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample29" role="button" aria-expanded="false" aria-controls="collapseExample">Big Think</a>')
file.write('</p>')
file.close()

# --- BLOCOS SEPARADOS EXATOS GRAVANDO EM ANEXO (MECÂNICA ORIGINAL) ---

# 0. Caixa Reservada de Palavras-Chave (Inicia 100% Fechada e Oculta)
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup">')
file.write('<div class="card card-body bg-light">')
# Esta lista será alimentada dinamicamente pelas coletas que baterem com o keywords.txt
file.write('</div></div>')
file.close()

# 0. VeryWell Mind (Corrigido para seletores funcionais dinâmicos, nascendo fechado)
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[0] is not None:
    for x in parser[0].find_all("a", class_=lambda c: c and ('card' in c or 'link' in c)):
        href = x.get("href")
        if href and href.startswith("/"): href = "https://verywellmind.com" + href
        texto = x.get_text().strip()
        if href and len(texto) > 15:
            file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
            trad = traduzir_texto(texto)
            if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
            if any(p in texto.lower() or p in trad.lower() for p in keywords):
                noticias_filtradas_urgentes.append((href, texto, trad, "VeryWell Mind"))
file.write("</div></div>")
file.close()

# 1. Psychology Today
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample1" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[1] is not None:
    for x in parser[1].find_all("div", class_="layout-content-main"):
        for z in x.find_all("a"):
            href = links[1] + str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Psychology Today"))
file.write("</div></div>")
file.close()

# 2. Scientific American
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample2" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[2] is not None:
    for x in parser[2].find_all("div", "articleList-CcaLz root-fREBs"):
        for z in x.find_all("a"):
            href = "https://scientificamerican.com" + str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Scientific American"))
file.write("</div></div>")
file.close()

# 3. NIMH
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample3" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[3] is not None:
    for x in parser[3].find_all("article"):
        for z in x.find_all("a", class_="aggregated_term_news_link"):
            href = "https://nih.gov" + str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "NIMH"))
file.write("</div></div>")
file.close()

# 4. APA PsyPort
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample4" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[4] is not None:
    for x in parser[4].find_all("article"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "APA PsyPort"))
file.write("</div></div>")
file.close()

# 5. APA Monitor
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample5" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[5] is not None:
    for x in parser[5].find_all("section", class_="linkWidget tile square"):
        for z in x.find_all("p", class_="title"):
            for n in z.find_all("a"):
                href = "https://apa.org" + str(n.get("href"))
                texto = z.text.strip()
                if len(texto) > 14:
                    file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                    trad = traduzir_texto(texto)
                    if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                    if any(p in texto.lower() or p in trad.lower() for p in keywords):
                        noticias_filtradas_urgentes.append((href, texto, trad, "APA Monitor"))
file.write("</div></div>")
file.close()

# 6. Google Notícias
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample6" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[6] is not None:
    for x in parser[6].find_all("article"):
        for z in x.find_all("a", class_="VDXfz"):
            href = "https://google.com" + str(z.get("href"))
            texto = x.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Google Notícias"))
file.write("</div></div>")
file.close()

# 7. SBP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample7" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[7] is not None:
    for x in parser[7].find_all("div", class_="content list"):
        for z in x.find_all("p"):
            for n in z.find_all("a"):
                href = "https://sbponline.org.br" + str(n.get("href"))
                texto = n.text.strip()
                if len(texto) > 14:
                    file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                    trad = traduzir_texto(texto)
                    if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                    if any(p in texto.lower() or p in trad.lower() for p in keywords):
                        noticias_filtradas_urgentes.append((href, texto, trad, "SBP"))
file.write("</div></div>")
file.close()

# 8. Neuroscience
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample8" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[8] is not None:
    for x in parser[8].find_all("h3"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = x.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Neuroscience"))
file.write("</div></div>")
file.close()

# 9. Positive Psychology
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample9" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[9] is not None:
    for x in parser[9].find_all("a"):
        for z in x.find_all("h3"):
            href = str(x.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Positive Psychology"))
file.write("</div></div>")
file.close()

# 10. Positive Psychcentral
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample10" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[10] is not None:
    for x in parser[10].find_all("div", class_="css-fdjy12"):
        for z in x.find_all("a"):
            href = "https://psychcentral.com" + str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Psychcentral"))
file.write("</div></div>")
file.close()

# 11. IQ`s Corner
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample11" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[11] is not None:
    for x in parser[11].find_all("h3"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "IQ`s Corner"))
file.write("</div></div>")
file.close()

# 12. Happier Human
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample12" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[12] is not None:
    for x in parser[12].find_all("h2"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Happier Human"))
file.write("</div></div>")
file.close()

# 13. PsyNewsDaily
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample13" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[13] is not None:
    for x in parser[13].find_all("h2"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "PsyNewsDaily"))
file.write("</div></div>")
file.close()

# 14. Psychiatric Times
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample14" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[14] is not None:
    for x in parser[14].find_all("a"):
        for z in x.find_all("h2"):
            href = "https://psychiatrictimes.com" + str(x.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "Psychiatric Times"))
file.write("</div></div>")
file.close()

# 15. APS
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample15" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[15] is not None:
    for x in parser[15].find_all("h3"):
        for z in x.find_all("a"):
            href = str(z.get("href"))
            texto = z.text.strip()
            if len(texto) > 14:
                file.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
                trad = traduzir_texto(texto)
                if trad and trad != texto: file.write(f'<span class="sub-tra">↳ {trad}</span>')
                if any(p in texto.lower() or p in trad.lower() for p in keywords):
                    noticias_filtradas_urgentes.append((href, texto, trad, "APS"))
file.write("</div></div>")
file.close()

# 16. CFP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample16" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[16] is not None:
    for x in parser[16].find_all("h3"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "CFP"))
file.write("</div></div>")
file.close()

# 17. Psicologia USP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample17" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[17] is not None:
    for x in parser[17].find_all("a"):
        for z in x.find_all("h3"):
            link_completo = "https://scielo.br" + str(x.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "Psicologia USP"))
file.write("</div></div>")
file.close()

# 18. Conselho Regional de Psicologia SP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample18" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[18] is not None:
    for x in parser[18].find_all("a"):
        for z in x.find_all("h3"):
            link_completo = str(x.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "CRP-SP"))
file.write("</div></div>")
file.close()

# 19. El País Psicologia
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample19" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[19] is not None:
    for x in parser[19].find_all("h2"):
        for z in x.find_all("a"):
            link_completo = "https://elpais.com" + str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "El País"))
file.write("</div></div>")
file.close()

# 20. G1 Saúde Mental
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample20" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[20] is not None:
    for x in parser[20].find_all("div", class_="_evt"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "G1"))
file.write("</div></div>")
file.close()

# 21. Medical Xpress
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample21" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[21] is not None:
    for x in parser[21].find_all("div"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "Medical Xpress"))
file.write("</div></div>")
file.close()

# 22. Psychreg
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample22" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[22] is not None:
    for x in parser[22].find_all("div", class_="col-md-4"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "Psychreg"))
file.write("</div></div>")
file.close()

# 23. Folha Equilíbrio Mente
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample23" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[23] is not None:
    for x in parser[23].find_all("a"):
        for z in x.find_all("h2"):
            link_completo = str(x.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "Folha"))
file.write("</div></div>")
file.close()

# 24. PsychCrunch
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample24" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[24] is not None:
    for x in parser[24].find_all("div", class_="libsyn-item-title"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "PsychCrunch"))
file.write("</div></div>")
file.close()

# 25. A Mente É Maravilhosa Neurociência
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample25" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[25] is not None:
    for x in parser[25].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
        link_completo = "https://amenteemaravilhosa.com.br" + str(x.get("href"))
        texto_limpo = x.text.strip()
        file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
        traducao = traduzir_texto(texto_limpo)
        if traducao and traducao != texto_limpo:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
        if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
            noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "A Mente É Maravilhosa Neurociência"))
file.write("</div></div>")
file.close()

# 26. A Mente É Maravilhosa Psicologia
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample26" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[26] is not None:
    for x in parser[26].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
        link_completo = "https://amenteemaravilhosa.com.br" + str(x.get("href"))
        texto_limpo = x.text.strip()
        file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
        traducao = traduzir_texto(texto_limpo)
        if traducao and traducao != texto_limpo:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
        if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
            noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "A Mente É Maravilhosa Psicologia"))
file.write("</div></div>")
file.close()

# 27. A Mente É Maravilhosa Relações
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample27" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[27] is not None:
    for x in parser[27].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
        link_completo = "https://amenteemaravilhosa.com.br" + str(x.get("href"))
        texto_limpo = x.text.strip()
        file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
        traducao = traduzir_texto(texto_limpo)
        if traducao and traducao != texto_limpo:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
        if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
            noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "A Mente É Maravilhosa Relações"))
file.write("</div></div>")
file.close()

# 28. A Mente É Maravilhosa Saúde
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample28" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[28] is not None:
    for x in parser[28].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
        link_completo = "https://amenteemaravilhosa.com.br" + str(x.get("href"))
        texto_limpo = x.text.strip()
        file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
        traducao = traduzir_texto(texto_limpo)
        if traducao and traducao != texto_limpo:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
        if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
            noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "A Mente É Maravilhosa Saúde"))
file.write("</div></div>")
file.close()

# 29. Big Think Neuropsych
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample29" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[29] is not None:
    for x in parser[29].find_all("h1", class_="card-headline"):
        for z in x.find_all("a"):
            link_completo = str(z.get("href"))
            texto_limpo = z.text.strip()
            file.write(f'<a href="{link_completo}">{texto_limpo}</a></br>')
            traducao = traduzir_texto(texto_limpo)
            if traducao and traducao != texto_limpo:
                file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
            if any(p in texto_limpo.lower() or p in traducao.lower() for p in keywords):
                noticias_filtradas_urgentes.append((link_completo, texto_limpo, traducao, "Big Think"))
file.write("</div></div>")
file.close()


# =====================================================================
# BLOCO DE FECHAMENTO E MONTAGEM DA CAIXA EXCLUSIVA DE PALAVRAS-CHAVE
# =====================================================================
file = open(namefile, "a", encoding="utf-8")

# Inserção da caixa de Palavras-Chave Ativas no mesmo padrão estrito dos botões Bootstrap
file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup" Style>')
file.write('<div class="card card-body bg-light">')
file.write(f'<p class="text-muted small">Termos monitorados ativos: {", ".join(keywords)}</p>')

if not noticias_filtradas_urgentes:
    file.write('<p class="text-muted">Nenhum artigo correspondente encontrado nas últimas varreduras.</p>')
else:
    for l_url, l_orig, l_trad, l_fonte in noticias_filtradas_urgentes:
        file.write(f'<a href="{l_url}" target="_blank">📌 [{l_fonte}] {l_orig}</a></br>')
        if l_trad and l_trad != l_orig:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ Tradução: {l_trad}</span>')

file.write("</div></div>")

# Scripts finais padrão do Bootstrap coletados do rodapé do seu arquivo original
file.write('<div>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jquery.com"></script>')
file.write('<script src="https://cloudflare.com"></script>')
file.write('<script src="https://bootstrapcdn.com"></script>')
file.write('</div></body>')

# Fechamento definitivo do arquivo index.html
file.close()
print("Sucesso! O script concluiu com precisão toda a árvore de renderização do design nativo.")

