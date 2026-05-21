import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- 1. CONFIGURAÇÕES DE TEMPO, ARQUIVOS E TRADUTOR ---
data_e_hora_atuais = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# Carrega palavras-chave do arquivo keywords.txt de forma segura
def carregar_keywords():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

keywords = carregar_keywords()
noticias_filtradas_urgentes = []

# Função auxiliar de tradução estável
def traduzir_texto(texto):
    if not texto or len(texto) < 12: return ""
    try: return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return ""

# --- 2. CONFIGURAÇÃO DOS LINKS E CABEÇALHOS ORIGINAIS ---
links = [
    "https://verywellmind.com", "https://psychologytoday.com", 
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
    "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://bigthink.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

responder = [None] * len(links)
parser = [None] * len(links)

print("Iniciando varredura dos portais...")
for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
        time.sleep(0.1)  # Pausa sutil de estabilidade
    except Exception as e:
        print(f"Aviso: Falha ao carregar o link {links[x]}")

# --- 3. CRIAÇÃO DO ARQUIVO HTML (ESTRUTURA DE DESIGN IDÊNTICA AO SEU ANEXO) ---
file = open(namefile, "w", encoding="utf-8")
file.write('<!DOCTYPE html>')
file.write('<html lang="pt-br">')
file.write('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
file.write('<title>PSI LINKS BOARD</title>')
# Mantém seus espaçamentos e adiciona o estilo da legenda cinza menor abaixo do link e o botão dinâmico de topo
file.write('''<style>
    .btn-space { margin: 4px; }
    .sub-tra { font-size: 0.82rem; color: #6c757d; display: block; margin-bottom: 8px; margin-left: 10px; }
    #btnVoltarTopo { position: fixed; bottom: 20px; right: 20px; display: none; z-index: 99; border: none; background-color: #17a2b8; color: white; padding: 10px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.15); }
</style>''')
file.write('</head>')

# Inicialização do Body e Container exatamente como na sua imagem
file.write('<body><button onclick="irParaOTopo()" id="btnVoltarTopo">▲ Voltar ao Topo</button><div class="container-fluid px-4" id="myGroup">')
file.write(f'<h1>PSI MONITOR <small class="text-muted" style="font-size: 0.45em; margin-left: 10px;">• Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</small></h1><p>')

# CRIAÇÃO DA GRADE DE BOXES FIXOS (Idêntica à sua imagem enviada)
file.write('<a class="btn btn-space btn-danger btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseKeywords">🎯 PALAVRAS-CHAVE ATIVAS</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample0" role="button" aria-expanded="false">VeryWell Mind</a>')
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

# --- 4. CRIAÇÃO DAS CAIXAS DE CONTEÚDO (TODAS NATIVAS E FECHADAS POR PADRÃO) ---

def gravar_links_com_traducao(html_id, links_encontrados, url_base, fonte_nome):
    """Função interna para manter a escrita limpa e alimentar o filtro de keywords"""
    f = open(namefile, "a", encoding="utf-8")
    f.write(f'<div class="collapse" id="{html_id}" data-parent="#myGroup" Style><div class="card card-body">')
    vistos = set()
    for item_a in links_encontrados:
        href = item_a.get("href", "")
        texto = item_a.get_text().strip()
        if not href or len(texto) < 14: continue
        if href.startswith("/"): href = url_base.rstrip('/') + href
        if href not in vistos:
            vistos.add(href)
            f.write(f'<a href="{href}" target="_blank">{texto}</a></br>')
            trad = traduzir_texto(texto)
            if trad and trad != texto:
                f.write(f'<span class="sub-tra">↳ {trad}</span>')
            if any(p in texto.lower() or p in trad.lower() for p in keywords):
                noticias_filtradas_urgentes.append((href, texto, trad, fonte_nome))
    f.write('</div></div>')
    f.close()

# 0. VeryWell Mind (Corrigido dinâmico)
if parser[0] is not None:
    items = parser[0].find_all("a", class_=lambda c: c and ('card' in c or 'link' in c))[:12]
    gravar_links_com_traducao("collapseExample", items, "https://verywellmind.com", "VeryWell Mind")

# 1. Psychology Today
if parser[1] is not None:
    items = []
    for x in parser[1].find_all("div", class_="layout-content-main"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample1", items, "https://psychologytoday.com", "Psychology Today")

# 2. Scientific American
if parser[2] is not None:
    items = []
    for x in parser[2].find_all("div", class_="articleList-CcaLz root-fREBs"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample2", items, "https://scientificamerican.com", "Scientific American")

# 3. NIMH
if parser[3] is not None:
    items = []
    for x in parser[3].find_all("article"):
        items.extend(x.find_all("a", class_="aggregated_term_news_link"))
    gravar_links_com_traducao("collapseExample3", items, "https://nih.gov", "NIMH")

# 4. APA PsyPort
if parser[4] is not None:
    items = []
    for x in parser[4].find_all("article"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample4", items, "", "APA PsyPort")

# 5. APA Monitor
if parser[5] is not None:
    items = []
    for x in parser[5].find_all("section", class_="linkWidget tile square"):
        for z in x.find_all("p", class_="title"):
            items.extend(z.find_all("a"))
    gravar_links_com_traducao("collapseExample5", items, "https://apa.org", "APA Monitor")

# 6. Google Notícias
if parser[6] is not None:
    items = []
    for x in parser[6].find_all("article"):
        items.extend(x.find_all("a", class_="VDXfz"))
    gravar_links_com_traducao("collapseExample6", items, "https://google.com", "Google Notícias")

# 7. SBP
if parser[7] is not None:
    items = []
    for x in parser[7].find_all("div", class_="content list"):
        for z in x.find_all("p"):
            items.extend(z.find_all("a"))
    gravar_links_com_traducao("collapseExample7", items, "https://sbponline.org.br", "SBP")

# 8. Neuroscience
if parser[8] is not None:
    items = []
    for x in parser[8].find_all("h3"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample8", items, "", "Neuroscience")

# 9. Positive Psychology
if parser[9] is not None:
    items = parser[9].find_all("a")
    gravar_links_com_traducao("collapseExample9", items, "", "Positive Psychology")

# 10. Positive Psychcentral
if parser[10] is not None:
    items = []
    for x in parser[10].find_all("div", class_="css-fdjy12"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample10", items, "https://psychcentral.com", "Psychcentral")

# 11. IQ's Corner
if parser[11] is not None:
    items = []
    for x in parser[11].find_all("h3"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample11", items, "", "IQ's Corner")

# 12. Happier Human
if parser[12] is not None:
    items = []
    for x in parser[12].find_all("h2"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample12", items, "", "Happier Human")

# 13. PsyNewsDaily
if parser[13] is not None:
    items = []
    for x in parser[13].find_all("h2"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample13", items, "", "PsyNewsDaily")

# 14. Psychiatric Times
if parser[14] is not None:
    items = parser[14].find_all("a")
    gravar_links_com_traducao("collapseExample14", items, "https://psychiatrictimes.com", "Psychiatric Times")

# 15. APS
if parser[15] is not None:
    items = []
    for x in parser[15].find_all("h3"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample15", items, "", "APS")

# 16. CFP
if parser[16] is not None:
    items = []
    for x in parser[16].find_all("h3"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample16", items, "", "CFP")

# 17. Psicologia USP
if parser[17] is not None:
    items = parser[17].find_all("a")
    gravar_links_com_traducao("collapseExample17", items, "https://scielo.br", "Psicologia USP")

# 18. Conselho Regional de Psicologia SP
if parser[18] is not None:
    items = parser[18].find_all("a")
    gravar_links_com_traducao("collapseExample18", items, "", "CRP-SP")

# 19. El País Psicologia
if parser[19] is not None:
    items = []
    for x in parser[19].find_all("h2"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample19", items, "https://elpais.com", "El País")

# 20. G1 Saúde Mental
if parser[20] is not None:
    items = []
    for x in parser[20].find_all("div", class_="_evt"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample20", items, "", "G1")

# 21. Medical Xpress
if parser[21] is not None:
    items = []
    for x in parser[21].find_all("div"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample21", items, "", "Medical Xpress")

# 22. Psychreg
if parser[22] is not None:
    items = []
    for x in parser[22].find_all("div", class_="col-md-4"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample22", items, "", "Psychreg")

# 23. Folha Equilíbrio Mente
if parser[23] is not None:
    items = parser[23].find_all("a")
    gravar_links_com_traducao("collapseExample23", items, "", "Folha")

# 24. PsychCrunch
if parser[24] is not None:
    items = []
    for x in parser[24].find_all("div", class_="libsyn-item-title"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample24", items, "", "PsychCrunch")

# 25 a 28. A Mente é Maravilhosa (Estrutura Unificada Nativa)
base_amm = "https://amenteemaravilhosa.com.br"
class_amm = "jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"
if parser[25] is not None:
    gravar_links_com_traducao("collapseExample25", parser[25].find_all("a", class_=class_amm), base_amm, "AMM Neuro")
if parser[26] is not None:
    gravar_links_com_traducao("collapseExample26", parser[26].find_all("a", class_=class_amm), base_amm, "AMM Psico")
if parser[27] is not None:
    gravar_links_com_traducao("collapseExample27", parser[27].find_all("a", class_=class_amm), base_amm, "AMM Rel")
if parser[28] is not None:
    gravar_links_com_traducao("collapseExample28", parser[28].find_all("a", class_=class_amm), base_amm, "AMM Saúde")

# 29. Big Think
if parser[29] is not None:
    items = []
    for x in parser[29].find_all("h1", class_="card-headline"):
        items.extend(x.find_all("a"))
    gravar_links_com_traducao("collapseExample29", items, "", "Big Think")

# --- 5. GRAVAÇÃO DA CAIXA DE PALAVRAS-CHAVE E SCRIPT DE FECHAMENTO ---
file = open(namefile, "a", encoding="utf-8")
file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup" Style><div class="card card-body bg-light">')
file.write(f'<p class="text-muted small">Termos monitorados ativos: {", ".join(keywords)}</p>')

if not noticias_filtradas_urgentes:
    file.write('<p class="text-muted">Nenhum artigo correspondente encontrado nas últimas varreduras.</p>')
else:
    for url, orig, trad, fonte in noticias_filtradas_urgentes:
        file.write(f'<a href="{url}" target="_blank">📌 [{fonte}] {orig}</a></br>')
        if trad and trad != orig:
            file.write(f'<span class="sub-tra">↳ Tradução: {trad}</span>')
file.write('</div></div>')

# Rodapé de scripts Bootstrap originais e lógica dinâmica do topo
file.write('''<div>
<script src="https://jquery.com"></script>
<script src="https://cloudflare.com"></script>
<script src="https://bootstrapcdn.com"></script>
<script>
    window.onscroll = function() {
        var btn = document.getElementById("btnVoltarTopo");
        if (document.body.scrollTop > 180 || document.documentElement.scrollTop > 180) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    };
    function irParaOTopo() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    }
</script>
</div></body></html>''')
file.close()

print("Sucesso! index.html compilado com o design estrito exato da foto.")
