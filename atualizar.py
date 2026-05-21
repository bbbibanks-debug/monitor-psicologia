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

# Carrega palavras-chave do arquivo de texto de forma segura
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

# --- SELETORES CIRÚRGICOS DO SEU SCRIPT ORIGINAL ANEXADO ---
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

# URLs exatas mapeadas do seu PDF original
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

# Executa raspagem em array na memória (Garante eficiência total)
for idx, config in enumerate(fontes_config):
    url_alvo = links_originais[idx]
    print(f"[{idx+1}/30] Extraindo do formato original: {config['nome']}")
    links_site = []
    vistos = set()
    
    try:
        res = requests.get(url_alvo, headers=header, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            
            # Executa a regra exata mapeada da sua folha original
            find_args = config["find"]
            if len(find_args) == 2 and isinstance(find_args[1], dict):
                elementos = soup.find_all(find_args[0], find_args[1])
            else:
                elementos = soup.find_all(find_args[0])
                
            for elem in elementos:
                # Trata as inversões ou sub-achados de tags h2/h3/a nativos
                if config.get("invert"):
                    tags_a = [elem] if elem.name == "a" else []
                    texto_nodo = elem.find(config["sub_find"])
                    texto = texto_nodo.get_text().strip() if texto_nodo else elem.get_text().strip()
                else:
                    if config["sub_find"]:
                        if "sub_class" in config:
                            tags_a = elem.find_all(config["sub_find"], class_=config["sub_class"])
                        else:
                            tags_a = elem.find_all(config["sub_find"])
                    else:
                        tags_a = [elem] if elem.name == "a" else []
                    texto = None
                
                for a in tags_a:
                    href = a.get("href", "")
                    if not texto: texto = a.get_text().strip()
                    
                    if not href or len(texto) < 14: continue
                    
                    # Concatena os caminhos relativos exatamente como no seu script
                    if href.startswith("/"):
                        href = config["base"].rstrip('/') + href if config["base"] else url_alvo.rstrip('/') + href
                    elif not href.startswith("http"):
                        if idx == 1: href = url_alvo + href # Caso específico Psychology Today
                    
                    if href not in vistos:
                        vistos.add(href)
                        traducao = traduzir(texto)
                        item = {"url": href, "texto": texto, "traducao": traducao}
                        links_site.append(item)
                        
                        if any(p in texto.lower() or p in traducao.lower() for p in keywords):
                            noticias_filtradas_urgentes.append({**item, "fonte": config["nome"]})
        time.sleep(0.2)
    except Exception as e:
        print(f"Ignorado/Timeout em {config['nome']}")
        
    dados_painel.append({"nome": config["nome"], "noticias": links_site[:12]})

# --- RENDERIZAÇÃO ESTREITA E COMPACTA NO SEU DESIGN NATIVO ORIGINAL ---
with open(namefile, "w", encoding="utf-8") as file:
    # 1. Escrita estrutural do Head e CSS integrado para controle fino do seu design
    file.write('<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
    file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
    file.write('<title>PSI LINKS BOARD</title>')
    file.write('''<style>
        .btn-space { margin: 4px; }
        .sub-tra { font-size: 0.82rem; color: #6c757d; display: block; margin-bottom: 8px; margin-left: 10px; }
        #btnVoltarTopo { position: fixed; bottom: 20px; right: 20px; display: none; z-index: 99; border: none; background-color: #17a2b8; color: white; padding: 10px 16px; border-radius: 4px; font-weight: 600; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; }
    </style></head>''')
    
    # Body, botão de topo e Título original com a estampa de data sutil integrada
    file.write('<body><button onclick="irParaOTopo()" id="btnVoltarTopo">▲ Topo</button>')
    file.write('<div class="container" id="myGroup">')
    
    # Cabeçalho original enriquecido discretamente com a data da raspagem requerida
    file.write(f'<h1> PSI MONITOR <span class="text-muted" style="font-size: 1rem; font-weight: normal; margin-left: 15px;">| Varredura realizada em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</span></h1><p>')
    
    # Botão de Destaques das Palavras-Chave no seu padrão exato de botões inline
    file.write('<a class="btn btn-space btn-danger btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button" aria-expanded="false" aria-controls="collapseKeywords">🎯 Palavras-Chave Ativas</a>')
    
    # Loop que injeta os 30 botões exatamente em linha horizontal no layout que você ama
    for i, site in enumerate(dados_painel):
        classe_btn = "btn-outline-danger" if not site["noticias"] else "btn-outline-info"
        file.write(f'<a class="btn btn-space {classe_btn} btn-lg" data-toggle="collapse" href="#collapseIndex{i}" role="button" aria-expanded="false" aria-controls="collapseExample">{site["nome"]}</a>')
    file.write('</p>')

    # 2. CONTÊINERES COLLAPSE NATIVOS DO SEU PROJETO ORIGINAL
    
    # Caixa expansível de Palavras-Chave
    file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup"><div class="card card-body bg-light">')
    file.write(f'<p class="text-muted small">Termos monitorados: {", ".join(keywords)}</p>')
    if not noticias_filtradas_urgentes:
        file.write('<p class="text-muted">Nenhum artigo correspondente encontrado.</p>')
    else:
        for n in noticias_filtradas_urgentes:
            file.write(f'<a href="{n["url"]}" target="_blank">📌 [{n["fonte"]}] {n["texto"]}</a></br>\n')
            if n["traducao"] and n["traducao"] != n["texto"]:
                file.write(f'<span class="sub-tra">↳ Tradução: {n["traducao"]}</span>\n')
    file.write('</div></div>')

    # Loop único e curto que escreve as 30 divisões de cards mantendo a primeira aberta ("collapse show")
    for i, site in enumerate(dados_painel):
        classe_show = "collapse show" if i == 0 else "collapse"
        file.write(f'<div class="{classe_show}" id="collapseIndex{i}" data-parent="#myGroup" Style><div class="card card-body">')
        
        if not site["noticias"]:
            file.write('<p class="text-muted">Nenhum link pôde ser extraído na execução atual.</p>')
        else:
            for n in site["noticias"]:
                file.write(f'<a href="{n["url"]}" target="_blank">{n["texto"]}</a></br>\n')
                if n["traducao"] and n["traducao"] != n["texto"]:
                    file.write(f'<span class="sub-tra">↳ {n["traducao"]}</span>\n')
                    
        file.write('</div></div>')

    # 3. FECHAMENTO DO ARQUIVO COM OS SCRIPTS ORIGINAIS + RECURSO DINÂMICO DO TOPO
    file.write('''</div><div>
    <script src="https://jsdelivr.net"></script>
    <script src="https://jsdelivr.net"></script>
    <script src="https://jsdelivr.net"></script>
    <script src="https://jquery.com"></script>
    <script src="https://cloudflare.com"></script>
    <script src="https://bootstrapcdn.com"></script>
    <script>
        window.onscroll = function() {
            var btn = document.getElementById("btnVoltarTopo");
            if (document.body.scrollTop > 250 || document.documentElement.scrollTop > 250) {
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

print("Sucesso! Script enxuto compilado mantendo 100% da integridade do seu design original.")
