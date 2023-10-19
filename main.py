import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Die URL der Webseite, von der du Bilder herunterladen möchtest
url = 'https://unsplash.com/de/s/fotos/hidden-face'

# Der Name des Ordners, in dem die Bilder gespeichert werden sollen
folder_name = 'downloaded_images'

# Erstelle den Ordner, wenn er nicht existiert
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# User-Agent-Header hinzufügen, um sich als Browser auszugeben
headers = {'User-Agent': 'Mozilla/5.0'}

# HTTP-Anfrage an die Webseite senden
response = requests.get(url, headers=headers)

# Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
if response.status_code == 200:
    # HTML-Inhalt der Webseite analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Alle Bilder auf der Webseite finden
    images = soup.find_all('img')

    # Bilder herunterladen und im Ordner speichern
    for i, img in enumerate(images):
        img_url = img.get('src')
        if img_url and 'http' in img_url:
            try:
                # Vollständige Bild-URL erstellen (falls relativ)
                image_url = urljoin(url, img_url)

                # Den Dateinamen aus der URL extrahieren
                image_name = os.path.join(folder_name, f'image_{i + 1}.jpg')

                # Bild herunterladen und speichern
                image_data = requests.get(image_url).content
                with open(image_name, 'wb') as image_file:
                    image_file.write(image_data)

                print(f'Bild {i + 1} heruntergeladen: {image_name}')
            except Exception as e:
                print(f'Fehler beim Herunterladen von Bild {i + 1}: {e}')
        else:
            print(f'Ungültige Bild-URL in Bild {i + 1}: {img_url}')
else:
    print(f'Fehler beim Abrufen der Webseite: {url}')
