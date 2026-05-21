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
    print(f"[{idx+1}/30] Coletando: {config['nome']}")
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

# --- RENDERIZAÇÃO NO DESIGN TRADICIONAL ULTRA-ELEGANTE E EM CAIXA ---
with open(namefile, "w", encoding="utf-8") as file:
    file.write('''<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://bootstrapcdn.com">
    <title>PSI LINKS BOARD</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding-bottom: 60px; }
        
        /* Box do Topo Elegante Dark */
        .box-header { background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-top: 25px; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
        .box-header h1 { font-size: 1.8rem; font-weight: 800; color: #38bdf8; margin: 0; letter-spacing: -0.5px; }
        .box-header p { margin: 6px 0 0 0; color: #94a3b8; font-size: 0.9rem; }
        
        /* Estilização da Grade de Botões Tradicionais */
        .btn-space { margin: 4px; font-size: 0.88rem; font-weight: 600; border-radius: 6px; padding: 8px 16px; transition: all 0.2s; text-transform: uppercase; letter-spacing: 0.2px; }
        .btn-outline-info { color: #38bdf8; border-color: #38bdf8; }
        .btn-outline-info:hover, .btn-outline-info:not(:disabled):not(.disabled):active { background-color: #38bdf8; color: #0f172a; border-color: #38bdf8; }
        .btn-outline-danger { color: #f87171; border-color: #f87171; }
        .btn-outline-danger:hover { background-color: #f87171; color: #0f172a; border-color: #f87171; }
        
        /* Apresentação das Notícias em Caixas/Boxes Premium */
        .box-conteudo { background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-top: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
        .box-conteudo-titulo { font-size: 1.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        
        /* Links e Traduções organizados */
        .item-noticia { padding: 10px 0; border-bottom: 1px solid #334155; display: block; }
        .item-noticia:last-child { border-bottom: none; }
        .link-noticia { font-size: 1.02rem; font-weight: 500; color: #f1f5f9; text-decoration: none; transition: color 0.15s; }
        .link-noticia:hover { color: #38bdf8; text-decoration: none; }
        .sub-tra { font-size: 0.85rem; color: #94a3b8; display: block; margin-top: 4px; padding-left: 12px; border-left: 2px solid #475569; font-style: italic; }
        
        /* Link Voltar ao Topo Interno e Dinâmico */
        .link-topo { font-size: 0.82rem; color: #94a3b8; cursor: pointer; font-weight: 600; text-transform: uppercase; }
        .link-topo:hover { color: #38bdf8; }
        #btnVoltarTopo { position: fixed; bottom: 25px; right: 25px; display: none; z-index: 99; border: none; background-color: #38bdf8; color: #0f172a; padding: 10px 18px; border-radius: 30px; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); cursor: pointer; transition: all 0.2s; }
        #btnVoltarTopo:hover { transform: translateY(-2px); background-color: #bae6fd; }
    </style></head>''')
    
    file.write('<body><button onclick="irParaOTopo()" id="btnVoltarTopo">▲ Voltar ao Topo</button>')
    file.write('<div class="container" id="myGroup">')
    
    # 1. Caixa de Cabeçalho com o Horário e Dia Destacados
    file.write('<div class="box-header"><h1>PSI MONITOR</h1>')
    file.write(f'<p>📅 Varredura sistêmica executada em: <strong>{data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</strong></p></div><p>')
    
    # Grade Horizontal Original de Botões (Preservando 100% da sua disposição preferida)
    file.write('<a class="btn btn-space btn-danger btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseKeywords">🎯 PALAVRAS-CHAVE ATIVAS</a>')
    for i, site in enumerate(dados_painel):
        classe_btn = "btn-outline-danger" if not site["noticias"] else "btn-outline-info"
        file.write(f'<a class="btn btn-space {classe_btn} btn-lg" data-toggle="collapse" href="#collapseIndex{i}" role="button" aria-expanded="false">{site["nome"]}</a>')
    file.write('</p>')

    # 2. Apresentação das Listas dentro dos "Boxes Elegantes" (Collapse Card-Body Original Estilizado)
    
    # Box Elegante de Palavras-Chave
    file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup"><div class="box-conteudo">')
    file.write(f'<div class="box-conteudo-titulo"><span>🎯 Artigos Filtrados (Keywords: {", ".join(keywords)})</span><span class="link-topo" onclick="irParaOTopo()">▲ Voltar</span></div>')
    if not noticias_filtradas_urgentes:
        file.write('<p class="text-muted">Nenhum artigo de interesse detectado na varredura recente.</p>')
    else:
        for n in noticias_filtradas_urgentes:
            file.write(f'<div class="item-noticia"><a class="link-noticia" href="{n["url"]}" target="_blank">📌 [{n["fonte"]}] {n["texto"]}</a>')
            if n["traducao"] and n["traducao"] != n["texto"]:
                file.write(f'<span class="sub-tra">↳ Tradução: {n["traducao"]}</span>')
            file.write('</div>')
    file.write('</div></div>')

    # Boxes Elegantes de cada Portal Individual
    for i, site in enumerate(dados_painel):
        classe_show = "collapse show" if i == 0 else "collapse"
        file.write(f'<div class="{classe_show}" id="collapseIndex{i}" data-parent="#myGroup"><div class="box-conteudo">')
        file.write(f'<div class="box-conteudo-titulo"><span>🌐 {site["nome"]}</span><span class="link-topo" onclick="irParaOTopo()">▲ Voltar ao Topo</span></div>')
        
        if not site["noticias"]:
            file.write('<p class="text-muted">Nenhum link pôde ser extraído na execução atual.</p>')
        else:
            for n in site["noticias"]:
                file.write(f'<div class="item-noticia"><a class="link-noticia" href="{n["url"]}" target="_blank">🔗 {n["texto"]}</a>')
                if n["traducao"] and n["traducao"] != n["texto"]:
                    file.write(f'<span class="sub-tra">↳ {n["traducao"]}</span>')
                file.write('</div>')
                    
        file.write('</div></div>')

    # Fechamento com os scripts e a lógica dinâmica de rolagem
    file.write('''</div><div>
    <script src="https://jquery.com"></script>
    <script src="https://cloudflare.com"></script>
    <script src="https://bootstrapcdn.com"></script>
    <script>
        window.onscroll = function() {
            var btn = document.getElementById("btnVoltarTopo");
            if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
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

print("Sucesso! Painel gerado com layout em caixas escuras harmônicas de alta fidelidade.")
