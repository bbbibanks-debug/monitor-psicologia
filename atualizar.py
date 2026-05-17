# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta

# Força o fuso horário de Brasília (-3) na geração do HTML
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
data_e_hora_sao_paulo = datetime.now(timezone.utc).astimezone(fuso_horario)

namefile = "index.html"

links = [
    "https://verywellmind.com", "https://psychologytoday.com", "https://scientificamerican.com",
    "https://nih.gov", "https://apa.org", "https://apa.org",
    "https://google.com", "https://sbponline.org.br",
    "https://neurosciencenews.com", "https://positivepsychology.com", "https://psychcentral.com", "http://iqscorner.com",
    "https://happierhuman.com", "https://psychnewsdaily.com", "https://psychiatrictimes.com",
    "https://psychologicalscience.org", "https://cfp.org.br", "https://scielo.br",
    "https://crpsp.org", "https://elpais.com", "https://globo.com",
    "https://medicalxpress.com", "https://psychreg.org", "https://uol.com.br", 
    "https://libsyn.com", "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br",
    "https://amenteemaravilhosa.com.br", "https://amenteemaravilhosa.com.br", "https://bigthink.com"
]

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
nomes_botoes = [
    "VeryWell Mind", "Psychology Today", "Scientific American", "NIMH (Research Highlights)",
    "APA PsyPort", "APA Monitor", "Google Notícias", "SBP Notícias", "Neuroscience News",
    "Positive Psychology", "Psych Central", "IQ`s Corner", "Happier Human", "PsyNewsDaily",
    "Psychiatric Times", "APS", "CFP", "Psicologia USP", "CRP-SP", "El País Psicologia",
    "G1 Saúde Mental", "Medical Xpress", "Psychreg"
]

responder = [None] * len(links)
for x in range(len(links)):
    try:
        response = requests.get(links[x], headers=header, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar {links[x]}: {e}")

file = open(namefile, "w", encoding="utf-8")
file.write('<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
file.write('<link rel="stylesheet" href="https://bootstrapcdn.com"><title>PSI LINKS BOARD</title></head>')
file.write('<body><div class="container mt-5">')
file.write('<h1> PSI MONITOR</h1>')
# ESSA LINHA IMPRIME O HORÁRIO EXATO DA RASPAGEM NA PÁGINA
file.write(f'<p class="text-muted">Última atualização automática: {data_e_hora_sao_paulo.strftime("%d/%m/%Y às %H:%M")} (Horário de Brasília)</p><hr><p>')

for idx, nome in enumerate(nomes_botoes):
    if idx < len(links):
        file.write(f'<a class="btn btn-space btn-outline-info btn-lg m-1" href="{links[idx]}" target="_blank" role="button">{nome}</a>\n')

file.write('</p></div></body></html>')
file.close()
print("Script atualizar.py reconfigurado para fuso horário local!")
