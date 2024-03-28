import requests
from bs4 import BeautifulSoup
import os

# URL du flux RSS
url = "https://www.portail-ie.fr/feed/"

# Téléchargement du contenu du flux RSS
response = requests.get(url)
rss_content = response.content

# Analyse du contenu XML du flux RSS
soup = BeautifulSoup(rss_content, "xml")

# Récupération de tous les éléments "item"
articles = soup.find_all("item")

# Dossier de destination pour les fichiers texte
output_folder = "articles"
os.makedirs(output_folder, exist_ok=True)

# Parcours de chaque article et enregistrement dans un fichier texte distinct
for article in articles:
    title = article.find("title").get_text()
    content = article.find("content:encoded").get_text()

    # Nettoyage du titre pour qu'il soit utilisable comme nom de fichier
    clean_title = title.replace(":", "").replace("/", "").replace("?", "").replace("!", "").replace("|", "").replace(
        "\"", "'")

    # Analyse du contenu HTML de l'article
    soup_content = BeautifulSoup(content, "html.parser")

    # Extraction du texte principal de l'article
    article_content = "\n".join(paragraph.get_text() for paragraph in soup_content.find_all("p"))

    # Nettoyage du contenu de l'article
    separator = "Pour aller plus loin :"
    if separator in article_content:
        article_content = article_content.split(separator)[0]

    # Chemin du fichier texte pour cet article
    filename = os.path.join(output_folder, f"{clean_title}.txt")

    # Enregistrement du contenu de l'article dans le fichier texte
    with open(filename, "w", encoding="utf-8") as file:
        file.write(article_content)

    print(f"Article enregistré : {filename}")
