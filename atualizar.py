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

# --- MAPEAMENTO DA ARQUITETURA DE RASPAGEM (SELETORES CIRÚRGICOS) ---
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

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

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
                config["sub_find"] = "a" if elementos_pai and elementos_pai[0].name != "a" else None
            
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
        
    dados_painel.append({"nome": config["nome"], "noticias": links_site[:10]})

# --- RENDERIZAÇÃO DO TEMPLATE COM DESIGN DE PAINEL SISTÊMICO ---
with open(namefile, "w", encoding="utf-8") as file:
    # Cabeçalho estrutural e CSS Customizado de Alta Performance visual
    file.write('''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://bootstrapcdn.com">
    <title>Painel Integrado de Psicologia</title>
    <style>
        body { background-color: #f0f2f5; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; }
        .main-card { background: #ffffff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border: none; margin-top: 30px; margin-bottom: 40px; overflow: hidden; }
        .app-header { background: #1a2a40; color: white; padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #243b55; flex-wrap: wrap; }
        .app-title { font-size: 1.6rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
        .time-badge { background: #2a3e59; color: #a5c2f4; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }
        
        /* Sistema de Abas Avançado */
        .sidebar-menu { background: #f8fafc; border-right: 1px solid #e2e8f0; max-height: 700px; overflow-y: auto; padding: 15px 10px; }
        .list-group-item-action { border: none !important; border-radius: 8px !important; margin-bottom: 4px; font-weight: 500; font-size: 0.95rem; color: #4a5568; padding: 12px 16px; transition: all 0.15s ease-in-out; }
        .list-group-item-action:hover { background-color: #edf2f7; color: #1a2a40; text-decoration: none; }
        .list-group-item-action.active { background: #3182ce !important; color: white !important; box-shadow: 0 4px 10px rgba(49,130,206,0.25); }
        .list-group-item-action.kw-active { background: #e53e3e !important; color: white !important; box-shadow: 0 4px 10px rgba(229,62,62,0.25); font-weight: bold; }
        
        /* Espaço de Conteúdo */
        .content-body { padding: 30px; max-height: 700px; overflow-y: auto; background: #ffffff; }
        .content-title { font-size: 1.4rem; font-weight: 700; color: #1a2a40; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #edf2f7; }
        .article-block { padding: 14px 0; border-bottom: 1px solid #f1f5f9; transition: transform 0.2s; }
        .article-block:last-child { border-bottom: none; }
        .article-link { font-size: 1.05rem; font-weight: 600; color: #1e3a8a; text-decoration: none; line-height: 1.4; display: inline-block; }
        .article-link:hover { color: #3b82f6; text-decoration: none; }
        .sub-tra { font-size: 0.88rem; color: #475569; display: block; margin-top: 5px; padding-left: 12px; border-left: 3px solid #cbd5e1; font-style: italic; }
        
        @media (max-width: 767.98px) {
            .sidebar-menu { max-height: 250px; border-right: none; border-bottom: 1px solid #e2e8f0; }
            .app-header { text-align: center; justify-content: center; gap: 10px; }
        }
    </style>
</head>
<body>
    <div class="container-fluid px-md-5">
        <div class="card main-card">
            <!-- Cabeçalho Fixo -->
            <div class="app-header">
                <h1 class="app-title">🧠 MONITOR INTEGRADO DE PSICOLOGIA</h1>''')
                
    # Inserção explícita e elegante do dia e horário conforme solicitado
    file.write(f'''
                <div class="time-badge">
                    ⏱️ Última raspagem: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}
                </div>
            </div>
            
            <div class="row no-gutters">
                <!-- Coluna de Navegação Esquerda -->
                <div class="col-md-4 col-lg-3 sidebar-menu">
                    <div class="list-group" id="list-tab" role="tablist">
                        <a class="list-group-item list-group-item-action kw-active" id="list-kw-list" data-toggle="list" href="#list-kw" role="tab">🎯 PALAVRAS-CHAVE</a>
    ''')
    
    for i, site in enumerate(dados_painel):
        # A primeira aba de site normal inicia marcada como ativa por convenção do Bootstrap
        file.write(f'<a class="list-group-item list-group-item-action" id="list-index{i}-list" data-toggle="list" href="#list-index{i}" role="tab">📁 {site["nome"]}</a>\n')
        
    file.write('''
                    </div>
                </div>
                
                <!-- Coluna de Leitura Direita -->
                <div class="col-md-8 col-lg-9">
                    <div class="tab-content content-body" id="nav-tabContent">
                        
                        <!-- Painel de Palavras-Chave -->
                        <div class="tab-pane fade show active" id="list-kw" role="tabpanel">
                            <div class="content-title text-danger">🎯 Artigos Filtrados por Interesse</div>
    ''')
    
    file.write(f'<p class="text-muted small">Termos monitorados ativos no arquivo: <code>{", ".join(keywords)}</code></p>')
    if not noticias_filtradas_urgentes:
        file.write('<div class="alert alert-light text-muted">Nenhum artigo contendo as palavras-chave foi detectado na execução atual.</div>')
    else:
        for n in noticias_filtradas_urgentes:
            file.write(f'''
                            <div class="article-block">
                                <a class="article-link" href="{n["url"]}" target="_blank">📌 [{n["fonte"]}] {n["texto"]}</a>
            ''')
            if n["traducao"] and n["traducao"] != n["texto"]:
                file.write(f'<span class="sub-tra">↳ Tradução: {n["traducao"]}</span>')
            file.write('</div>')
            
    file.write('</div>')

    # Painéis Individuais de cada Site
    for i, site in enumerate(dados_painel):
        file.write(f'''
                        <div class="tab-pane fade" id="list-index{i}" role="tabpanel">
                            <div class="content-title text-primary">🌐 {site["nome"]}</div>
        ''')
        
        if not site["noticias"]:
            file.write('<div class="alert alert-light text-muted">Nenhum artigo pôde ser extraído deste portal nesta rodada.</div>')
        else:
            for n in site["noticias"]:
                file.write(f'''
                            <div class="article-block">
                                <a class="article-link" href="{n["url"]}" target="_blank">🔗 {n["texto"]}</a>
                ''')
                if n["traducao"] and n["traducao"] != n["texto"]:
                    file.write(f'<span class="sub-tra">↳ {n["traducao"]}</span>')
                file.write('</div>')
                
        file.write('</div>')

    # Encerramento do documento e carregamento assíncrono dos scripts necessários
    file.write('''
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://jquery.com"></script>
    <script src="https://cloudflare.com"></script>
    <script src="https://bootstrapcdn.com"></script>
</body>
</html>''')

print("Sucesso! Painel gerado com layout sistêmico de alta fidelidade.")
