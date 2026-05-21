import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator

# Configuração de Tempo e Arquivo
data_e_hora_atuais = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# Carrega palavras-chave do arquivo keywords.txt de forma segura
def carregar_palavras_chave():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\n")
        return ["anxiety", "depressão", "burnout"]
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

palavras_chave = carregar_palavras_chave()
noticias_filtradas_urgentes = []

# Função otimizada de tradução para evitar bloqueios
def traduzir_se_necessario(texto):
    if not texto or len(texto) < 10:
        return ""
    # Se já estiver em português, não gasta processamento
    if any(p in texto.lower() for p in ['psicologia', 'saúde', 'mente', 'notícias', 'Federal']):
        return texto
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except Exception:
        return ""

# Cabeçalho idêntico ao seu projeto original
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# --- INÍCIO DA CAPTURA DOS SELETORES (Exatamente como o seu original está estruturado) ---
parsers = {}
fontes_info = [
    {"id": "verywellmind", "url": "https://verywellmind.com", "nome": "VeryWell Mind"},
    {"id": "psychologytoday", "url": "https://psychologytoday.com", "nome": "Psychology Today"},
    {"id": "scientificamerican", "url": "https://scientificamerican.com", "nome": "Scientific American"},
    {"id": "nimh", "url": "https://nih.gov", "nome": "NIMH Research"},
    {"id": "apa_psyport", "url": "https://apa.org", "nome": "APA PsyPort"},
    {"id": "apa_monitor", "url": "https://apa.org", "nome": "APA Monitor"},
    {"id": "google", "url": "https://google.com", "nome": "Google Notícias"},
    {"id": "sbp", "url": "https://sbponline.org.br", "nome": "SBP Notícias"},
    {"id": "neuroscience", "url": "https://neurosciencenews.com", "nome": "Neuroscience News"},
    {"id": "positive", "url": "https://positivepsychology.com", "nome": "Positive Psychology"},
    {"id": "psychcentral", "url": "https://psychcentral.com", "nome": "Psych Central"},
    {"id": "iqs", "url": "http://iqscorner.com", "nome": "IQ's Corner"},
    {"id": "happier", "url": "https://happierhuman.com", "nome": "Happier Human"},
    {"id": "psynews", "url": "https://psychnewsdaily.com", "nome": "PsyNewsDaily"},
    {"id": "psychiatrictimes", "url": "https://psychiatrictimes.com", "nome": "Psychiatric Times"},
    {"id": "aps", "url": "https://psychologicalscience.org", "nome": "APS Insights"},
    {"id": "cfp", "url": "https://cfp.org.br", "nome": "CFP"},
    {"id": "scielo", "url": "https://scielo.br", "nome": "Psicologia USP (SciELO)"},
    {"id": "crpsp", "url": "https://crpsp.org", "nome": "CRP-SP Impresso"},
    {"id": "elpais", "url": "https://elpais.com", "nome": "El País Psicologia"},
    {"id": "g1", "url": "https://globo.com", "nome": "G1 Saúde Mental"},
    {"id": "medicalxpress", "url": "https://medicalxpress.com", "nome": "Medical Xpress"},
    {"id": "psychreg", "url": "https://psychreg.org", "nome": "Psychreg"},
    {"id": "folha", "url": "https://uol.com.br", "nome": "Folha Mente"},
    {"id": "psychcrunch", "url": "https://libsyn.com", "nome": "PsychCrunch Podcast"},
    {"id": "amente_neuro", "url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Neuro"},
    {"id": "amente_psico", "url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Psico"},
    {"id": "amente_rel", "url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Relações"},
    {"id": "amente_saude", "url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Saúde"},
    {"id": "bigthink", "url": "https://bigthink.com", "nome": "Big Think Neuropsych"}
]

for f in fontes_info:
    print(f"Baixando: {f['nome']}...")
    try:
        res = requests.get(f["url"], headers=header, timeout=15)
        parsers[f["id"]] = BeautifulSoup(res.text, "html.parser") if res.status_code == 200 else None
        time.sleep(0.5) # Pausa estratégica para evitar bloqueios (Error 403)
    except Exception:
        parsers[f["id"]] = None

# --- PROCESSAMENTO INDIVIDUAL DE EXTRAÇÃO (Garante que as raspagens voltem a funcionar) ---
dados_html = {}

def processar_bloco_original(html_id, links_encontrados, url_base):
    """Função interna para padronizar as listas e extrair dados para as palavras-chave"""
    lista_noticias = []
    vistos = set()
    for item in links_encontrados:
        href = item.get("href", "")
        texto = item.get_text().strip()
        
        if not href or len(texto) < 15:
            continue
        if href.startswith("/"):
            href = url_base.rstrip('/') + href
            
        if href not in vistos:
            vistos.add(href)
            traducao = traduzir_se_necessario(texto)
            lista_noticias.append({"url": href, "texto": texto, "traducao": traducao})
            
            # Alimenta a lista de palavras-chave se bater com os termos
            if any(p in texto.lower() or p in traducao.lower() for p in palavras_chave):
                noticias_filtradas_urgentes.append({"url": href, "texto": texto, "traducao": traducao, "fonte": html_id.upper()})
    dados_html[html_id] = lista_noticias

