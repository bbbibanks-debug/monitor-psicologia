import os
import re
import functools
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone, timedelta

# Time
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime("%d%m%Yday%H%Mtime")

# Nome padrão do arquivo de saída
namefile = "index.html"

# Mapping
links = [
    "https://verywellmind.com",
    "https://psychologytoday.com",
    "https://scientificamerican.com",
    "https://nih.gov",
    "https://apa.org",
    "https://apa.org",
    "https://google.com",
    "https://sbponline.org.br",
    "https://neurosciencenews.com",
    "https://positivepsychology.com",
    "https://psychcentral.com",
    "http://iqscorner.com",
    "https://happierhuman.com",
    "https://psychnewsdaily.com",
    "https://psychiatrictimes.com",
    "https://psychologicalscience.org",
    "https://cfp.org.br",
    "https://scielo.br",
    "https://crpsp.org",
    "https://elpais.com",
    "https://globo.com",
    "https://medicalxpress.com",
    "https://psychreg.org",
    "https://uol.com.br",
    "https://libsyn.com",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br",
    "https://bigthink.com"
]

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Inicialização das listas de conteúdo raspado
responder = [None] * len(links)
parser = [None] * len(links)

# Dicionário para guardar: (URL, Texto Original)
links_raspados_por_fonte = {i: [] for i in range(len(links))}

