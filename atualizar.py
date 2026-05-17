
namefile = "index.html"

import requests
from bs4 import *
import os
import functools
import re
from datetime import datetime, timezone
from datetime import timedelta

#Time
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime("%d%m%Yday%H%Mtime")
namefile = str(data_e_hora_sao_paulo_em_texto)+".html"
namefile = "index.html"

#Mapping
links =["https://www.verywellmind.com/", "https://www.psychologytoday.com/us/news", "https://www.scientificamerican.com/mind-and-brain/","https://www.nimh.nih.gov/news/research-highlights",
"https://www.apa.org/news/psycport","https://www.apa.org/monitor","https://news.google.com/search?q=psicologia&hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
"https://www.sbponline.org.br/noticias","https://neurosciencenews.com/","https://positivepsychology.com/","https://psychcentral.com/",
"http://www.iqscorner.com/","https://www.happierhuman.com/","https://www.psychnewsdaily.com/","https://www.psychiatrictimes.com/",
"https://www.psychologicalscience.org/news","https://site.cfp.org.br/","https://www.scielo.br/j/pusp/","https://www.crpsp.org/impresso/index",
"https://brasil.elpais.com/noticias/psicologia/", "https://g1.globo.com/saude/saude-mental/","https://medicalxpress.com/psychology-news/",
"https://www.psychreg.org/","https://www1.folha.uol.com.br/equilibrio/mente/", "https://psychcrunch.libsyn.com/","https://amenteemaravilhosa.com.br/neurociencia/",
"https://amenteemaravilhosa.com.br/psicologia/","https://amenteemaravilhosa.com.br/relacoes/","https://amenteemaravilhosa.com.br/saude/",
"https://bigthink.com/neuropsych/"]
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"}

# Initialize responder and parser lists with None for all potential entries
responder = [None] * len(links)
parser = [None] * len(links)

for x in range(len(links)):
  try:
    response = requests.get(links[x], headers=header, timeout=15) # Added a timeout for robustness
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

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
file = open(namefile,"w")

#Criação do Head, Metas e Título, além do link do Bootstrap

file.write('<!DOCTYPE html>')
file.write('<html lang="pt-br">')
file.write('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">')
file.write('<title>PSI LINKS BOARD</title></head>')

#Criação do Body, Container e Botões
file.write('<body><div class="container" id="myGroup"><h1> PSI MONITOR</h1><p>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample"   role="button" aria-expanded="false" aria-controls="collapseExample">VeryWell Mind</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample1"  role="button" aria-expanded="false" aria-controls="collapseExample">Psychology Today</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample2"  role="button" aria-expanded="false" aria-controls="collapseExample">Scientific American</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample3"  role="button" aria-expanded="false" aria-controls="collapseExample">The National Institute of Mental Health (NIMH)</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample4"  role="button" aria-expanded="false" aria-controls="collapseExample">APA PsyPort</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample5"  role="button" aria-expanded="false" aria-controls="collapseExample">APA Monitor</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample6"  role="button" aria-expanded="false" aria-controls="collapseExample">Google Notícias</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample7"  role="button" aria-expanded="false" aria-controls="collapseExample">SBP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample8"  role="button" aria-expanded="false" aria-controls="collapseExample">Neuroscience</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample9"  role="button" aria-expanded="false" aria-controls="collapseExample">Positive Psichology</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample10"  role="button" aria-expanded="false" aria-controls="collapseExample">Positive Psychcentral</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample11"  role="button" aria-expanded="false" aria-controls="collapseExample">IQ`s Corner</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample12"  role="button" aria-expanded="false" aria-controls="collapseExample">Happier Human</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample13"  role="button" aria-expanded="false" aria-controls="collapseExample">PsyNewsDaily</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample14"  role="button" aria-expanded="false" aria-controls="collapseExample">Psychiatric Times</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample15"  role="button" aria-expanded="false" aria-controls="collapseExample">APS</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample16"  role="button" aria-expanded="false" aria-controls="collapseExample">CFP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample17"  role="button" aria-expanded="false" aria-controls="collapseExample">Psicologia USP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample18"  role="button" aria-expanded="false" aria-controls="collapseExample">Conselho Regional de Psicologia SP</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample19"  role="button" aria-expanded="false" aria-controls="collapseExample">El País Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample20"  role="button" aria-expanded="false" aria-controls="collapseExample">G1 Saúde Mental</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample21"  role="button" aria-expanded="false" aria-controls="collapseExample">Medical Xpress</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample22"  role="button" aria-expanded="false" aria-controls="collapseExample">Psychreg</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample23"  role="button" aria-expanded="false" aria-controls="collapseExample">Folha Equilíbrio Mente</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample24"  role="button" aria-expanded="false" aria-controls="collapseExample">PsychCrunch</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample25"  role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Neurociência</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample26"  role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Psicologia</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample27"  role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Relações</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample28"  role="button" aria-expanded="false" aria-controls="collapseExample">A Mente é Maravilhosa-Saúde</a>')
file.write('<a class="btn btn-space btn-outline-info btn-lg" data-toggle="collapse" href="#collapseExample29"  role="button" aria-expanded="false" aria-controls="collapseExample">Big Think</a>')


