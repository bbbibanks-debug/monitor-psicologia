import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÃO DE TEMPO E ARQUIVO (ORIGINAL DO ANEXO) ---
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# --- MAPEAMENTO DE LINKS (IDÊNTICO AO SEU ANEXO) ---
links = [
    "https://verywellmind.com", 
    "https://psychologytoday.com", 
    "https://scientificamerican.com",
    "https://nih.gov",
    "https://apa.org",
    "https://apa.org",
    "https://google.com",
    "https://sbponline.org.br",
    "https://neurosciencenews.com",
    "https://positivepsychology.com",
    "https://psychcentral.com",
    "http://iqscorner.com",
    "https://happierhuman.com",
    "https://psychnewsdaily.com",
    "https://psychiatrictimes.com",
    "https://psychologicalscience.org",
    "https://cfp.org.br",
    "https://scielo.br",
    "https://crpsp.org",
    "https://elpais.com", 
    "https://globo.com",
    "https://medicalxpress.com",
    "https://psychreg.org",
    "https://uol.com.br", 
    "https://libsyn.com",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://bigthink.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# --- CONFIGURAÇÃO DO FILTRO DE PALAVRAS-CHAVE ---
def carregar_palavras_chave():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

palavras_chave = carregar_palavras_chave()
noticias_filtradas_html = "" # Acumula strings HTML para a caixa de palavras-chave

def traduzir(texto):
    if not texto or len(texto.strip()) < 10:
        return ""
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except:
        return ""

# --- INICIALIZAÇÃO DE LISTAS COM NONE (ORIGINAL) ---
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

# --- CRIAÇÃO DO ARQUIVO HTML E HEAD (ORIGINAL DO ANEXO) ---
file = open(namefile, "w", encoding="utf-8")
file.write('<!DOCTYPE html>')
file.write('<html lang="pt-br">')
file.write('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
file.write('<title>PSI LINKS BOARD</title>')
# Estilo discreto adicionado para as legendas de tradução ficarem menores e cinzas
file.write('<style>.sub-tra{font-size:0.80rem; color:#6c757d; display:block; margin-bottom:6px; margin-left:10px;}</style>')
file.write('</head>')

# --- CRIAÇÃO DOS BOTÕES (ESTRUTURA COMPLETA DO SEU ANEXO) ---
file.write('<body><div class="container" id="myGroup"><h1> PSI MONITOR</h1><p>')

# Botão das Palavras-Chave integrado perfeitamente no mesmo design
file.write('<a class="btn btn-space btn-primary btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false">🎯 PALAVRAS-CHAVE</a>')

# Todos os seus 30 botões originais preservados
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

# --- FUNÇÃO AUXILIAR DE ESCRITA DE LINK + FILTRO + TRADUÇÃO ---
def registrar_link(f_obj, url, texto, fonte_nome):
    global noticias_filtradas_html
    if not url or not texto or len(texto.strip()) < 12:
        return
    
    # Escreve o link original de forma padrão conforme seu anexo
    f_obj.write('<a href="' + url + '" target="_blank">' + texto + '</a></br>\n')
    
    # Processa a tradução e adiciona embaixo em fonte menor
    legenda_traduzida = traduzir(texto)
    if legenda_traduzida and legenda_traduzida.lower() != texto.lower():
        f_obj.write('<span class="sub-tra">↳ ' + legenda_traduzida + '</span>\n')
        
    # Verifica se bate com as palavras-chave para alimentar o box principal
    if any(p in texto.lower() or p in legenda_traduzida.lower() for p in palavras_chave):
        noticias_filtradas_html += '<a href="' + url + '" target="_blank">📌 [' + fonte_nome + '] ' + texto + '</a></br>\n'
        if legenda_traduzida:
            noticias_filtradas_html += '<span class="sub-tra">↳ Tradução: ' + legenda_traduzida + '</span>\n'

# --- CLASSES DE CONTEÚDO DOS BOTÕES (EXATAMENTE COMO O SEU ANEXO) ---

# 0. Very Well Mind (CORRIGIDO: Varre os cards dinâmicos estruturais)
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse show" id="collapseExample" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[0] is not None:
    for z in parser[0].find_all("a", class_=lambda c: c and ('card' in c or 'link' in c))[:12]:
        href = z.get("href", "")
        if href.startswith("/"): href = "https://verywellmind.com" + href
        registrar_link(file, href, z.text.strip(), "VeryWell Mind")
file.write("</div></div>")
file.close()

# 1. Psychology Today
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample1" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[1] is not None:
    for x in parser[1].find_all("div", class_="layout-content-main"):
        for z in x.find_all("a"):
            registrar_link(file, links[1] + z.get("href", ""), z.text.strip(), "Psychology Today")
file.write("</div></div>")
file.close()

# 2. Scientific American (CORRIGIDO: Seletor flexível baseado em links de artigos)
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample2" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[2] is not None:
    for z in parser[2].find_all("a", href=re.compile(r"/article/"))[:12]:
        href = z.get("href", "")
        if href.startswith("/"): href = "https://scientificamerican.com" + href
        registrar_link(file, href, z.text.strip(), "Scientific American")
file.write("</div></div>")
file.close()

# 3. NIHM
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample3" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[3] is not None:
    for x in parser[3].find_all("article"):
        for z in x.find_all("a", class_="aggregated_term_news_link"):
            registrar_link(file, "https://nih.gov" + z.get("href", ""), z.text.strip(), "NIMH")
file.write("</div></div>")
file.close()

# 4. APA PsyPort
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample4" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[4] is not None:
    for x in parser[4].find_all("article"):
        for z in x.find_all("a"):
            registrar_link(file, z.get("href", ""), z.text.strip(), "APA PsyPort")
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
                registrar_link(file, "https://apa.org" + str(n.get("href")), z.text.strip(), "APA Monitor")
file.write("</div></div>")
file.close()

# 6. Google Notícias
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample6" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[6] is not None:
    for x in parser[6].find_all("article"):
        for z in x.find_all("a", class_="VDXfz"):
            registrar_link(file, "https://google.com" + str(z.get("href")), x.text.strip(), "Google Notícias")
file.write("</div></div>")
file.close()

# 7. Sociedade Brasileira de Psicologia
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample7" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[7] is not None:
    for x in parser[7].find_all("div", class_="content list"):
        for z in x.find_all("p"):
            for n in z.find_all("a"):
                registrar_link(file, "https://sbponline.org.br" + str(n.get("href")), n.text.strip(), "SBP")
file.write("</div></div>")
file.close()

# 8. Neuroscience
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample8" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[8] is not None:
    for x in parser[8].find_all("h3"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), x.text.strip(), "Neuroscience")
file.write("</div></div>")
file.close()

# 9. Positive Psychology
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample9" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[9] is not None:
    for x in parser[9].find_all("a"):
        for z in x.find_all("h3"):
            registrar_link(file, str(x.get("href")), z.text.strip(), "Positive Psychology")
file.write("</div></div>")
file.close()

# 10. Psychcentral
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample10" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[10] is not None:
    for x in parser[10].find_all("div", class_="css-fdjy12"):
        for z in x.find_all("a"):
            registrar_link(file, "https://psychcentral.com" + str(z.get("href")), z.text.strip(), "Psychcentral")
file.write("</div></div>")
file.close()

# 11. IQ`s Corner
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample11" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[11] is not None:
    for x in parser[11].find_all("h3"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "IQ's Corner")
file.write("</div></div>")
file.close()

# 12. Happier Human
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample12" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[12] is not None:
    for x in parser[12].find_all("h2"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "Happier Human")
file.write("</div></div>")
file.close()

# 13. PsychNewsDaily
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample13" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[13] is not None:
    for x in parser[13].find_all("h2"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "PsychNewsDaily")
file.write("</div></div>")
file.close()

# 14. Psychiatric Times
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample14" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[14] is not None:
    for x in parser[14].find_all("a"):
        for z in x.find_all("h2"):
            registrar_link(file, "https://psychiatrictimes.com" + str(x.get("href")), z.text.strip(), "Psychiatric Times")
file.write("</div></div>")
file.close()

# 15. APS
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample15" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[15] is not None:
    for x in parser[15].find_all("h3"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "APS")
file.write("</div></div>")
file.close()

# 16. CFP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample16" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[16] is not None:
    for x in parser[16].find_all("h3"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "CFP")
file.write("</div></div>")
file.close()

# 17. Psicologia USP
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample17" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[17] is not None:
    for x in parser[17].find_all("a"):
        for z in x.find_all("h3"):
            registrar_link(file, "https://scielo.br" + str(x.get("href")), z.text.strip(), "Psicologia USP")
file.write("</div></div>")
file.close()

# 18. Conselho Regional de Psicologia de São Paulo
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample18" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[18] is not None:
    for x in parser[18].find_all("a"):
        for z in x.find_all("h3"):
            registrar_link(file, str(x.get("href")), z.text.strip(), "CRP-SP")
file.write("</div></div>")
file.close()

# 19. El País Psicologia
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample19" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[19] is not None:
    for x in parser[19].find_all("h2"):
        for z in x.find_all("a"):
            registrar_link(file, "https://elpais.com" + str(z.get("href")), z.text.strip(), "El País")
file.write("</div></div>")
file.close()

# 20. G1 Saúde
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample20" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[20] is not None:
    for x in parser[20].find_all("div", class_="_evt"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "G1 Saúde Mental")
file.write("</div></div>")
file.close()

# 21. Medical Xpress
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample21" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[21] is not None:
    for x in parser[21].find_all("div"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "Medical Xpress")
file.write("</div></div>")
file.close()

# 22. Psychreg
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample22" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[22] is not None:
    for x in parser[22].find_all("div", class_="col-md-4"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "Psychreg")
file.write("</div></div>")
file.close()

# 23. Folha Equilíbrio Mente
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample23" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[23] is not None:
    for x in parser[23].find_all("a"):
        for z in x.find_all("h2"):
            registrar_link(file, str(x.get("href")), z.text.strip(), "Folha Mente")
file.write("</div></div>")
file.close()

# 24. PsychCrunch
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseExample24" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
if parser[24] is not None:
    for x in parser[24].find_all("div", class_="libsyn-item-title"):
        for z in x.find_all("a"):
            registrar_link(file, str(z.get("href")), z.text.strip(), "PsychCrunch")
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
        # Adiciona a tradução opcional se o termo estiver em inglês
        traducao = traduzir_texto(texto_limpo)
        if traducao and traducao != texto_limpo:
            file.write(f'<span style="font-size:0.80rem; color:#6c757d; display:block; margin-bottom:8px;">↳ {traducao}</span>')
        # Filtro de Palavras-Chave integrado
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

# Inserção do bloco de Palavras-Chave Ativas no mesmo padrão estrito dos botões Bootstrap
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
print("Sucesso! O script concluiu a compilação do design original.")

