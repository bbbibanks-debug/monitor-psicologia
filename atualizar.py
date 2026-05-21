import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
# Importação da biblioteca de tradução gratuita
from deep_translator import GoogleTranslator

# Configuração de Tempo
data_e_hora_atuais = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# Carrega palavras-chave do arquivo de texto (keywords.txt)
def carregar_palavras_chave(caminho_arquivo="keywords.txt"):
    if not os.path.exists(caminho_arquivo):
        # Cria um arquivo padrão caso ele não exista
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write("anxiety\ndepressão\nburnout\nneuroscience\n")
        return ["anxiety", "depressão", "burnout", "neuroscience"]
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        # Lê, remove espaços e ignora linhas vazias
        return [linha.strip().lower() for linha in f if linha.strip()]

palavras_chave = carregar_palavras_chave()

# Função auxiliar para tradução rápida e segura
def traduzir_texto(texto):
    try:
        # Detecta o idioma de origem e traduz automaticamente para o Português
        traducao = GoogleTranslator(source='auto', target='pt').translate(texto)
        return traducao
    except Exception:
        return "Falha na tradução automática."

# Lista das 30 fontes de mapeamento originais
fontes = [
    {"url": "https://verywellmind.com", "nome": "VeryWell Mind"},
    {"url": "https://psychologytoday.com", "nome": "Psychology Today"},
    {"url": "https://scientificamerican.com", "nome": "Scientific American"},
    {"url": "https://nih.gov", "nome": "NIMH Research"},
    {"url": "https://apa.org", "nome": "APA PsyPort"},
    {"url": "https://apa.org", "nome": "APA Monitor"},
    {"url": "https://google.com", "nome": "Google Notícias"},
    {"url": "https://sbponline.org.br", "nome": "SBP Notícias"},
    {"url": "https://neurosciencenews.com", "nome": "Neuroscience News"},
    {"url": "https://positivepsychology.com", "nome": "Positive Psychology"},
    {"url": "https://psychcentral.com", "nome": "Psych Central"},
    {"url": "http://iqscorner.com", "nome": "IQ's Corner"},
    {"url": "https://happierhuman.com", "nome": "Happier Human"},
    {"url": "https://psychnewsdaily.com", "nome": "PsyNewsDaily"},
    {"url": "https://psychiatrictimes.com", "nome": "Psychiatric Times"},
    {"url": "https://psychologicalscience.org", "nome": "APS Insights"},
    {"url": "https://cfp.org.br", "nome": "CFP"},
    {"url": "https://scielo.br", "nome": "Psicologia USP (SciELO)"},
    {"url": "https://crpsp.org", "nome": "CRP-SP Impresso"},
    {"url": "https://elpais.com", "nome": "El País Psicologia"},
    {"url": "https://globo.com", "nome": "G1 Saúde Mental"},
    {"url": "https://medicalxpress.com", "nome": "Medical Xpress"},
    {"url": "https://psychreg.org", "nome": "Psychreg"},
    {"url": "https://uol.com.br", "nome": "Folha Mente"},
    {"url": "https://libsyn.com", "nome": "PsychCrunch Podcast"},
    {"url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Neuro"},
    {"url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Psico"},
    {"url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Relações"},
    {"url": "https://amenteemaravilhosa.com.br", "nome": "A Mente é Maravilhosa - Saúde"},
    {"url": "https://bigthink.com", "nome": "Big Think Neuropsych"}
]

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Coleta Geral
conteudos_coletados = []
noticias_filtradas_urgentes = [] # Irá armazenar correspondências das palavras-chave

def extrair_links(soup, url_base):
    links_validos = []
    vistos = set()
    termos_ignorar = ["privacy", "terms of use", "contact", "about", "cookie", "entrar", "assine", "newsletter", "home", "login"]
    
    blocos = soup.find_all(['article', 'section', 'h1', 'h2', 'h3', 'h4', 'h5'])
    for bloco in blocos:
        tags_a = bloco.find_all('a', href=True) if bloco.name != 'a' else [bloco]
        for a in tags_a:
            href = a.get("href").strip()
            texto = a.get_text(strip=True)
            
            if not href or len(texto) < 18 or any(t in texto.lower() for t in termos_ignorar):
                continue
                
            if href.startswith("/"):
                raiz = re.match(r"(https?://[^/]+)", url_base)
                href = raiz.group(1) + href if raiz else url_base.rstrip('/') + href
            elif not href.startswith("http"):
                continue
                
            dominio_base = url_base.split("//")[-1].split("/")[0].replace("www.", "")
            if href not in vistos and (dominio_base in href or "google.com" in url_base):
                vistos.add(href)
                links_validos.append((href, texto))
                
    return links_validos[:12]

