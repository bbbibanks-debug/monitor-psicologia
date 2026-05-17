# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

# ==========================================
# CONFIG
# ==========================================

namefile = "index.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

SOURCES = [
    {
        "title": "VeryWell Mind",
        "url": "https://www.verywellmind.com/",
        "selector": "section a",
        "base": None
    },
    {
        "title": "Psychology Today",
        "url": "https://www.psychologytoday.com/us/news",
        "selector": ".layout-content-main a",
        "base": "https://www.psychologytoday.com"
    },
    {
        "title": "Scientific American",
        "url": "https://www.scientificamerican.com/mind-and-brain/",
        "selector": "a",
        "base": "https://www.scientificamerican.com"
    },
    {
        "title": "NIMH",
        "url": "https://www.nimh.nih.gov/news/research-highlights",
        "selector": "article a",
        "base": "https://www.nimh.nih.gov"
    },
    {
        "title": "Neuroscience News",
        "url": "https://neurosciencenews.com/",
        "selector": "h3 a",
        "base": None
    },
    {
        "title": "Psych Central",
        "url": "https://psychcentral.com/",
        "selector": "a",
        "base": "https://psychcentral.com"
    },
    {
        "title": "APA Monitor",
        "url": "https://www.apa.org/monitor",
        "selector": "a",
        "base": "https://www.apa.org"
    }
]

# ==========================================
# HTML START
# ==========================================

html = f"""
<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>PSI MONITOR</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

        body {{
            background-color: #111827;
            color: white;
            padding: 30px;
        }}

        .source-card {{
            margin-bottom: 20px;
        }}

        .article-link {{
            display: block;
            padding: 6px 0;
            color: #93c5fd;
            text-decoration: none;
        }}

        .article-link:hover {{
            color: white;
        }}

        .header-box {{
            margin-bottom: 40px;
        }}

    </style>

</head>

<body>

<div class="container">

    <div class="header-box">
        <h1 class="display-4">PSI MONITOR</h1>
        <p>
            Atualizado em:
            {datetime.now().strftime("%d/%m/%Y %H:%M")}
        </p>
    </div>

    <div class="accordion" id="accordionSources">
"""

# ==========================================
# SCRAPING
# ==========================================

for idx, source in enumerate(SOURCES):

    print(f"Coletando: {source['title']}")

    links_html = ""

    try:

        response = requests.get(
            source["url"],
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        found_links = soup.select(source["selector"])

        used = set()

        for tag in found_links:

            href = tag.get("href")
            text = tag.get_text(strip=True)

            if not href or not text:
                continue

            full_link = urljoin(
                source["base"] or source["url"],
                href
            )

            if full_link in used:
                continue

            used.add(full_link)

            links_html += f'''
                <a class="article-link"
                   href="{full_link}"
                   target="_blank">
                   {text}
                </a>
            '''

        if not links_html:
            links_html = "<p>Nenhum conteúdo encontrado.</p>"

    except Exception as e:

        links_html = f"""
            <div class="alert alert-danger">
                Erro ao carregar fonte:
                {str(e)}
            </div>
        """

    html += f"""

    <div class="accordion-item source-card">

        <h2 class="accordion-header" id="heading{idx}">

            <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse{idx}">

                {source['title']}

            </button>

        </h2>

        <div
            id="collapse{idx}"
            class="accordion-collapse collapse"
            data-bs-parent="#accordionSources">

            <div class="accordion-body">

                {links_html}

            </div>

        </div>

    </div>
"""

# ==========================================
# HTML END
# ==========================================

html += """

    </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
"""

# ==========================================
# SAVE FILE
# ==========================================

with open(namefile, "w", encoding="utf-8") as file:
    file.write(html)

print(f"Arquivo '{namefile}' criado com sucesso.")
