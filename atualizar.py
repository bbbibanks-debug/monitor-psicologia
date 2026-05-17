import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta

data_e_hora_atuais = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

namefile = "index.html"

links = ["https://verywellmind.com", "https://psychologytoday.com", "https://scientificamerican.com","https://nih.gov",
"https://apa.org","https://apa.org","https://google.com",
"https://sbponline.org.br","https://neurosciencenews.com","https://positivepsychology.com","https://psychcentral.com",
"http://iqscorner.com","https://happierhuman.com","https://psychnewsdaily.com","https://psychiatrictimes.com",
"https://psychologicalscience.org","https://cfp.org.br","https://scielo.br","https://crpsp.org",
"https://elpais.com", "https://globo.com","https://medicalxpress.com",
"https://psychreg.org","https://uol.com.br", "https://libsyn.com","https://amenteemaravilhosa.com.br",
"https://amenteemaravilhosa.com.br","https://amenteemaravilhosa.com.br","https://amenteemaravilhosa.com.br",
"https://bigthink.com"]

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}

file = open(namefile,"w", encoding="utf-8")
file.write('<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com">')
file.write(f'<title>PSI LINKS BOARD</title></head><body><div class="container" id="myGroup"><h1 class="mt-5"> PSI MONITOR</h1><p class="text-muted">Atualizado automaticamente em: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")}</p><hr><div class="row">')

for idx, link in enumerate(links):
    file.write(f'<div class="col-md-4 mb-3"><a class="btn btn-block btn-outline-info" href="{link}" target="_blank">Link Fonte {idx+1}</a></div>')

file.write('</div></div></body></html>')
file.close()
print("Script atualizar.py pronto.")
