import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÕES DE TEMPO E ARQUIVOS ---
data_e_hora_sao_paulo = datetime.now(timezone(timedelta(hours=-3)))
namefile = "index.html"

# Carrega palavras-chave do arquivo de texto
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

# --- MAPEAMENTO DA ARQUITETURA DE RASPAGEM (SELETORES CIRÚRGICOS) ---
# Centraliza as regras de cada site em um dicionário para eliminar repetição de código
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

# Executa a varredura em loop único inteligente
for idx, config in enumerate(fontes_config):
    print(f"[{idx+1}/{len(fontes_config)}] Capturando: {config['nome']}")
    links_site = []
    vistos = set()
    
    try:
        res = requests.get(config["url"], headers=header, timeout=12)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            
            # Executa a busca baseada na configuração cirúrgica do site
            elementos_pai = soup.find_all(config["find"][0], config["find"][1] if len(config["find"]) > 1 else None)
            
            for elem in elementos_pai:
                tags_a = elem.find_all(config["sub_find"]) if config["sub_find"] else [elem] if elem.name == "a" else []
                
                for a in tags_a:
                    href = a.get("href", "")
                    texto = a.get_text().strip()
                    
                    if not href or len(texto) < 14: continue
                    if href.startswith("/"): href = config["base"].rstrip('/') + href
                    
                    if href not in vistos:
                        vistos.add(href)
                        traducao = traduzir(texto)
                        item = {"url": href, "texto": texto, "traducao": traducao}
                        links_site.append(item)
                        
                        # Alimenta as palavras-chave globais
                        if any(p in texto.lower() or p in traducao.lower() for p in keywords):
                            noticias_filtradas_urgentes.append({**item, "fonte": config["nome"]})
                            
    except Exception as e:
        print(f"Erro em {config['nome']}: {e}")
        
    dados_painel.append({"nome": config["nome"], "noticias": links_site[:10]})

# --- RENDERIZAÇÃO EM ARQUIVO ÚNICO (DESIGN MINIMALISTA E MODERNO) ---
with open(namefile, "w", encoding="utf-8") as file:
    file.write(f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://bootstrapcdn.com">
    <title>PSI Links Board</title>
    <style>
        body {{ background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        .dashboard-header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px 20px; border-radius: 0 0 20px 20px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .btn-tag {{ margin: 4px; border-radius: 30px; font-weight: 500; font-size: 0.9rem; padding: 6px 16px; transition: all 0.2s; }}
        .card-container {{ border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); background: white; padding: 20px; margin-bottom: 20px; }}
        .news-link {{ font-size: 1.05rem; font-weight: 500; color: #2c3e50; text-decoration: none; display: inline-block; margin-top: 8px; }}
        .news-link:hover {{ color: #0056b3; text-decoration: none; }}
        .sub-tra {{ font-size: 0.85rem; color: #6c757d; display: block; margin-bottom: 12px; padding-left: 15px; border-left: 2px solid #dee2e6; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="dashboard-header text-center">
            <h1 class="display-5 font-weight-bold">🧠 PSI MONITOR</h1>
            <p class="mb-0 opacity-75">Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</p>
        </div>

        <!-- Tag de Palavras-Chave -->
        <div class="text-center mb-4">
            <a class="btn btn-tag btn-danger btn-lg shadow-sm" data-toggle="collapse" href="#collapseKeywords" role="button">🎯 Palavras-Chave Ativas</a>
            {" ".join([f'<a class="btn btn-tag btn-outline-primary shadow-sm" data-toggle="collapse" href="#collapseIndex{i}" role="button">{site["nome"]}</a>' for i, site in enumerate(dados_painel)])}
        </div>

        <div id="myGroup">
            <!-- Box de Palavras-Chave -->
            <div class="collapse" id="collapseKeywords" data-parent="#myGroup">
                <div class="card-container" style="border-top: 4px solid #dc3545;">
                    <h4 class="text-danger font-weight-bold mb-3">🎯 Destaques do seu interesse</h4>
                    {"<p class='text-muted'>Nenhum artigo correspondente encontrado.</p>" if not noticias_filtradas_urgentes else ""}
                    {"".join([f'<a class="news-link" href="{n["url"]}" target="_blank">📌 [{n["fonte"]}] {n["texto"]}</a><span class="sub-tra">↳ {n["traducao"]}</span>' for n in noticias_filtradas_urgentes])}
                </div>
            </div>

            <!-- Boxes Individuais dos Sites -->
            {"".join([f'''
            <div class="collapse {'show' if i==0 else ''}" id="collapseIndex{i}" data-parent="#myGroup">
                <div class="card-container" style="border-top: 4px solid #007bff;">
                    <h4 class="text-primary font-weight-bold mb-3">🌐 {site["nome"]}</h4>
                    {"<p class='text-muted'>Nenhum artigo capturado nesta rodada.</p>" if not site["noticias"] else ""}
                    {"".join([f'<a class="news-link" href="{n["url"]}" target="_blank">🔗 {n["texto"]}</a><span class="sub-tra">↳ {n["traducao"]}</span>' for n in site["noticias"]])}
                </div>
            </div>
            ''' for i, site in enumerate(dados_painel)])}
        </div>
    </div>

    <script src="https://jquery.com"></script>
    <script src="https://cloudflare.com"></script>
    <script src="https://bootstrapcdn.com"></script>
</body>
</html>''')

print("Painel atualizado com sucesso com design premium!")
