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
    {"nome": "VeryWell Mind", "url": "https://verywellmind.com", "base": "https://verywellmind.com", "find": ["a", {"class": lambda c: c and ('card' in c or 'link' in c)}], "sub_find": None},
    {"nome": "Psychology Today", "url": "https://psychologytoday.com", "base": "https://psychologytoday.com", "find": ["div", {"class": "layout-content-main"}], "sub_find": "a"},
    {"nome": "Scientific American", "url": "https://scientificamerican.com", "base": "https://scientificamerican.com", "find": ["div", {"class": "articleList-CcaLz root-fREBs"}], "sub_find": "a"},
    {"nome": "NIMH Research", "url": "https://nih.gov", "base": "https://nih.gov", "find": ["a", {"class": "aggregated_term_news_link"}], "sub_find": None},
    {"nome": "APA PsyPort", "url": "https://apa.org", "base": "", "find": ["article"], "sub_find": "a"},
    {"nome": "APA Monitor", "url": "https://apa.org", "base": "https://apa.org", "find": ["p", {"class": "title"}], "sub_find": "a"},
    {"nome": "Google Notícias", "url": "https://google.com", "base": "https://google.com", "find": ["a", {"class": "VDXfz"}], "sub_find": None},
    {"nome": "SBP Notícias", "url": "https://sbponline.org.br", "base": "https://sbponline.org.br", "find": ["div", {"class": "content list"}], "sub_find": "a"},
    {"nome": "Neuroscience News", "url": "https://neurosciencenews.com", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Positive Psychology", "url": "https://positivepsychology.com", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Psych Central", "url": "https://psychcentral.com", "base": "https://psychcentral.com", "find": ["div", {"class": "css-fdjy12"}], "sub_find": "a"},
    {"nome": "IQ's Corner", "url": "http://iqscorner.com", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Happier Human", "url": "https://happierhuman.com", "base": "", "find": ["h2"], "sub_find": "a"},
    {"nome": "PsyNewsDaily", "url": "https://psychnewsdaily.com", "base": "", "find": ["h2"], "sub_find": "a"},
    {"nome": "Psychiatric Times", "url": "https://psychiatrictimes.com", "base": "https://psychiatrictimes.com", "find": ["h2"], "sub_find": "a"},
    {"nome": "APS Insights", "url": "https://psychologicalscience.org", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "CFP", "url": "https://cfp.org.br", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "Psicologia USP", "url": "https://scielo.br", "base": "https://scielo.br", "find": ["h3"], "sub_find": "a"},
    {"nome": "CRP-SP Impresso", "url": "https://crpsp.org", "base": "", "find": ["h3"], "sub_find": "a"},
    {"nome": "El País Psicologia", "url": "https://elpais.com", "base": "https://elpais.com", "find": ["h2"], "sub_find": "a"},
    {"nome": "G1 Saúde Mental", "url": "https://globo.com", "base": "", "find": ["div", {"class": "_evt"}], "sub_find": "a"},
    {"nome": "Medical Xpress", "url": "https://medicalxpress.com", "base": "", "find": ["div", {"class": "sorted-news-list"}], "sub_find": "a"},
    {"nome": "Psychreg", "url": "https://psychreg.org", "base": "", "find": ["div", {"class": "col-md-4"}], "sub_find": "a"},
    {"nome": "Folha Mente", "url": "https://uol.com.br", "base": "", "find": ["h2"], "sub_find": "a"},
    {"nome": "PsychCrunch Podcast", "url": "https://libsyn.com", "base": "", "find": ["div", {"class": "libsyn-item-title"}], "sub_find": "a"},
    {"nome": "A Mente é Maravilhosa - Neuro", "url": "https://amenteemaravilhosa.com.br", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa - Psico", "url": "https://amenteemaravilhosa.com.br", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa - Rel", "url": "https://amenteemaravilhosa.com.br", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "A Mente é Maravilhosa - Saúde", "url": "https://amenteemaravilhosa.com.br", "base": "https://amenteemaravilhosa.com.br", "find": ["a", {"class": "global-link"}], "sub_find": None},
    {"nome": "Big Think", "url": "https://bigthink.com", "base": "", "find": ["h1", {"class": "card-headline"}], "sub_find": "a"}
]

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for idx, config in enumerate(fontes_config):
    print(f"[{idx+1}/{len(fontes_config)}] Capturando: {config['nome']}")
    links_site = []
    vistos = set()
    
    try:
        res = requests.get(config["url"], headers=header, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            
            find_args = config["find"]
            if len(find_args) == 2 and isinstance(find_args, dict):
                elementos_pai = soup.find_all(find_args, find_args)
            else:
                elementos_pai = soup.find_all(find_args)
            
            if not elementos_pai:
                elementos_pai = soup.find_all(['h2', 'h3', 'article'])
                config["sub_find"] = "a" if elementos_pai and elementos_pai.name != "a" else None
            
            for elem in elementos_pai:
                tags_a = elem.find_all(config["sub_find"]) if config["sub_find"] else [elem] if elem.name == "a" else []
                
                for a in tags_a:
                    href = a.get("href", "")
                    texto = a.get_text().strip()
                    
                    if not href or len(texto) < 14: continue
                    if href.startswith("/"): href = config["base"].rstrip('/') + href
                    if not href.startswith("http"): continue
                    
                    if href not in vistos:
                        vistos.add(href)
                        traducao = traduzir(texto)
                        item = {"url": href, "texto": texto, "traducao": traducao}
                        links_site.append(item)
                        
                        if any(p in texto.lower() or p in traducao.lower() for p in keywords):
                            noticias_filtradas_urgentes.append({**item, "fonte": config["nome"]})
                            
        time.sleep(0.3)
    except Exception as e:
        print(f"Erro em {config['nome']}: {e}")
        
    # Correção do erro de digitação (dados_panel -> dados_painel)
    dados_painel.append({"nome": config["nome"], "noticias": links_site[:12]})

# --- RENDERIZAÇÃO NO DESIGN TRADICIONAL CORRIGIDO E HARMÔNICO ---
with open(namefile, "w", encoding="utf-8") as file:
    file.write('''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://bootstrapcdn.com">
    <title>PSI LINKS BOARD</title>
    <style>
        body { background-color: #f5f6f8; color: #212529; }
        .header-premium { background-color: #1a2530; color: #ffffff; padding: 20px; border-radius: 4px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .btn-space { margin: 4px; }
        .sub-tra { font-size: 0.82rem; color: #6c757d; display: block; margin-bottom: 10px; margin-left: 15px; }
        #btnVoltarTopo { position: fixed; bottom: 20px; right: 20px; display: none; z-index: 99; border: none; outline: none; background-color: #1a2530; color: white; cursor: pointer; padding: 12px 18px; border-radius: 30px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2); transition: all 0.2s; }
        #btnVoltarTopo:hover { background-color: #3182ce; transform: translateY(-2px); }
    </style>
</head>
<body>
    <button onclick="irParaOTopo()" id="btnVoltarTopo" title="Voltar ao topo">▲ Voltar ao Topo</button>

    <div class="container" id="myGroup">
        <div class="header-premium mt-3">
            <h1 style="margin:0; font-size:2rem; font-weight:700; letter-spacing:-0.5px;">PSI MONITOR</h1>''')
            
    file.write(f'<p style="margin:5px 0 0 0; color:#a0aec0; font-size:0.9rem;">Última raspagem realizada em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</p></div>')

    file.write('<p>\n')
    file.write('<a class="btn btn-space btn-primary btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseKeywords">🎯 PALAVRAS-CHAVE ATIVAS</a>\n')
    for i, site in enumerate(dados_painel):
        classe_status = "btn-outline-danger" if not site["noticias"] else "btn-outline-info"
        file.write(f'<a class="btn btn-space {classe_status} btn-lg" data-toggle="collapse" href="#collapseIndex{i}" role="button" aria-expanded="false" aria-controls="collapseIndex{i}">{site["nome"]}</a>\n')
    file.write('</p>\n')

    file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup"><div class="card card-body bg-light">')
    file.write(f'<p class="text-muted small">Termos ativos monitorados: {", ".join(keywords)}</p>')
    if not noticias_filtradas_urgentes:
        file.write('<p class="text-muted">Nenhum artigo correspondente encontrado.</p>')
    else:
        for n in noticias_filtradas_urgentes:
            file.write(f'<a href="{n["url"]}" target="_blank">📌 [{n["fonte"]}] {n["texto"]}</a></br>\n')
            if n["traducao"] and n["traducao"] != n["texto"]:
                file.write(f'<span class="sub-tra">↳ Tradução: {n["traducao"]}</span>\n')
    file.write('</div></div>\n')

    for i, site in enumerate(dados_painel):
        classe_show = "collapse show" if i == 0 else "collapse"
        file.write(f'<div class="{classe_show}" id="collapseIndex{i}" data-parent="#myGroup" Style>\n')
        file.write('<div class="card card-body">\n')
        
        if not site["noticias"]:
            file.write('<p class="text-muted">Nenhum artigo relevante capturado nesta rodada.</p>\n')
        else:
            for n in site["noticias"]:
                file.write(f'<a href="{n["url"]}" target="_blank">{n["texto"]}</a></br>\n')
                if n["traducao"] and n["traducao"] != n["texto"]:
                    file.write(f'<span class="sub-tra">↳ {n["traducao"]}</span>\n')
                    
        file.write('</div></div>\n')

    file.write('''</div>
    <div>
    <script src="https://jquery.com"></script>
    <script src="https://cloudflare.com"></script>
    <script src="https://bootstrapcdn.com"></script>
    
    <script>
        window.onscroll = function() { verificarRolagem() };

        function verificarRolagem() {
            var botao = document.getElementById("btnVoltarTopo");
            if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
                botao.style.display = "block";
            } else {
                botao.style.display = "none";
            }
        }

        function irParaOTopo() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
    </script>
    </div>
</body>
</html>''')

print("Fidelidade original restaurada com paleta premium harmônica.")