for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
        
        p_obj = parser[x]
        if not p_obj:
            continue
            
        if x == 0:
            for s in p_obj.find_all("section"):
                for z in s.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((z.get("href"), z.text.strip()))
        elif x == 1:
            for div in p_obj.find_all("div", class_="layout-content-main"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((links[1] + z.get("href"), z.text.strip()))
        elif x == 2:
            for div in p_obj.find_all("div", class_=re.compile("articleList")):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://scientificamerican.com" + z.get("href"), z.text.strip()))
        elif x == 3:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", class_="aggregated_term_news_link", href=True):
                    links_raspados_por_fonte[x].append(("https://nih.gov" + z.get("href"), z.text.strip()))
        elif x == 4:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((z.get("href"), z.text.strip()))
        elif x == 5:
            for s in p_obj.find_all("section", class_="linkWidget tile square"):
                for p_tag in s.find_all("p", class_="title"):
                    for n in p_tag.find_all("a", href=True):
                        links_raspados_por_fonte[x].append(("https://apa.org" + str(n.get("href")), p_tag.text.strip()))
        elif x == 6:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", class_="VDXfz", href=True):
                    links_raspados_por_fonte[x].append(("https://google.com" + str(z.get("href")), art.text.strip()))
        elif x == 7:
            for div in p_obj.find_all("div", class_="content list"):
                for p_tag in div.find_all("p"):
                    for n in p_tag.find_all("a", href=True):
                        links_raspados_por_fonte[x].append(("https://sbponline.org.br" + str(n.get("href")), n.text.strip()))
        elif x == 8:
            for h3 in p_obj.find_all("h3"):
                for z in h3.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), h3.text.strip()))
        elif x == 9:
            for a_tag in p_obj.find_all("a", href=True):
                for h3 in a_tag.find_all("h3"):
                    links_raspados_por_fonte[x].append((str(a_tag.get("href")), h3.text.strip()))
        elif x == 10:
            for div in p_obj.find_all("div", class_="css-fdjy12"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://psychcentral.com" + str(z.get("href")), z.text.strip()))
        elif x in [11, 12, 13, 15, 16, 18, 21]:
            for h2_ou_h3 in p_obj.find_all(["h2", "h3"]):
                for z in h2_ou_h3.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 14:
            for a_tag in p_obj.find_all("a", href=True):
                for h2 in a_tag.find_all("h2"):
                    links_raspados_por_fonte[x].append(("https://psychiatrictimes.com" + str(a_tag.get("href")), h2.text.strip()))
        elif x == 17:
            for a_tag in p_obj.find_all("a", href=True):
                for h3 in a_tag.find_all("h3"):
                    links_raspados_por_fonte[x].append(("https://scielo.br" + str(a_tag.get("href")), h3.text.strip()))
        elif x == 19:
            for h2 in p_obj.find_all("h2"):
                for z in h2.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://elpais.com" + str(z.get("href")), z.text.strip()))
        elif x == 20:
            for div in p_obj.find_all("div", class_="_evt"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 22:
            for div in p_obj.find_all("div", class_="col-md-4"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 23:
            for a_tag in p_obj.find_all("a", href=True):
                for h2 in a_tag.find_all("h2"):
                    links_raspados_por_fonte[x].append((str(a_tag.get("href")), h2.text.strip()))
        elif x == 24:
            for div in p_obj.find_all("div", class_="libsyn-item-title"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x in [25, 26, 27, 28]:
            for a_tag in p_obj.find_all("a", class_=re.compile("default-a-link"), href=True):
                links_raspados_por_fonte[x].append(("https://amenteemaravilhosa.com.br" + str(a_tag.get("href")), a_tag.text.strip()))
        elif x == 29:
            for h1 in p_obj.find_all("h1", class_="card-headline"):
                for z in h1.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))

    except Exception as e:
        print(f"Erro ao raspar {links[x]}: {e}")

# Geração do arquivo HTML definitivo - CSS Mantido Crucialmente Intacto
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n')
    file.write('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n')
    file.write('<title>PSI LINKS BOARD</title>\n')
    
    # === DESIGN MANTIDO 100% INALTERADO ===
    file.write('<style>\n')
    file.write('  body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 24px; color: #333; background-color: #ffffff; }\n')
    file.write('  h1 { font-size: 28px; font-weight: bold; margin-bottom: 20px; color: #111; }\n')
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
    
    file.write('<div class="grid-botoes">\n')
    nomes_fontes = [
        "VeryWell Mind", "Psychology Today", "Scientific American", "The National Institute of Mental Health (NIMH)",
        "APA PsyPort", "APA Monitor", "Google Notícias", "SBP", "Neuroscience", "Positive Psychology",
        "Positive Psychcentral", "IQ's Corner", "Happier Human", "PsyNewsDaily", "Psychiatric Times", "APS", "CFP",
        "Psicologia USP", "Conselho Regional de Psicologia SP", "El País Psicologia", "G1 Saúde Mental",
        "Medical Xpress", "Psychreg", "Folha Equilíbrio Mente", "PsychCrunch", "A Mente é Maravilhosa-Neurociência",
        "A Mente é Maravilhosa-Psicologia", "A Mente é Maravilhosa-Relações", "A Mente é Maravilhosa-Saúde", "Big Think"
    ]
    
    for idx, nome in enumerate(nomes_fontes):
        classe_ativa = " ativo" if idx == 0 else ""
        file.write(f'  <button class="btn-fonte{classe_ativa}" onclick="mostrarConteudo({idx}, this)">{nome}</button>\n')
    file.write('</div>\n\n')

    # Caixa dinâmica inicial
    file.write('<div class="caixa-dinamica" id="conteudoResultados">\n')
    if 0 in links_raspados_por_fonte and len(links_raspados_por_fonte[0]) > 0:
        for url_lnk, txt_lnk in links_raspados_por_fonte[0]:
            file.write('  <div class="item-artigo">\n')
            file.write(f'    <a href="{url_lnk}" target="_blank">{txt_lnk if txt_lnk else url_lnk}</a>\n')
            file.write(f'    <span class="traducao" data-original="{txt_lnk}">Traduzindo...</span>\n')
            file.write('  </div>\n')
    else:
        file.write('  <span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\n')
    file.write("</div>\n\n")

    # Injeção do Banco de Dados JSON e lógica JS
    file.write('<script>\n')
    file.write('  const bancoDeDados = {\n')
    for idx in range(len(links)):
        file.write(f'    {idx}: [\n')
        for url_lnk, txt_lnk in links_raspados_por_fonte[idx]:
            texto_limpo = txt_lnk.replace('"', '\\"').replace('\n', ' ').replace('\r', '')
            url_limpa = url_lnk.replace('"', '\\"')
            file.write(f'      {{ url: "{url_limpa}", texto: "{texto_limpo}" }},\n')
        file.write('    ],\n')
    file.write('  };\n\n')

    # Motor assíncrono de tradução em tempo real sem intermediários
    file.write('  async function traduzirTextoNativo(elementoSpan, textoOriginal) {\n')
    file.write('    if (!textoOriginal || textoOriginal.length < 3) return;\n')
    file.write('    const palavrasChave = ["psicologia", "saúde", "mente", "notícias", "noticias"];\n')
    file.write('    if (palavrasChave.some(p => textoOriginal.toLowerCase().includes(p))) {\n')
    file.write('      elementoSpan.style.display = "none";\n')
    file.write('      return;\n')
    file.write('    }\n')
    file.write('    try {\n')
    file.write('      const url = `https://googleapis.com{encodeURIComponent(textoOriginal)}`;\n')
    file.write('      const res = await fetch(url);\n')
    file.write('      const dados = await res.json();\n')
    file.write('      if (dados && dados[0] && dados[0][0]) {\n')
    file.write('        elementoSpan.textContent = dados[0][0][0];\n')
    file.write('      }\n')
    file.write('    } catch (e) {\n')
    file.write('      elementoSpan.style.display = "none";\n')
    file.write('    }\n')
    file.write('  }\n\n')

    # Renderizador da caixa que dispara as requisições em paralelo sob demanda
    file.write('  function mostrarConteudo(id, elementoAlvo) {\n')
    file.write('    document.querySelectorAll(".btn-fonte").forEach(btn => btn.classList.remove("ativo"));\n')
    file.write('    elementoAlvo.classList.add("ativo");\n\n')
    file.write('    const container = document.getElementById("conteudoResultados");\n')
    file.write('    container.innerHTML = "";\n\n')
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
    
    file.write('        const span = document.createElement("span");\n')
    file.write('        span.className = "traducao";\n')
    file.write('        span.textContent = "Traduzindo...";\n')
    file.write('        div.appendChild(span);\n\n')
    file.write('        container.appendChild(div);\n\n')
    
    file.write('        traduzirTextoNativo(span, art.texto);\n')
    file.write('      });\n')
    file.write('    } else {\n')
    file.write('      container.innerHTML = \'<span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\';\n')
    file.write('    }\n')
    file.write('  }\n\n')
    
    file.write('  // Inicializa as traduções da primeira fonte carregada por padrão\n')
    file.write('  document.querySelectorAll("#conteudoResultados .traducao").forEach(span => {\n')
    file.write('    traduzirTextoNativo(span, span.getAttribute("data-original"));\n')
    file.write('  });\n')
    file.write('</script>\n')
    file.write('</body>\n</html>')
