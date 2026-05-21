import os
import re
import functools
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

# Configuração de Arquivo e Tempo
data_e_hora_atuais = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
namefile = "index.html"

# Mapeamento de Links (URLs e Nomes Exibidos)
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
}

# Coleta Inteligente de Dados
conteudos_coletados = []

def extrair_links_relevantes(soup, url_base):
    links_validos = []
    vistos = set()
    
    # Palavras-chave de links institucionais / irrelevantes para ignorar
    termos_ignorar = ["privacy policy", "terms of use", "contact us", "about us", "cookie policy", 
                      "entrar", "assine", "anuncie", "newsletter", "home", "perfil", "login", "cadastre-se"]
    
    # Estratégia 1: Procurar links dentro de tags estruturais de artigos
    blocos = soup.find_all(['article', 'section', 'h1', 'h2', 'h3', 'h4', 'h5'])
    for bloco in blocos:
        # Se for um título, pega o link de dentro ou o próprio bloco se for um link
        tags_a = bloco.find_all('a', href=True) if bloco.name != 'a' else [bloco]
        for a in tags_a:
            href = a.get("href").strip()
            texto = a.get_text(strip=True)
            
            # Filtros de relevância
            if not href or len(texto) < 18 or any(t in texto.lower() for t in termos_ignorar):
                continue
                
            # Tratamento de caminhos relativos
            if href.startswith("/"):
                # Remove barras extras se houver
                raiz = re.match(r"(https?://[^/]+)", url_base)
                href = raiz.group(1) + href if raiz else url_base.rstrip('/') + href
            elif not href.startswith("http"):
                continue
                
            # Evita duplicados e links externos de anúncios
            dominio_base = url_base.split("//")[-1].split("/")[0].replace("www.", "")
            if href not in vistos and (dominio_base in href or "google.com" in url_base):
                vistos.add(href)
                links_validos.append((href, texto))
                
    # Estratégia de contingência se as tags estruturais falharem
    if not links_validos:
        for a in soup.find_all('a', href=True):
            href = a.get("href").strip()
            texto = a.get_text(strip=True)
            if len(texto) > 20 and not any(t in texto.lower() for t in termos_ignorar):
                if href.startswith("/"):
                    raiz = re.match(r"(https?://[^/]+)", url_base)
                    href = raiz.group(1) + href if raiz else url_base + href
                if href not in vistos:
                    vistos.add(href)
                    links_validos.append((href, texto))
                    
    return links_validos[:15] # Limita às 15 principais notícias por site

# Execução do Scraper loop centralizado
for idx, fonte in enumerate(fontes):
    print(f"Coletando [{idx+1}/{len(fontes)}]: {fonte['nome']}...")
    try:
        response = requests.get(fonte["url"], headers=header, timeout=12)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        noticias = extrair_links_relevantes(soup, fonte["url"])
        conteudos_coletados.append({"nome": fonte["nome"], "noticias": noticias})
    except Exception as e:
        print(f"Erro ao acessar {fonte['nome']}: {e}")
        conteudos_coletados.append({"nome": fonte["nome"], "noticias": [], "erro": True})

# GERAÇÃO DO ARQUIVO HTML COMPACTO E LIMPO
with open(namefile, "w", encoding="utf-8") as file:
    # Cabeçalho estrutural
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n<meta charset="utf-8">\n')
    file.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')
    file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">\n')
    file.write('<title>PSI LINKS BOARD</title>\n<style>.btn-space{margin:4px;}</style>\n</head>\n')
    
    # Corpo do Painel
    file.write('<body>\n<div class="container my-4" id="myGroup">\n')
    file.write(f'<h1>PSI MONITOR</h1><p class="text-muted">Atualizado em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y %H:%M")}</p>\n<hr><p>\n')
    
    # 1. Renderiza os Botões Dinamicamente
    for idx, item in enumerate(conteudos_coletados):
        classe_status = "btn-outline-danger" if item.get("erro") or not item["noticias"] else "btn-outline-info"
        active_show = "show" if idx == 0 else "" # O primeiro inicia aberto por padrão
        
        file.write(f'<a class="btn btn-space {classe_status} btn-lg" data-toggle="collapse" ')
        file.write(f'href="#collapseExample{idx}" role="button" aria-expanded="{"true" if idx==0 else "false"}" ')
        file.write(f'aria-controls="collapseExample{idx}">{item["nome"]}</a>\n')
    file.write('</p>\n')
    
    # 2. Renderiza as Abas de Conteúdo Correspondentes
    for idx, item in enumerate(conteudos_coletados):
        active_show = "show" if idx == 0 else ""
        file.write(f'<div class="collapse {active_show}" id="collapseExample{idx}" data-parent="#myGroup">\n')
        file.write('  <div class="card card-body">\n')
        
        if item.get("erro"):
            file.write('    <p class="text-danger">Falha temporária ao conectar com o servidor deste portal.</p>\n')
        elif not item["noticias"]:
            file.write('    <p class="text-warning">Nenhuma notícia relevante estruturada pôde ser extraída desta vez.</p>\n')
        else:
            for url_noticia, texto_noticia in item["noticias"]:
                file.write(f'    <a href="{url_noticia}" target="_blank" class="d-block py-1">📌 {texto_noticia}</a>\n')
                
        file.write('  </div>\n</div>\n')
        
    # Scripts de fechamento do Bootstrap
    file.write('</div>\n<div>\n')
    file.write('<script src="https://jquery.com"></script>\n')
    file.write('<script src="https://cloudflare.com"></script>\n')
    file.write('<script src="https://bootstrapcdn.com"></script>\n')
    file.write('</div>\n</body>\n</html>')

print(f"Sucesso! O painel '{namefile}' foi atualizado e reconstruído.")
