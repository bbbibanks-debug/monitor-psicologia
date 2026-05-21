import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÕES DE TEMPO E ARQUIVOS ---
data_e_hora_sao_paulo = datetime.now(timezone(timedelta(hours=-3)))
namefile = "index.html"

def carregar_keywords():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

keywords = carregar_keywords()
noticias_filtradas_urgentes = []
dados_painel = []

def traduzir(texto):
    if not texto or len(texto) < 12: return ""
    try: return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return ""

# --- MAPEAMENTO DA ARQUITETURA DE RASPAGEM ORIGINAL ---
fontes_config = [
    {"nome": "VeryWell Mind", "base": "https://verywellmind.com", "find": ["a", {"class": lambda c: c and ('card' in c or 'link' in c)}], "sub_find": None},
    {"nome": "Psychology Today", "base": "https://psychologytoday.com", "find": ["div", {"class": "layout-content-main"}], "sub_find": "a"},
    {"nome": "Scientific American", "base": "https://scientificamerican.com", "find": ["div", {"class": "articleList-CcaLz root-fREBs"}], "sub_find": "a"},
    {"nome": "The National Institute of Mental Health (NIMH)", "base": "https://nih.gov", "find": ["article"], "sub_find": "a", "sub_class": "aggregated_term_news_link"},
    {"nome": "APA PsyPort", "base": "", "find": ["article"], "sub_find": "a"},
    {"nome": "APA Monitor", "base": "https://apa.org", "find": ["section", {"class": "linkWidget tile square"}], "sub_find": "p", "sub_class": "title"},
    {"nome": "Google Notícias", "base": "https://google.com", "find": ["article"], "sub_find": "a", "sub_class": "VDXfz"},
    {"nome": "SBP", "base": "https://sbponline.org.br", "find": ["div", {"class": "content list"}], "sub_find": "a"},
    {"nome": "Neuroscience", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Positive Psychology", "base": "", "find": ["a"], "sub_find": "h3", "invert": True},
    {"nome": "Positive Psychcentral", "base": "https://psychcentral.com", "find": ["div", {"class": "css-fdjy12"}], "sub_find": "a"},
    {"nome": "IQ`s Corner", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Happier Human", "base": "", "find": ["h2"], "sub_find": "a"},
    {"nome": "PsyNewsDaily", "base": "", "find": ["h2"], "sub_find": "a"},
    {"nome": "Psychiatric Times", "base": "https://psychiatrictimes.com", "find": ["a"], "sub_find": "h2", "invert": True},
    {"nome": "APS", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "CFP", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Psicologia USP", "base": "https://scielo.br", "find": ["a"], "sub_find": "h3", "invert": True},
    {"nome": "Conselho Regional de Psicologia SP", "base": "", "find": ["a"], "sub_find": "h3", "invert": True},
    {"nome": "El País Psicologia", "base": "https://elpais.com", "find": ["h2"], "sub_find": "a"},
    {"nome": "G1 Saúde Mental", "base": "", "find": ["div", {"class": "_evt"}], "sub_find": "a"},
    {"nome": "Medical Xpress", "base": "", "find": ["div"], "sub_find": "a"},
    {"nome": "Psychreg", "base": "", "find": ["div", {"class": "col-md-4"}], "sub_find": "a"},
    {"nome": "Folha Equilíbrio Mente", "base": "", "find": ["a"], "sub_find": "h2", "invert": True},
    {"nome": "PsychCrunch", "base": "", "find": ["div", {"class": "libsyn-item-title"}], "sub_find": "a"},
    {"nome": "A Mente é Maravilhosa-Neurociência", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa-Psicologia", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa-Relações", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa-Saúde", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "Big Think", "base": "", "find": ["h1", {"class": "card-headline"}], "sub_find": "a"}
]

links_originais = [
    "https://verywellmind.com/", "https://psychologytoday.com", 
    "https://scientificamerican.com/mind-and-brain/", "https://nih.gov/news/research-highlights",
    "https://apa.org/news/psycport", "https://apa.org/monitor", 
    "https://google.com/search?q=psicologia&hl=pt-BR&gl=BR&ceid=BR%3Apt-419", "https://sbponline.org.br/noticias", 
    "https://neurosciencenews.com", "https://positivepsychology.com", "https://psychcentral.com",
    "http://iqscorner.com", "https://happierhuman.com", "https://psychnewsdaily.com", 
    "https://psychiatrictimes.com/", "https://psychologicalscience.org", "https://cfp.org.br", 
    "https://scielo.br/j/pusp/", "https://crpsp.org", "https://elpais.com/noticias/psicologia/", 
    "https://globo.com", "https://medicalxpress.com", "https://psychreg.org", 
    "https://uol.com.br", "https://libsyn.com", "https://amenteemaravilhosa.com.br", 
    "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", 
    "https://bigthink.com"
]

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for idx, config in enumerate(fontes_config):
    url_alvo = links_originais[idx]
    links_site = []
    vistos = set()
    
    try:
        res = requests.get(url_alvo, headers=header, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            find_args = config["find"]
            elementos = soup.find_all(find_args, find_args) if len(find_args) == 2 and isinstance(find_args, dict) else soup.find_all(find_args)
                
            for elem in elementos:
                if config.get("invert"):
                    tags_a = [elem] if elem.name == "a" else []
                    texto_nodo = elem.find(config["sub_find"])
                    texto = texto_nodo.get_text().strip() if texto_nodo else elem.get_text().strip()
                else:
                    tags_a = elem.find_all(config["sub_find"], class_=config["sub_class"]) if "sub_class" in config else elem.find_all(config["sub_find"]) if config["sub_find"] else [elem] if elem.name == "a" else []
                    texto = None
                
                for a in tags_a:
                    href = a.get("href", "")
                    if not texto: texto = a.get_text().strip()
                    if not href or len(texto) < 14: continue
                    
                    if href.startswith("/"):
                        href = config["base"].rstrip('/') + href if config["base"] else url_alvo.rstrip('/') + href
                    elif not href.startswith("http") and idx == 1:
                        href = url_alvo + href
                    
                    if href not in vistos:
                        vistos.add(href)
                        traducao = traduzir(texto)
                        item = {"url": href, "texto": texto, "traducao": traducao}
                        links_site.append(item)
                        if any(p in texto.lower() or p in traducao.lower() for p in keywords):
                            noticias_filtradas_urgentes.append({**item, "fonte": config["nome"]})
        time.sleep(0.1)
    except Exception:
        pass
    dados_painel.append({"nome": config["nome"], "noticias": links_site[:12]})

# --- RENDERIZAÇÃO ESTREITA E COMPACTA NO SEU DESIGN NATIVO ORIGINAL CORRIGIDO ---
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
    file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
    file.write('<title>PSI LINKS BOARD</title>')
    file.write('''<style>
        body { background-color: #f8fafc; color: #1e293b; padding-top: 20px; padding-bottom: 60px; }
        .btn-space { margin: 4px; border-radius: 4px; font-weight: 600; padding: 10px 18px; text-decoration: none !important; }
        .card-body { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; margin-top: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .box-title-inner { font-size: 1.25rem; font-weight: 700; color: #0b516f; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; display: flex; justify-content: space-between; }
        .sub-tra { font-size: 0.83rem; color: #64748b; display: block; margin-bottom: 12px; margin-left: 12px; font-style: italic; }
        .link-topo-inner { font-size: 0.8rem; color: #64748b; cursor: pointer; text-transform: uppercase; font-weight: 700; }
        .link-topo-inner:hover { color: #0b516f; }
        #btnVoltarTopo { position: fixed; bottom: 25px; right: 25px; display: none; z-index: 99; border: none; background-color: #0b516f; color: white; padding: 12px 20px; border-radius: 30px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.15); cursor: pointer; }
    </style></head>''')
    
    file.write('<body><button onclick="irParaOTopo()" id="btnVoltarTopo">▲ Voltar ao Topo</button>')
    file.write('<div class="container-fluid px-4" id="myGroup">')
    
    # Cabeçalho original harmônico com cor estável
    file.write(f'<h1 class="font-weight-bold" style="color:#0b516f; font-size: 2.2rem; letter-spacing:-0.5px;">PSI MONITOR <span class="text-muted" style="font-size:0.95rem; font-weight:normal; margin-left:12px;">• Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</span></h1><hr><p>')
    
    # RESTAURAÇÃO COMPLETA DOS BOXES FIXOS DO BOOTSTRAP (Classes btn nativas que geram o box)
    file.write('<a class="btn btn-space btn-danger btn-lg shadow-sm" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseKeywords">🎯 PALAVRAS-CHAVE ATIVAS</a>')
    for i, site in enumerate(dados_painel):
        classe_btn = "btn-outline-danger" if not site["noticias"] else "btn-outline-info"
        file.write(f'<a class="btn btn-space {classe_btn} btn-lg shadow-sm" data-toggle="collapse" href="#collapseIndex{i}" role="button" aria-expanded="false">{site["nome"]}</a>')
    file.write('</p>')

    # --- SETOR DE CAIXAS TOTALMENTE FECHADAS POR PADRÃO (Sem a classe 'show') ---
    
    # Caixa Palavras-Chave (Totalmente Fechada)
    file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup"><div class="card card-body">')
    file.write(f'<div class="box-title-inner"><span>🎯 Palavras-Chave ({", ".join(keywords)})</span><span class="link-topo-inner" onclick="irParaOTopo()">▲ Subir</span></div>')
    if not noticias_filtradas_urgentes:
        file.write('<p class="text-muted">Nenhum artigo correspondente encontrado.</p>')
    else:
        for n in noticias_filtradas_urgentes:
            file.write(f'<a href="{n["url"]}" target="_blank" class="font-weight-bold" style="color:#0b516f;">📌 [{n["fonte"]}] {n["texto"]}</a></br>\n')
            if n["traducao"] and n["traducao"] != n["texto"]:
                file.write(f'<span class="sub-tra">↳ Tradução: {n["traducao"]}</span>\n')
    file.write('</div></div>\n')

    # As 30 Janelas dos Portais (Todas "collapse" puras, nascem 100% FECHADAS)
    for i, site in enumerate(dados_painel):
        file.write(f'<div class="collapse" id="collapseIndex{i}" data-parent="#myGroup" Style><div class="card card-body">\n')
        file.write(f'<div class="box-title-inner"><span>🌐 {site["nome"]}</span><span class="link-topo-inner" onclick="irParaOTopo()">▲ Voltar ao Topo</span></div>')
        
        if not site["noticias"]:
            file.write('<p class="text-muted">Nenhum artigo relevante capturado nesta rodada.</p>\n')
        else:
            for n in site["noticias"]:
                file.write(f'<a href="{n["url"]}" target="_blank" style="color:#1e293b; font-weight:500; font-size:1.05rem;">🔗 {n["texto"]}</a></br>\n')
                if n["traducao"] and n["traducao"] != n["texto"]:
                    file.write(f'<span class="sub-tra">↳ {n["traducao"]}</span>\n')
                    
        file.write('</div></div>\n')

    file.write('''</div><div>
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

print("Sucesso! O design dos boxes fixos e fechados foi 100% corrigido.")
