import os
import re
import functools
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone, timedelta
from deep_translator import GoogleTranslator
from urllib.parse import urljoin

# 2) Horário e Data da última captura (Horário de Brasília)
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = datetime.now(fuso_horario)
data_e_hora_em_texto = data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")

namefile = "index.html"

# 3) Carregamento da lista de exclusão independente externa
urls_bloqueadas = []
if os.path.exists("blacklist.txt"):
    with open("blacklist.txt", "r", encoding="utf-8") as f:
        urls_bloqueadas = [linha.strip().lower() for linha in f if linha.strip()]

# Mapping - OS 10 SETORES ANTERIORES + O NOVO GOOGLE NEWS COMO 11º ITEM
links = [
    "https://verywellmind.com",
    "https://psychologytoday.com",
    "https://scientificamerican.com",
    "https://nih.gov",
    "https://apa.org",
    "https://sbponline.org.br",
    "https://neurosciencenews.com",
    "https://positivepsychology.com",
    "https://medicalxpress.com",
    "https://amenteemaravilhosa.com.br",
    "https://google.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Inicialização do tradutor
tradutor = GoogleTranslator(source='auto', target='pt')

def traduzir_texto(texto):
    if not texto or len(texto.strip()) < 3:
        return ""
    if texto.strip().startswith("http") or any(p in texto.lower() for p in ["psicologia", "saúde", "mente", "notícias", "noticias", "sbp", "crp"]):
        return texto
    try:
        return tradutor.translate(texto)
    except Exception:
        return texto

def url_permitida(url):
    if not url:
        return False
    return not any(termo in url.lower() for termo in urls_bloqueadas)

# Inicialização das listas de dados para as 11 fontes
links_raspados_por_fonte = {i: [] for i in range(len(links))}

for x in range(len(links)):
    try:
        url_raiz = links[x]
        response = requests.get(url_raiz, headers=header, timeout=20)
        response.raise_for_status()
        p_obj = BeautifulSoup(response.text, "html.parser")
        
        vistos = set()
        
        # === RASPAGEM DA SCIENTIFIC AMERICAN REFINADA (ÍNDICE 2) ===
        if x == 2:
            for h_tag in p_obj.find_all(["h2", "h3"]):
                z = h_tag.find("a", href=True) if h_tag.name != "a" else h_tag
                if not z and h_tag.parent.name == "a":
                    z = h_tag.parent
                if z and z.get("href"):
                    url_completa = urljoin(url_raiz, z.get("href"))
                    if url_permitida(url_completa) and url_completa not in vistos:
                        txt = h_tag.text.strip()
                        if len(txt) > 15:
                            vistos.add(url_completa)
                            links_raspados_por_fonte[x].append((url_completa, txt, traduzir_texto(txt)))

        # === RASPAGEM DO NOVO FEED DO GOOGLE NEWS REFINADO (ÍNDICE 10) ===
        elif x == 10:
            for art in p_obj.find_all("article"):
                z = art.find("a", href=True)
                if z and z.get("href"):
                    url_completa = urljoin("https://google.com", z.get("href"))
                    if url_permitida(url_completa) and url_completa not in vistos:
                        txt = ""
                        for elem in art.find_all(["h3", "h4", "a"]):
                            if elem.text.strip():
                                txt = elem.text.strip()
                                break
                        if len(txt) > 12:
                            vistos.add(url_completa)
                            links_raspados_por_fonte[x].append((url_completa, txt, txt))
                            
        # === RASPAGEM AMPLIADA GERAL (PARA OS DEMAIS PORTAIS) ===
        else:
            for z in p_obj.find_all("a", href=True):
                url_completa = urljoin(url_raiz, z.get("href"))
                if not url_permitida(url_completa) or url_completa in vistos:
                    continue
                txt = z.text.strip()
                if not txt and z.get("title"):
                    txt = z.get("title").strip()
                if len(txt) < 15 or any(m in txt.lower() for m in ["home", "about us", "contact", "privacy policy", "terms of use", "subscribe", "login", "sign in", "facebook", "twitter", "instagram", "linkedin", "cookies"]):
                    continue
                vistos.add(url_completa)
                
                if x == 5 or x == 9:
                    links_raspados_por_fonte[x].append((url_completa, txt, txt))
                else:
                    links_raspados_por_fonte[x].append((url_completa, txt, traduzir_texto(txt)))
            
    except Exception as e:
        print(f"Aviso: Omissão temporária ou erro ao raspar {links[x]}: {e}")

# Geração do arquivo HTML definitivo - DESIGN EXIGIDO 100% PROTEGIDO E INTACTO
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n')
    file.write('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n')
    file.write('<title>PSI LINKS BOARD</title>\n')
    
    # === CSS TOTALMENTE MANTIDO ===
    file.write('<style>\n')
    file.write('  body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 24px; color: #333; background-color: #ffffff; }\n')
    file.write('  h1 { font-size: 28px; font-weight: bold; margin-bottom: 2px; color: #111; }\n')
    file.write('  .data-captura { font-size: 14px; color: #666666; margin-bottom: 20px; font-style: italic; }\n')
    file.write('  .grid-botoes { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }\n')
    file.write('  .btn-fonte { background: #ffffff; border: 1px solid #1192a4; color: #1192a4; padding: 8px 14px; font-size: 15px; border-radius: 6px; cursor: pointer; transition: all 0.15s ease; font-weight: 400; }\n')
    file.write('  .btn-fonte:hover { background-color: #1192a4; color: #ffffff; }\n')
    file.write('  .btn-fonte.ativo { background-color: #e6f7f9; border-color: #0b6c7a; color: #0b6c7a; font-weight: 500; }\n')
    file.write('  .caixa-dinamica { border: 1px solid #cccccc; border-radius: 6px; padding: 20px; min-height: 120px; background-color: #ffffff; }\n')
    file.write('  .item-artigo { margin-bottom: 16px; }\n')
    file.write('  .caixa-dinamica a { display: inline-block; color: #0066cc; text-decoration: none; font-size: 15px; line-height: 1.4; }\n')
    file.write('  .caixa-dinamica a:hover { text-decoration: underline; color: #004499; }\n')
    file.write('  .traducao { display: block; color: #666666; font-size: 13px; margin-top: 2px; font-style: italic; }\n')
    file.write('  .vazio { color: #777777; font-style: italic; }\n')
    file.write('</style>\n</head>\n<body>\n')

    file.write('<h1>PSI MONITOR</h1>\n')
    file.write(f'<div class="data-captura">Última atualização: {data_e_hora_em_texto}</div>\n')
    
    # Nomes dos 11 botões em grade com o "Google News" incluso no final
    file.write('<div class="grid-botoes">\n')
    nomes_fontes = [
        "VeryWell Mind", 
        "Psychology Today", 
        "Scientific American", 
        "The National Institute of Mental Health (NIMH)",
        "APA PsyPort", 
        "SBP", 
        "Neuroscience", 
        "Positive Psychology", 
        "Medical Xpress", 
        "A Mente é Maravilhosa-Neurociência",
        "Google News"
    ]
    
    for idx, nome in enumerate(nomes_fontes):
        classe_ativa = " ativo" if idx == 0 else ""
        file.write(f'  <button class="btn-fonte{classe_ativa}" onclick="mostrarConteudo({idx}, this)">{nome}</button>\n')
    file.write('</div>\n\n')

    # Caixa dinâmica inicial carregando o primeiro item
    file.write('<div class="caixa-dinamica" id="conteudoResultados">\n')
    if 0 in links_raspados_por_fonte and len(links_raspados_por_fonte) > 0:
        for url_lnk, txt_lnk, trad_lnk in links_raspados_por_fonte:
            file.write('  <div class="item-artigo">\n')
            file.write(f'    <a href="{url_lnk}" target="_blank">{txt_lnk if txt_lnk else url_lnk}</a>\n')
            if trad_lnk and trad_lnk != txt_lnk:
                file.write(f'    <span class="traducao">{trad_lnk}</span>\n')
            file.write('  </div>\n')
    else:
        file.write('  <span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\n')
    file.write("</div>\n\n")

    # Injeção estável do Banco de Dados JSON para alimentar o clique dos 11 itens
    file.write('<script>\n')
    file.write('  const bancoDeDados = {\n')
    for idx in range(len(links)):
        file.write(f'    {idx}: [\n')
        for url_lnk, txt_lnk, trad_lnk in links_raspados_por_fonte[idx]:
            texto_limpo = txt_lnk.replace('"', '\\"').replace('\n', ' ').replace('\r', '')
            trad_limpa = trad_lnk.replace('"', '\\"').replace('\n', ' ').replace('\r', '')
            url_limpa = url_lnk.replace('"', '\\"')
            file.write(f'      {{ url: "{url_limpa}", texto: "{texto_limpo}", traducao: "{trad_limpa}" }},\n')
        file.write('    ],\n')
    file.write('  };\n\n')

    file.write('  function mostrarConteudo(id, elementoAlvo) {\n')
    file.write('    document.querySelectorAll(".btn-fonte").forEach(btn => btn.classList.remove("ativo"));\n')
    file.write('    elementoAlvo.classList.add("ativo");\n\n')
    file.write('    const container = document.getElementById("conteudoResultados");\n')
    file.write('    container.innerHTML = "";\n\n')  # Correção da linha 204 corrigida perfeitamente
    file.write('    const artigos = bancoDeDados[id];\n')
    file.write('    if (artigos && artigos.length > 0) {\n')
    file.write('      artigos.forEach(art => {\n')
    file.write('        const div = document.createElement("div");\n')
    file.write('        div.className = "item-artigo";\n\n')
    file.write('        const a = document.createElement("a");\n')
    file.write('        a.href = art.url;\n')
    file.write('        a.target = "_blank";\n')
    file.write('        a.textContent = art.texto || art.url;\n')
    file.write('        div.appendChild(a);\n\n')
    
    file.write('        if (art.traducao && art.traducao !== art.texto) {\n')
    file.write('          const span = document.createElement("span");\n')
    file.write('          span.className = "traducao";\n')
    file.write('          span.textContent = art.traducao;\n')
    file.write('          div.appendChild(span);\n')
    file.write('        }\n\n')
    file.write('        container.appendChild(div);\n')
    file.write('      });\n')
    file.write('    } else {\n')
    file.write('      container.innerHTML = \'<span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\';\n')
    file.write('    }\n')
    file.write('  }\n')
    file.write('</script>\n')
    file.write('</body>\n</html>')
