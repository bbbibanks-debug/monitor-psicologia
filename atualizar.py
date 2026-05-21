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

# Forçando o nome padrão conforme o final do script
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

# Initialize responder and parser lists with None for all potential entries
responder = [None] * len(links)
parser = [None] * len(links)

for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
        responder[x] = response
        parser[x] = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error for link {links[x]} (Status Code: {e.response.status_code}): {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error for link {links[x]}: {e}")
    except requests.exceptions.Timeout:
        print(f"Timeout Error for link {links[x]}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred for link {links[x]}: {e}")

# Criação da HTML com o nome do Arquivo
with open(namefile, "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>')
    file.write('<html lang="pt-br">')
    file.write('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
    file.write('<link rel="stylesheet" href="https://jsdelivr.net">')
    file.write('<style>.btn-space { margin-bottom: 8px; margin-right: 4px; display: inline-block; }.card-body a { display: block; margin-bottom: 6px; text-decoration: none; color: #007bff; }.card-body a:hover { text-decoration: underline; }</style>')
    file.write('<title>PSI LINKS BOARD</title></head>')

    file.write('<body><div class="container py-4" id="myGroup"><h1> PSI MONITOR</h1><p class="d-flex flex-wrap">')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample0" role="button" aria-expanded="false" aria-controls="collapseExample0">VeryWell Mind</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample1" role="button" aria-expanded="false" aria-controls="collapseExample1">Psychology Today</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false" aria-controls="collapseExample2">Scientific American</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample3" role="button" aria-expanded="false" aria-controls="collapseExample3">The National Institute of Mental Health (NIMH)</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample4" role="button" aria-expanded="false" aria-controls="collapseExample4">APA PsyPort</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample5" role="button" aria-expanded="false" aria-controls="collapseExample5">APA Monitor</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample6" role="button" aria-expanded="false" aria-controls="collapseExample6">Google Notícias</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample7" role="button" aria-expanded="false" aria-controls="collapseExample7">SBP</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample8" role="button" aria-expanded="false" aria-controls="collapseExample8">Neuroscience</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample9" role="button" aria-expanded="false" aria-controls="collapseExample9">Positive Psychology</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample10" role="button" aria-expanded="false" aria-controls="collapseExample10">Positive Psychcentral</a>')
    file.write("<a class=\"btn btn-space btn-outline-info btn-lg\" data-bs-toggle=\"collapse\" href=\"#collapseExample11\" role=\"button\" aria-expanded=\"false\" aria-controls=\"collapseExample11\">IQ's Corner</a>")
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample12" role="button" aria-expanded="false" aria-controls="collapseExample12">Happier Human</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample13" role="button" aria-expanded="false" aria-controls="collapseExample13">PsyNewsDaily</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample14" role="button" aria-expanded="false" aria-controls="collapseExample14">Psychiatric Times</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample15" role="button" aria-expanded="false" aria-controls="collapseExample15">APS</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample16" role="button" aria-expanded="false" aria-controls="collapseExample16">CFP</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample17" role="button" aria-expanded="false" aria-controls="collapseExample17">Psicologia USP</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample18" role="button" aria-expanded="false" aria-controls="collapseExample18">Conselho Regional de Psicologia SP</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample19" role="button" aria-expanded="false" aria-controls="collapseExample19">El País Psicologia</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample20" role="button" aria-expanded="false" aria-controls="collapseExample20">G1 Saúde Mental</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample21" role="button" aria-expanded="false" aria-controls="collapseExample21">Medical Xpress</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample22" role="button" aria-expanded="false" aria-controls="collapseExample22">Psychreg</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample23" role="button" aria-expanded="false" aria-controls="collapseExample23">Folha Equilíbrio Mente</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample24" role="button" aria-expanded="false" aria-controls="collapseExample24">PsychCrunch</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample25" role="button" aria-expanded="false" aria-controls="collapseExample25">A Mente é Maravilhosa-Neurociência</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample26" role="button" aria-expanded="false" aria-controls="collapseExample26">A Mente é Maravilhosa-Psicologia</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample27" role="button" aria-expanded="false" aria-controls="collapseExample27">A Mente é Maravilhosa-Relações</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample28" role="button" aria-expanded="false" aria-controls="collapseExample28">A Mente é Maravilhosa-Saúde</a>')
    file.write('<a class="btn btn-space btn-outline-info btn-lg" data-bs-toggle="collapse" href="#collapseExample29" role="button" aria-expanded="false" aria-controls="collapseExample29">Big Think</a>')
    file.write('</p>')

# Criação das Classes com o conteúdo dos Botões (Usando modo append 'a')
with open(namefile, "a", encoding="utf-8") as file:
    # 0 - Very Well
    file.write('<div class="collapse show" id="collapseExample0" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[0] is not None:
        for x in parser[0].find_all("section"):
            for z in x.find_all("a", href=True):
                file.write("<a href=" + z.get("href") + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 1 - Psychology Today
    file.write('<div class="collapse" id="collapseExample1" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[1] is not None:
        for x in parser[1].find_all("div", class_="layout-content-main"):
            for z in x.find_all("a"):
                file.write("<a href=" + links[1] + z.get("href") + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 2 - Scientific American
    file.write('<div class="collapse" id="collapseExample2" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[2] is not None:
        for x in parser[2].find_all("div", class_="articleList-CcaLz root-fREBs"):
            for z in x.find_all("a"):
                file.write("<a href=" + "https://scientificamerican.com" + z.get("href") + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 3 - NIMH
    file.write('<div class="collapse" id="collapseExample3" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[3] is not None:
        for x in parser[3].find_all("article"):
            for z in x.find_all("a", class_="aggregated_term_news_link"):
                file.write("<a href=" + "https://nih.gov" + z.get("href") + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 4 - APA PsyPort
    file.write('<div class="collapse" id="collapseExample4" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[4] is not None:
        for x in parser[4].find_all("article"):
            for z in x.find_all("a"):
                file.write("<a href=" + z.get("href") + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 5 - APA Monitor
    file.write('<div class="collapse" id="collapseExample5" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[5] is not None:
        for x in parser[5].find_all("section", class_="linkWidget tile square"):
            for z in x.find_all("p", class_="title"):
                for n in z.find_all("a"):
                    file.write("<a href=" + "https://apa.org" + str(n.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 6 - Google Notícias
    file.write('<div class="collapse" id="collapseExample6" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[6] is not None:
        for x in parser[6].find_all("article"):
            for z in x.find_all("a", class_="VDXfz"):
                file.write("<a href=" + "https://google.com" + str(z.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 7 - Sociedade Brasileira de Psicologia
    file.write('<div class="collapse" id="collapseExample7" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[7] is not None:
        for x in parser[7].find_all("div", class_="content list"):
            for z in x.find_all("p"):
                for n in z.find_all("a"):
                    file.write("<a href=" + "https://sbponline.org.br" + str(n.get("href")) + ">" + n.text + "</a></br>")
    file.write("</div></div>")

    # 8 - Neuroscience
    file.write('<div class="collapse" id="collapseExample8" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[8] is not None:
        for x in parser[8].find_all("h3"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 9 - Positive Psychology
    file.write('<div class="collapse" id="collapseExample9" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[9] is not None:
        for x in parser[9].find_all("a"):
            for z in x.find_all("h3"):
                file.write("<a href=" + str(x.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 10 - Psychcentral
    file.write('<div class="collapse" id="collapseExample10" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[10] is not None:
        for x in parser[10].find_all("div", class_="css-fdjy12"):
            for z in x.find_all("a"):
                file.write("<a href=" + "https://psychcentral.com" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 11 - IQ's Corner
    file.write('<div class="collapse" id="collapseExample11" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[11] is not None:
        for x in parser[11].find_all("h3"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 12 - Happier Human
    file.write('<div class="collapse" id="collapseExample12" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[12] is not None:
        for x in parser[12].find_all("h2"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 13 - PsychNewsDaily
    file.write('<div class="collapse" id="collapseExample13" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[13] is not None:
        for x in parser[13].find_all("h2"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 14 - Psychiatric Times
    file.write('<div class="collapse" id="collapseExample14" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[14] is not None:
        for x in parser[14].find_all("a"):
            for z in x.find_all("h2"):
                file.write("<a href=" + "https://psychiatrictimes.com" + str(x.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 15 - APS
    file.write('<div class="collapse" id="collapseExample15" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[15] is not None:
        for x in parser[15].find_all("h3"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 16 - CFP
    file.write('<div class="collapse" id="collapseExample16" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[16] is not None:
        for x in parser[16].find_all("h3"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 17 - Psicologia USP
    file.write('<div class="collapse" id="collapseExample17" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[17] is not None:
        for x in parser[17].find_all("a"):
            for z in x.find_all("h3"):
                file.write("<a href=" + "https://scielo.br" + str(x.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 18 - Conselho Regional de Psicologia de São Paulo
    file.write('<div class="collapse" id="collapseExample18" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[18] is not None:
        for x in parser[18].find_all("a"):
            for z in x.find_all("h3"):
                file.write("<a href=" + str(x.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 19 - El País Psicologia
    file.write('<div class="collapse" id="collapseExample19" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[19] is not None:
        for x in parser[19].find_all("h2"):
            for z in x.find_all("a"):
                file.write("<a href=" + "https://elpais.com" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 20 - G1 Saúde
    file.write('<div class="collapse" id="collapseExample20" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[20] is not None:
        for x in parser[20].find_all("div", class_="_evt"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 21 - Medical Xpress
    file.write('<div class="collapse" id="collapseExample21" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[21] is not None:
        for x in parser[21].find_all("div"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 22 - Psychreg
    file.write('<div class="collapse" id="collapseExample22" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[22] is not None:
        for x in parser[22].find_all("div", class_="col-md-4"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 23 - Folha Equilíbrio Mente
    file.write('<div class="collapse" id="collapseExample23" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[23] is not None:
        for x in parser[23].find_all("a"):
            for z in x.find_all("h2"):
                file.write("<a href=" + str(x.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 24 - PsychCrunch
    file.write('<div class="collapse" id="collapseExample24" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[24] is not None:
        for x in parser[24].find_all("div", class_="libsyn-item-title"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # 25 - A Mente É Maravilhosa Neurociência
    file.write('<div class="collapse" id="collapseExample25" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[25] is not None:
        for x in parser[25].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
            file.write("<a href=" + "https://amenteemaravilhosa.com.br" + str(x.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 26 - A Mente É Maravilhosa Psicologia
    file.write('<div class="collapse" id="collapseExample26" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[26] is not None:
        for x in parser[26].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
            file.write("<a href=" + "https://amenteemaravilhosa.com.br" + str(x.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 27 - A Mente É Maravilhosa Relações
    file.write('<div class="collapse" id="collapseExample27" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[27] is not None:
        for x in parser[27].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
            file.write("<a href=" + "https://amenteemaravilhosa.com.br" + str(x.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 28 - A Mente É Maravilhosa Saúde
    file.write('<div class="collapse" id="collapseExample28" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[28] is not None:
        for x in parser[28].find_all("a", class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
            file.write("<a href=" + "https://amenteemaravilhosa.com.br" + str(x.get("href")) + ">" + x.text + "</a></br>")
    file.write("</div></div>")

    # 29 - Big Think Neuropsych
    file.write('<div class="collapse" id="collapseExample29" data-bs-parent="#myGroup">')
    file.write('<div class="card card-body">')
    if parser[29] is not None:
        for x in parser[29].find_all("h1", class_="card-headline"):
            for z in x.find_all("a"):
                file.write("<a href=" + str(z.get("href")) + ">" + z.text + "</a></br>")
    file.write("</div></div>")

    # Criação do script unificado e nativo do Bootstrap 5
    file.write('<div>')
    file.write('<script src="https://jsdelivr.net"></script>')
    file.write('</div></body></html>')
