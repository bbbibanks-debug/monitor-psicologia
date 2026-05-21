import requests
from bs4 import *
import os
import functools
import re
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- Configuração de Tempo (Mantida do seu original) ---
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# --- Carregamento Seguro das Palavras-Chave ---
def carregar_palavras_chave():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

palavras_chave = carregar_palavras_chave()
noticias_filtradas_urgentes = []

def traduzir_texto(texto):
    if not texto or len(texto.strip()) < 10:
        return ""
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except Exception:
        return ""

# --- Mapeamento das 30 URLs Originais ---
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
    "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br", "https://bigthink.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# --- Loop de Conexão Nativo ---
responder = [None] * len(links)
parser = [None] * len(links)
for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Erro ao acessar {links[x]}: {e}")

# --- CRIAÇÃO DO HEAD E BOTÕES (Design Clássico Restaurado) ---
file = open(namefile, "w", encoding="utf-8")
file.write('<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
file.write('<title>PSI LINKS BOARD</title>')
file.write('<style>.btn-space{margin:4px;} .sub-tra{font-size:0.78rem; color:#6c757d; display:block; margin-bottom:6px; margin-left:10px;}</style></head>')
file.write('<body><div class="container" id="myGroup"><h1> PSI MONITOR</h1><p>')

# Botão customizado de Palavras-Chave integrado na mesma linha
file.write('<a class="btn btn-space btn-primary btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false">🎯 Palavras-Chave Ativas</a>')

# Seus botões originais idênticos
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false">VeryWell Mind</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample1" role="button" aria-expanded="false">Psychology Today</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false">Scientific American</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample3" role="button" aria-expanded="false">The National Institute of Mental Health (NIMH)</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample4" role="button" aria-expanded="false">APA PsyPort</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample5" role="button" aria-expanded="false">APA Monitor</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample6" role="button" aria-expanded="false">Google Notícias</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample7" role="button" aria-expanded="false">SBP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample8" role="button" aria-expanded="false">Neuroscience</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample9" role="button" aria-expanded="false">Positive Psichology</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample10" role="button" aria-expanded="false">Positive Psychcentral</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample11" role="button" aria-expanded="false">IQ`s Corner</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample12" role="button" aria-expanded="false">Happier Human</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample13" role="button" aria-expanded="false">PsyNewsDaily</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample14" role="button" aria-expanded="false">Psychiatric Times</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample15" role="button" aria-expanded="false">APS</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample16" role="button" aria-expanded="false">CFP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample17" role="button" aria-expanded="false">Psicologia USP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample18" role="button" aria-expanded="false">Conselho Regional de Psicologia SP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample19" role="button" aria-expanded="false">El País Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample20" role="button" aria-expanded="false">G1 Saúde Mental</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample21" role="button" aria-expanded="false">Medical Xpress</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample22" role="button" aria-expanded="false">Psychreg</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample23" role="button" aria-expanded="false">Folha Equilíbrio Mente</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample24" role="button" aria-expanded="false">PsychCrunch</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample25" role="button" aria-expanded="false">A Mente é Maravilhosa-Neurociência</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample26" role="button" aria-expanded="false">A Mente é Maravilhosa-Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample27" role="button" aria-expanded="false">A Mente é Maravilhosa-Relações</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample28" role="button" aria-expanded="false">A Mente é Maravilhosa-Saúde</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample29" role="button" aria-expanded="false">Big Think</a>')
file.write('</p>')
file.close()

# --- FUNÇÃO AUXILIAR DE ESCREVER LINK (Processa Filtros e Traduções sem quebrar as tags) ---
def escrever_link(file_obj, href, texto, nome_fonte=""):
    t_clean = texto.strip()
    if not href or len(t_clean) < 12:
        return
    
    # Escreve no bloco nativo do site
    file_obj.write(f'<a href="{href}" target="_blank">{t_clean}</a></br>\n')
    trad = traduzir_texto(t_clean)
    if trad and trad.lower() != t_clean.lower():
        file_obj.write(f'<span class="sub-tra">↳ {trad}</span>\n')
        
    # Verifica palavra-chave para injetar posteriormente no painel principal
    if any(p in t_clean.lower() or p in trad.lower() for p in palavras_chave):
        noticias_filtradas_urgentes.append({"url": href, "texto": t_clean, "trad": trad, "fonte": nome_fonte})

# =======================================================================================
# --- PROCESSAMENTO DOS SELETORES ORIGINAIS DE CADA SITE (Nenhum seletor seu foi alterado) ---
# =======================================================================================

# 0. VeryWell Mind (Corrigido para usar a nova estrutura dinâmica baseada em links)
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse show" id="collapseExample" data-parent="#myGroup" Style><div class="card card-body">')
if parser[0] is not None:
    for z in parser[0].find_all("a", class_=lambda c: c and ('card' in c or 'link' in c))[:12]:
        url = z.get("href")
        if url and url.startswith("/"): url = "https://verywellmind.com" + url
        escrever_link(file, url, z.text, "VeryWell Mind")
file.write("</div></div>")
file.close()

# 1. Psychology Today
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample1" data-parent="#myGroup" Style><div class="card card-body">')
if parser[1] is not None:
    for x in parser[1].find_all("div", class_="layout-content-main"):
        for z in x.find_all("a"):
            escrever_link(file, links[1] + z.get("href"), z.text, "Psychology Today")
file.write("</div></div>")
file.close()

# 2. Scientific American
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample2" data-parent="#myGroup" Style><div class="card card-body">')
if parser[2] is not None:
    for x in parser[2].find_all("div", "articleList-CcaLz root-fREBs"):
        for z in x.find_all("a"):
            escrever_link(file, "https://scientificamerican.com" + z.get("href"), z.text, "Scientific American")
file.write("</div></div>")
file.close()

# 3. NIHM
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample3" data-parent="#myGroup" Style><div class="card card-body">')
if parser[3] is not None:
    for x in parser[3].find_all("article"):
        for z in x.find_all("a", class_="aggregated_term_news_link"):
            escrever_link(file, "https://nih.gov" + z.get("href"), z.text, "NIMH")
file.write("</div></div>")
file.close()

# 4. APA PsyPort
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample4" data-parent="#myGroup" Style><div class="card card-body">')
if parser[4] is not None:
    for x in parser[4].find_all("article"):
        for z in x.find_all("a"):
            escrever_link(file, z.get("href"), z.text, "APA PsyPort")
file.write("</div></div>")
file.close()

# 5. APA Monitor
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample5" data-parent="#myGroup" Style><div class="card card-body">')
if parser[5] is not None:
    for x in parser[5].find_all("section", class_="linkWidget tile square"):
        for z in x.find_all("p", class_="title"):
            for n in z.find_all("a"):
                escrever_link(file, "https://apa.org" + str(n.get("href")), z.text, "APA Monitor")
file.write("</div></div>")
file.close()

# 6. Google Notícias
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample6" data-parent="#myGroup" Style><div class="card card-body">')
if parser[6] is not None:
    for x in parser[6].find_all("article"):
        for z in x.find_all("a", class_="VDXfz"):
            escrever_link(file, "https://google.com" + str(z.get("href")), x.text, "Google Notícias")
file.write("</div></div>")
file.close()

# 7. SBP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample7" data-parent="#myGroup" Style><div class="card card-body">')
if parser[7] is not None:
    for x in parser[7].find_all("div", class_="content list"):
        for z in x.find_all("p"):
            for n in z.find_all("a"):
                escrever_link(file, "https://sbponline.org.br" + str(n.get("href")), n.text, "SBP")
file.write("</div></div>")
file.close()

# 8. Neuroscience
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample8" data-parent="#myGroup" Style><div class="card card-body">')
if parser[8] is not None:
    for x in parser[8].find_all("h3"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), x.text, "Neuroscience")
file.write("</div></div>")
file.close()

# 9. Positive Psychology
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample9" data-parent="#myGroup" Style><div class="card card-body">')
if parser[9] is not None:
    for x in parser[9].find_all("a"):
        for z in x.find_all("h3"):
            escrever_link(file, str(x.get("href")), z.text, "Positive Psychology")
file.write("</div></div>")
file.close()

# 10. Psychcentral
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample10" data-parent="#myGroup" Style><div class="card card-body">')
if parser[10] is not None:
    for x in parser[10].find_all("div", class_="css-fdjy12"):
        for z in x.find_all("a"):
            escrever_link(file, "https://psychcentral.com" + str(z.get("href")), z.text, "Psychcentral")
file.write("</div></div>")
file.close()

# 11. IQ`s Corner
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample11" data-parent="#myGroup" Style><div class="card card-body">')
if parser[11] is not None:
    for x in parser[11].find_all("h3"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "IQ`s Corner")
file.write("</div></div>")
file.close()

# 12. Happier Human
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample12" data-parent="#myGroup" Style><div class="card card-body">')
if parser[12] is not None:
    for x in parser[12].find_all("h2"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "Happier Human")
file.write("</div></div>")
file.close()

# 13. PsychNewsDaily
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample13" data-parent="#myGroup" Style><div class="card card-body">')
if parser[13] is not None:
    for x in parser[13].find_all("h2"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "PsychNewsDaily")
file.write("</div></div>")
file.close()

# 14. Psychiatric Times
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample14" data-parent="#myGroup" Style><div class="card card-body">')
if parser[14] is not None:
    for x in parser[14].find_all("a"):
        for z in x.find_all("h2"):
            escrever_link(file, "https://psychiatrictimes.com" + str(x.get("href")), z.text, "Psychiatric Times")
file.write("</div></div>")
file.close()

# 15. APS
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample15" data-parent="#myGroup" Style><div class="card card-body">')
if parser[15] is not None:
    for x in parser[15].find_all("h3"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "APS")
file.write("</div></div>")
file.close()

# 16. CFP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample16" data-parent="#myGroup" Style><div class="card card-body">')
if parser[16] is not None:
    for x in parser[16].find_all("h3"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "CFP")
file.write("</div></div>")
file.close()

# 17. Psicologia USP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample17" data-parent="#myGroup" Style><div class="card card-body">')
if parser[17] is not None:
    for x in parser[17].find_all("a"):
        for z in x.find_all("h3"):
            escrever_link(file, "https://scielo.br" + str(x.get("href")), z.text, "Psicologia USP")
file.write("</div></div>")
file.close()

# 18. CRP-SP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample18" data-parent="#myGroup" Style><div class="card card-body">')
if parser[18] is not None:
    for x in parser[18].find_all("a"):
        for z in x.find_all("h3"):
            escrever_link(file, str(x.get("href")), z.text, "CRP-SP")
file.write("</div></div>")
file.close()

# 19. El País
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample19" data-parent="#myGroup" Style><div class="card card-body">')
if parser[19] is not None:
    for x in parser[19].find_all("h2"):
        for z in x.find_all("a"):
            escrever_link(file, "https://elpais.com" + str(z.get("href")), z.text, "El País")
file.write("</div></div>")
file.close()

# 20. G1 Saúde Mental
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample20" data-parent="#myGroup" Style><div class="card card-body">')
if parser[20] is not None:
    for x in parser[20].find_all("div", class_="_evt"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "G1 Saúde Mental")
file.write("</div></div>")
file.close()

# 21. Medical Xpress
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample21" data-parent="#myGroup" Style><div class="card card-body">')
if parser[21] is not None:
    for x in parser[21].find_all("div"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "Medical Xpress")
file.write("</div></div>")
file.close()

# 22. Psychreg
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample22" data-parent="#myGroup" Style><div class="card card-body">')
if parser[22] is not None:
    for x in parser[22].find_all("div", class_="col-md-4"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "Psychreg")
file.write("</div></div>")
file.close()

# 23. Folha Mente
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample23" data-parent="#myGroup" Style><div class="card card-body">')
if parser[23] is not None:
    for x in parser[23].find_all("a"):
        for z in x.find_all("h2"):
            escrever_link(file, str(x.get("href")), z.text, "Folha Mente")
file.write("</div></div>")
file.close()

# 24. PsychCrunch
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample24" data-parent="#myGroup" Style><div class="card card-body">')
if parser[24] is not None:
    for x in parser[24].find_all("div", class_="libsyn-item-title"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "PsychCrunch")
file.write("</div></div>")
file.close()

# 25-28. A Mente é Maravilhosa (Todos os blocos estruturais idênticos)
for idx, p_idx in enumerate([25, 26, 27, 28], start=25):
    file = open(namefile, "a", encoding="utf-8")
    file.write(f'<div class="collapse" id="collapseExample{p_idx}" data-parent="#myGroup" Style><div class="card card-body">')
    if parser[p_idx] is not None:
        for x in parser[p_idx].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
            escrever_link(file, "https://amenteemaravilhosa.com.br" + str(x.get("href")), x.text, "A Mente é Maravilhosa")
    file.write("</div></div>")
    file.close()

# 29. Big Think
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample29" data-parent="#myGroup" Style><div class="card card-body">')
if parser[29] is not None:
    for x in parser[29].find_all("h1", class_="card-headline"):
        for z in x.find_all("a"):
            escrever_link(file, str(z.get("href")), z.text, "Big Think")
file.write("</div></div>")
file.close()


# =======================================================================================
# --- GERAÇÃO APENAS DO CONTEÚDO DO CARD DE PALAVRAS-CHAVE NO FINAL ---
# =======================================================================================
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup" Style><div class="card card-body bg-light">')
file.write(f'<p class="text-muted small">Termos monitorados do arquivo: {", ".join(palavras_chave)}</p><hr>')

if not noticias_filtradas_urgentes:
    file.write('<p class="text-muted">Nenhum artigo correspondente encontrado nas raspagens recentes.</p>')
else:
    for item in noticias_filtradas_urgentes:
        file.write(f'<a href="{item["url"]}" target="_blank">📌 [{item["fonte"]}] {item["texto"]}</a></br>\n')
        if item["trad"] and item["trad"].lower() != item["texto"].lower():
            file.write(f'<span class="sub-tra">↳ Tradução: {item["trad"]}</span>\n')

file.write('</div></div>')

# --- Fechamento dos Scripts do Bootstrap Nativo ---
file.write('<div>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jsdelivr.net"></script>')
file.write('<script src="https://jquery.com"></script>')
file.write('<script src="https://cloudflare.com"></script>')
file.write('<script src="https://bootstrapcdn.com"></script>')
file.write('</div></div></body></html>')
file.close()

print("Sucesso! Raspagem e design preservados integralmente.")