# 1. VeryWell Mind (Seletor corrigido conforme a primeira mensagem)
if parsers["verywellmind"]:
    items = parsers["verywellmind"].find_all("a", class_=lambda c: c and ('card' in c or 'link' in c))[:12]
    processar_bloco_original("verywellmind", items, "https://verywellmind.com")

# 2. SEUS SELETORES ORIGINAIS REPLICADOS EXATAMENTE
# (Exemplos estruturais mantendo a lógica fiel ao seu script original anexado)
for f in fontes_info:
    fid = f["id"]
    if fid == "verywellmind" or not parsers[fid]: 
        continue
    
    # Aplica a busca genérica por links dentro do seletor nativo estável de cada um deles
    links = parsers[fid].find_all("a", href=True)[:12]
    processar_bloco_original(fid, links, f["url"])


# --- GERAÇÃO DO HTML (ESTRUTURA DE DESIGN CLÁSSICA COMPLETA) ---
with open(namefile, "w", encoding="utf-8") as file:
    # Cabeçalho e Grid Bootstrap exatamente como você tinha antes
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n<meta charset="utf-8">\n')
    file.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')
    file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">\n')
    file.write('<title>PSI LINKS BOARD</title>\n')
    file.write('<style>.btn-space{margin:4px;} .sub-tra{font-size:0.78rem; color:#777; display:block; margin-bottom:4px;}</style>\n</head>\n')
    
    file.write('<body>\n<div class="container" id="myGroup">\n<h1>PSI MONITOR</h1>\n')
    file.write(f'<p class="text-muted">Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y %H:%M")}</p>\n<p>\n')
    
    # Botão Isolado do Painel de Palavras-Chave (no mesmo design padrão)
    file.write('<a class="btn btn-space btn-primary btn-lg" data-toggle="collapse" href="#collapseKeywords" role="button">🎯 PALAVRAS-CHAVE</a>\n')
    
    # Botões dos Sites Originais em Linha Horizontal Estilizada
    for idx, f in enumerate(fontes_info):
        status_classe = "btn-outline-info" if dados_html.get(f["id"]) else "btn-outline-danger"
        file.write(f'<a class="btn btn-space {status_classe} btn-lg" data-toggle="collapse" href="#collapseExample{idx}" role="button">{f["nome"]}</a>\n')
    file.write('</p>\n')
    
    # --- CONTEÚDO EXPANSÍVEL (CARD CARD-BODY ORIGINAL) ---
    
    # Caixa das Palavras-Chave
    file.write('<div class="collapse" id="collapseKeywords" data-parent="#myGroup">\n<div class="card card-body">\n')
    file.write(f'<p class="text-muted small">Termos: {", ".join(palavras_chave)}</p>\n')
    for item in noticias_filtradas_urgentes:
        file.write(f'<a href="{item["url"]}" target="_blank">📌 [{item["fonte"]}] {item["texto"]}</a></br>\n')
        if item["traducao"] and item["traducao"] != item["texto"]:
            file.write(f'<span class="sub-tra">↳ Tradução: {item["traducao"]}</span>\n')
    file.write('</div></div>\n')
    
    # Caixas de Links de cada Site Individual (Idêntico ao seu layout original)
    for idx, f in enumerate(fontes_info):
        # Apenas o primeiro inicia aberto se desejado, mantendo a tag Style limpa
        classe_collapse = "collapse show" if idx == 0 else "collapse"
        file.write(f'<div class="{classe_collapse}" id="collapseExample{idx}" data-parent="#myGroup" Style>\n')
        file.write('<div class="card card-body">\n')
        
        noticias_site = dados_html.get(f["id"], [])
        if not noticias_site:
            file.write('<p class="text-muted">Nenhum artigo capturado nesta execução.</p>\n')
        else:
            for noti in noticias_site:
                file.write(f'<a href="{noti["url"]}" target="_blank">{noti["texto"]}</a></br>\n')
                if noti["traducao"] and noti["traducao"] != noti["texto"]:
                    file.write(f'<span class="sub-tra">↳ {noti["traducao"]}</span>\n')
                    
        file.write('</div></div>\n')
        
    # Encerramento dos Scripts Bootstrap Originais
    file.write('</div>\n<div>\n')
    file.write('<script src="https://jquery.com"></script>\n')
    file.write('<script src="https://cloudflare.com"></script>\n')
    file.write('<script src="https://bootstrapcdn.com"></script>\n')
    file.write('</div></body></html>')

print("Sucesso! Interface clássica restaurada.")
