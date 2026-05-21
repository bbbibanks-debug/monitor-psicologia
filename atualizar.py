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

# Forçando o nome padrão do arquivo de saída
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

# Dicionário temporário para guardar os links de cada fonte
links_raspados_por_fonte = {i: [] for i in range(len(links))}

for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
        
        # Bloco de extração adaptado para guardar os dados estruturados na memória primeiro
        p_obj = parser[x]
        if x == 0 and p_obj:
            for s in p_obj.find_all("section"):
                for z in s.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((z.get("href"), z.text.strip()))
        elif x == 1 and p_obj:
            for div in p_obj.find_all("div", class_="layout-content-main"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((links[1] + z.get("href"), z.text.strip()))
        elif x == 2 and p_obj:
            for div in p_obj.find_all("div", class_=re.compile("articleList")):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://scientificamerican.com" + z.get("href"), z.text.strip()))
        elif x == 3 and p_obj:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", class_="aggregated_term_news_link", href=True):
                    links_raspados_por_fonte[x].append(("https://nih.gov" + z.get("href"), z.text.strip()))
        elif x == 4 and p_obj:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((z.get("href"), z.text.strip()))
        elif x == 5 and p_obj:
            for s in p_obj.find_all("section", class_="linkWidget tile square"):
                for p_tag in s.find_all("p", class_="title"):
                    for n in p_tag.find_all("a", href=True):
                        links_raspados_por_fonte[x].append(("https://apa.org" + str(n.get("href")), p_tag.text.strip()))
        elif x == 6 and p_obj:
            for art in p_obj.find_all("article"):
                for z in art.find_all("a", class_="VDXfz", href=True):
                    links_raspados_por_fonte[x].append(("https://google.com" + str(z.get("href")), art.text.strip()))
        elif x == 7 and p_obj:
            for div in p_obj.find_all("div", class_="content list"):
                for p_tag in div.find_all("p"):
                    for n in p_tag.find_all("a", href=True):
                        links_raspados_por_fonte[x].append(("https://sbponline.org.br" + str(n.get("href")), n.text.strip()))
        elif x == 8 and p_obj:
            for h3 in p_obj.find_all("h3"):
                for z in h3.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), h3.text.strip()))
        elif x == 9 and p_obj:
            for a_tag in p_obj.find_all("a", href=True):
                for h3 in a_tag.find_all("h3"):
                    links_raspados_por_fonte[x].append((str(a_tag.get("href")), h3.text.strip()))
        elif x == 10 and p_obj:
            for div in p_obj.find_all("div", class_="css-fdjy12"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://psychcentral.com" + str(z.get("href")), z.text.strip()))
        elif x in [11, 15, 16] and p_obj:
            for h3 in p_obj.find_all("h3"):
                for z in h3.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x in [12, 13] and p_obj:
            for h2 in p_obj.find_all("h2"):
                for z in h2.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 14 and p_obj:
            for a_tag in p_obj.find_all("a", href=True):
                for h2 in a_tag.find_all("h2"):
                    links_raspados_por_fonte[x].append(("https://psychiatrictimes.com" + str(a_tag.get("href")), h2.text.strip()))
        elif x in [17, 18, 23] and p_obj:
            for a_tag in p_obj.find_all("a", href=True):
                for element in a_tag.find_all(["h2", "h3"]):
                    prefix = "https://scielo.br" if x == 17 else ""
                    links_raspados_por_fonte[x].append((prefix + str(a_tag.get("href")), element.text.strip()))
        elif x == 19 and p_obj:
            for h2 in p_obj.find_all("h2"):
                for z in h2.find_all("a", href=True):
                    links_raspados_por_fonte[x].append(("https://elpais.com" + str(z.get("href")), z.text.strip()))
        elif x == 20 and p_obj:
            for div in p_obj.find_all("div", class_="_evt"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 21 and p_obj:
            for div in p_obj.find_all("div"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 22 and p_obj:
            for div in p_obj.find_all("div", class_="col-md-4"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x == 24 and p_obj:
            for div in p_obj.find_all("div", class_="libsyn-item-title"):
                for z in div.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))
        elif x in [25, 26, 27, 28] and p_obj:
            for a_tag in p_obj.find_all("a", class_=re.compile("default-a-link"), href=True):
                links_raspados_por_fonte[x].append(("https://amenteemaravilhosa.com.br" + str(a_tag.get("href")), a_tag.text.strip()))
        elif x == 29 and p_obj:
            for h1 in p_obj.find_all("h1", class_="card-headline"):
                for z in h1.find_all("a", href=True):
                    links_raspados_por_fonte[x].append((str(z.get("href")), z.text.strip()))

    except Exception as e:
        print(f"Erro ao raspar {links[x]}: {e}")

# Escrita estruturada do arquivo HTML final utilizando CSS Customizado Limpo
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n')
    file.write('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n')
    file.write('<title>PSI LINKS BOARD</title>\n')
    
    # Inclusão do CSS Nativo customizado idêntico ao layout desejado
    file.write('<style>\n')
    file.write('  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 24px; color: #212529; background-color: #fff; }\n')
    file.write('  h1 { font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.5px; }\n')
    file.write('  .grid-botoes { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }\n')
    file.write('  .btn-fonte { background: #fff; border: 1px solid #17a2b8; color: #17a2b8; padding: 10px 16px; font-size: 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s ease; text-decoration: none; display: inline-block; font-weight: 400; }\n')
    file.write('  .btn-fonte:hover { background-color: #17a2b8; color: #fff; }\n')
    file.write('  .btn-fonte.ativo { background-color: #e2f6f8; border-color: #117a8b; color: #117a8b; font-weight: 500; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); }\n')
    file.write('  .caixa-dinamica { border: 1px solid #dee2e6; border-radius: 6px; padding: 20px; min-height: 100px; background-color: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }\n')
    file.write('  .caixa-dinamica a { display: block; color: #007bff; text-decoration: none; margin-bottom: 10px; font-size: 15px; line-height: 1.4; }\n')
    file.write('  .caixa-dinamica a:hover { text-decoration: underline; color: #0056b3; }\n')
    file.write('  .vazio { color: #6c757d; font-style: italic; }\n')
    file.write('</style>\n</head>\n<body>\n')

    # Container principal e título
    file.write('<h1>PSI MONITOR</h1>\n')
    
    # Grid de botões com as fontes
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
        # O primeiro botão inicia com a classe 'ativo'
        classe_ativa = " ativo" if idx == 0 else ""
        file.write(f'  <button class="btn-fonte{classe_ativa}" onclick="mostrarConteudo({idx}, this)">{nome}</button>\n')
    file.write('</div>\n\n')

    # Caixa Dinâmica Única que exibe as raspagens
    file.write('<!-- Caixa de resultados dinâmica -->\n')
    file.write('<div class="caixa-dinamica" id="conteudoResultados">\n')
    
    # Inicia mostrando os dados da primeira fonte (VeryWell Mind)
    if links_raspados_por_fonte[0]:
        for link_url, link_texto in links_raspados_por_fonte[0]:
            file.write(f'  <a href="{link_url}" target="_blank">{link_texto if link_texto else link_url}</a>\n')
    else:
        file.write('  <span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\n')
    file.write('</div>\n\n')

    # Injeção de uma base de dados JSON compacta no próprio arquivo para alimentar o JavaScript localmente
    file.write('<script>\n')
    file.write('  // Banco de dados em memória gerado pela raspagem\n')
    file.write('  const bancoDeDados = {\n')
    for idx in range(len(links)):
        file.write(f'    {idx}: [\n')
        for link_url, link_texto in links_raspados_por_fonte[idx]:
            # Protege caracteres de quebra de linha ou aspas nas strings geradas
            texto_limpo = link_texto.replace('"', '\\"').replace('\n', ' ')
            url_limpa = link_url.replace('"', '\\"')
            file.write(f'      {{ url: "{url_limpa}", texto: "{texto_limpo}" }},\n')
        file.write('    ],\n')
    file.write('  };\n\n')

    # Função JS interativa responsável por limpar a caixa, remover o status de ativo e injetar o conteúdo novo
    file.write('  function mostrarConteudo(id, elementoAlvo) {\n')
    file.write('    // Altera a classe visual dos botões ativos\n')
    file.write('    document.querySelectorAll(".btn-fonte").forEach(btn => btn.classList.remove("ativo"));\n')
    file.write('    elementoAlvo.classList.add("ativo");\n\n')
    file.write('    const container = document.getElementById("conteudoResultados");\n')
    file.write('    container.innerHTML = "";\n\n')
    file.write('    const artigos = bancoDeDados[id];\n')
    file.write('    if (artigos && artigos.length > 0) {\n')
    file.write('      artigos.forEach(art => {\n')
    file.write('        const a = document.createElement("a");\n')
    file.write('        a.href = art.url;\n')
    file.write('        a.target = "_blank";\n')
    file.write('        a.textContent = art.texto || art.url;\n')
    file.write('        container.appendChild(a);\n')
    file.write('      });\n')
    file.write('    } else {\n')
    file.write('      container.innerHTML = \'<span class="vazio">Nenhum artigo encontrado para esta fonte no momento.</span>\';\n')
    file.write('    }\n')
    file.write('  }\n')
    file.write('</script>\n')
    file.write('</body>\n</html>')