# Execução da Raspagem Geral
for idx, fonte in enumerate(fontes):
    print(f"Varrendo [{idx+1}/{len(fontes)}]: {fonte['nome']}...")
    try:
        response = requests.get(fonte["url"], headers=header, timeout=12)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        noticias = extrair_links(soup, fonte["url"])
        
        # Filtro ativo por Palavras-Chave
        noticias_com_traducao = []
        for url, texto in noticias:
            # Traduz o título para podermos colocar a legenda menor embaixo
            texto_traduzido = traduzir_texto(texto)
            item_noticia = {"url": url, "original": texto, "traduzido": texto_traduzido, "fonte": fonte["nome"]}
            noticias_com_traducao.append(item_noticia)
            
            # Se encontrar a palavra-chave no texto original ou no traduzido, joga para o mural principal
            if any(p in texto.lower() or p in texto_traduzido.lower() for p in palavras_chave):
                noticias_filtradas_urgentes.append(item_noticia)
                
        conteudos_coletados.append({"nome": fonte["nome"], "noticias": noticias_com_traducao})
    except Exception as e:
        conteudos_coletados.append({"nome": fonte["nome"], "noticias": [], "erro": True})

# MONTAGEM DA NOVA PÁGINA HTML
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n<meta charset="utf-8">\n')
    file.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')
    file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">\n')
    file.write('<title>PSI MONITOR AVANÇADO</title>\n')
    file.write('<style>.btn-space{margin:4px;} .sub-tra{font-size:0.82rem; color:#6c757d; margin-left:18px; margin-bottom:6px; display:block;}</style>\n</head>\n')
    
    file.write('<body>\n<div class="container my-4" id="myGroup">\n')
    file.write(f'<h1>PSI MONITOR</h1><p class="text-muted">Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y %H:%M")}</p>\n<hr>\n')
    
    # ------------------ NOVO SETOR: BOX EXCLUSIVO DE PALAVRAS-CHAVE ------------------
    file.write('<div class="card border-primary mb-4">\n')
    file.write('  <div class="card-header bg-primary text-white">🎯 CONTEÚDOS FILTRADOS (Palavras-Chave Ativas)</div>\n')
    file.write('  <div class="card-body bg-light" style="max-height: 400px; overflow-y: auto;">\n')
    file.write(f'    <p class="small text-muted">Termos monitorados do arquivo: <i>{", ".join(palavras_chave)}</i></p>\n')
    
    if not noticias_filtradas_urgentes:
        file.write('    <p class="text-muted">Nenhum artigo contendo as palavras-chave foi detectado nas últimas horas.</p>\n')
    else:
        for noti in noticias_filtradas_urgentes:
            file.write(f'    <div class="mb-2">')
            file.write(f'      <a href="{noti["url"]}" target="_blank" class="font-weight-bold text-dark">📌 [{noti["fonte"]}] {noti["original"]}</a>\n')
            file.write(f'      <span class="sub-tra">🗣️ Tradução: {noti["traduzido"]}</span>\n')
            file.write(f'    </div>\n')
            
    file.write('  </div>\n</div>\n<hr>\n')
    # ---------------------------------------------------------------------------------
    
    # Renderização dos Botões de cada Site
    file.write('<p>\n')
    for idx, item in enumerate(conteudos_coletados):
        classe_status = "btn-outline-danger" if item.get("erro") or not item["noticias"] else "btn-outline-info"
        file.write(f'<a class="btn btn-space {classe_status} btn-lg" data-toggle="collapse" ')
        file.write(f'href="#collapseExample{idx}" role="button" aria-expanded="false" ')
        file.write(f'aria-controls="collapseExample{idx}">{item["nome"]}</a>\n')
    file.write('</p>\n')
    
    # Renderização do Conteúdo Interno de cada Botão
    for idx, item in enumerate(conteudos_coletados):
        file.write(f'<div class="collapse" id="collapseExample{idx}" data-parent="#myGroup">\n')
        file.write('  <div class="card card-body">\n')
        
        if item.get("erro"):
            file.write('    <p class="text-danger">Erro ao conectar com o servidor deste portal.</p>\n')
        elif not item["noticias"]:
            file.write('    <p class="text-warning">Nenhum conteúdo estruturado capturado.</p>\n')
        else:
            for noti in item["noticias"]:
                file.write(f'    <div class="mb-1">')
                file.write(f'      <a href="{noti["url"]}" target="_blank" class="d-inline-block font-weight-normal">🔗 {noti["original"]}</a>\n')
                # Letra menor cinza (class sub-tra) logo abaixo do link conforme solicitado
                file.write(f'      <span class="sub-tra">↳ {noti["traduzido"]}</span>\n')
                file.write(f'    </div>\n')
                
        file.write('  </div>\n</div>\n')
        
    file.write('</div>\n<div>\n')
    file.write('<script src="https://jquery.com"></script>\n')
    file.write('<script src="https://cloudflare.com"></script>\n')
    file.write('<script src="https://bootstrapcdn.com"></script>\n')
    file.write('</div>\n</body>\n</html>')

print(f"\nConcluído com sucesso! Verifique o arquivo '{namefile}'.")