file.write('</p>')
file.close()
#Criação das Classes com o conteúdo do Botões

#Very Well
file = open(namefile,"a")
file.write('<div class="collapse show" id="collapseExample" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[0] is not None before proceeding
if parser[0] is not None:
  for x in parser[0].find_all("section"):
    for z in x.find_all("a",href=True):
      file.write("<a href="+ z.get("href")+">"+z.text+"</a>"+"</br>")
    else:
      pass
file.write("</div></div>")
file.close()

#Psychology Today
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample1" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[1] is not None before proceeding
if parser[1] is not None:
  for x in parser[1].find_all("div", class_="layout-content-main"):
    for z in x.find_all("a"):
      file.write("<a href="+ links[1]+z.get("href")+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Scientific American
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample2" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[2] is not None before proceeding
if parser[2] is not None:
  for x in parser[2].find_all("div","articleList-CcaLz root-fREBs"):
    for z in x.find_all("a"):
      file.write("<a href="+ "https://www.scientificamerican.com"+ z.get("href")+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#NIHM
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample3" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[3] is not None before proceeding
if parser[3] is not None:
  for x in parser[3].find_all("article"):
    for z in x.find_all("a", class_="aggregated_term_news_link"):
      file.write("<a href="+ "https://www.nimh.nih.gov"+ z.get("href")+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#APA PsyPort
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample4" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[4] is not None before proceeding
if parser[4] is not None:
  for x in parser[4].find_all("article"):
    for z in x.find_all("a"):
      file.write("<a href="+z.get("href")+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#APA Monitor
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample5" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[5] is not None before proceeding
if parser[5] is not None:
  for x in parser[5].find_all("section", class_= "linkWidget tile square"):
    for z in x.find_all("p", class_="title"):
      for n in z.find_all("a"):
        file.write("<a href="+ "https://www.apa.org"+str(n.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Google Notícias
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample6" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[6] is not None before proceeding
if parser[6] is not None:
  for x in parser[6].find_all("article"):
    for z in x.find_all("a", class_="VDXfz"):
      file.write("<a href="+ "https://news.google.com"+str(z.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Sociedade Brasileira de Psicologia
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample7" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[7] is not None before proceeding
if parser[7] is not None:
  for x in parser[7].find_all("div", class_="content list"):
    for z in x.find_all("p"):
      for n in z.find_all("a"):
        file.write("<a href="+ "https://www.sbponline.org.br"+str(n.get("href"))+">"+n.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#Neuroscience
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample8" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[8] is not None before proceeding
if parser[8] is not None:
  for x in parser[8].find_all("h3"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Positive Psichology
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample9" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[9] is not None before proceeding
if parser[9] is not None:
  for x in parser[9].find_all("a"):
    for z in x.find_all("h3"):
      file.write("<a href="+str(x.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#SPsychcentral
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample10" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[10] is not None before proceeding
if parser[10] is not None:
  for x in parser[10].find_all("div", class_="css-fdjy12"):
    for z in x.find_all("a"):
      file.write("<a href="+ "https://psychcentral.com/"+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#IQ`s Corner
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample11" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[11] is not None before proceeding
if parser[11] is not None:
  for x in parser[11].find_all("h3"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#IQ`s Corner
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample12" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[12] is not None before proceeding
if parser[12] is not None:
  for x in parser[12].find_all("h2"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#PsychNewsDaily
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample13" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[13] is not None before proceeding
if parser[13] is not None:
  for x in parser[13].find_all("h2"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Psychiatric Times
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample14" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[14] is not None before proceeding
if parser[14] is not None:
  for x in parser[14].find_all("a"):
    for z in x.find_all("h2"):
      file.write("<a href="+ "https://www.psychiatrictimes.com/"+str(x.get("href"))+">"+z.text+"</a>"+"</br>") # Changed z.get("href") to x.get("href")
file.write("</div></div>")
file.close()

#APS
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample15" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[15] is not None before proceeding
if parser[15] is not None:
  for x in parser[15].find_all("h3"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#CFP
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample16" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[16] is not None before proceeding
if parser[16] is not None:
  for x in parser[16].find_all("h3"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#Psicologia USP
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample17" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[17] is not None before proceeding
if parser[17] is not None:
  for x in parser[17].find_all("a"):
    for z in x.find_all("h3"):
      file.write("<a href="+ "https://www.scielo.br"+str(x.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Conselho Regional de Psicologia de São Paulo
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample18" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[18] is not None before proceeding
if parser[18] is not None:
  for x in parser[18].find_all("a"):
    for z in x.find_all("h3"):
      file.write("<a href="+str(x.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#EL País Psicologia
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample19" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[19] is not None before proceeding
if parser[19] is not None:
  for x in parser[19].find_all("h2"):
    for z in x.find_all("a"):
      file.write("<a href="+ "https://brasil.elpais.com/"+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#G1 Saúde
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample20" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[20] is not None before proceeding
if parser[20] is not None:
  for x in parser[20].find_all("div",class_="_evt"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#Medical Xpress
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample21" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[21] is not None before proceeding
if parser[21] is not None:
  for x in parser[21].find_all("div"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()


#Psychreg
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample22" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[22] is not None before proceeding
if parser[22] is not None:
  for x in parser[22].find_all("div",class_="col-md-4"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Folha Equilíbrio Mente
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample23" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[23] is not None before proceeding
if parser[23] is not None:
  for x in parser[23].find_all("a"):
    for z in x.find_all("h2"):
      file.write("<a href="+str(x.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#PsychCrunch
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample24" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[24] is not None before proceeding
if parser[24] is not None:
  for x in parser[24].find_all("div", class_="libsyn-item-title"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#A Mente É Maravilhosa Neurociência
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample25" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[25] is not None before proceeding
if parser[25] is not None:
  for x in parser[25].find_all("a",class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
      file.write("<a href="+ "https://amenteemaravilhosa.com.br"+str(x.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#A Mente É Maravilhosa Psicologia
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample26" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[26] is not None before proceeding
if parser[26] is not None:
  for x in parser[26].find_all("a",class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
      file.write("<a href="+ "https://amenteemaravilhosa.com.br"+str(x.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#A Mente É Maravilhosa Relações
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample27" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[27] is not None before proceeding
if parser[27] is not None:
  for x in parser[27].find_all("a",class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
      file.write("<a href="+ "https://amenteemaravilhosa.com.br"+str(x.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#A Mente É Maravilhosa Saúde
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample28" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[28] is not None before proceeding
if parser[28] is not None:
  for x in parser[28].find_all("a",class_="jsx-151512268 jsx-1424224867 default-a-link global-link jsx-3363598852"):
      file.write("<a href="+ "https://amenteemaravilhosa.com.br"+str(x.get("href"))+">"+x.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Big Think Neuropsych
file = open(namefile,"a")
file.write('<div class="collapse" id="collapseExample29" data-parent="#myGroup" Style>')
file.write('<div class="card card-body">')
# Check if parser[29] is not None before proceeding
if parser[29] is not None:
  for x in parser[29].find_all("h1",class_="card-headline"):
    for z in x.find_all("a"):
      file.write("<a href="+str(z.get("href"))+">"+z.text+"</a>"+"</br>")
file.write("</div></div>")
file.close()

#Criação dos scripts
file = open(namefile,"a")
file.write('<div>')
file.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>')
file.write('<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"></script>')
file.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>')
file.write('<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>')
file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>')
file.write('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>')
file.write('</div></body>')

#Fechanmento do Arquivo
file.close()
