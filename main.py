import os
import requests
from bs4 import BeautifulSoup


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_images(url, folder_name):
    create_folder(folder_name)

    # User-Agent Header hinzufügen, um sich als Browser auszugeben
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        for i, img in enumerate(images):
            img_url = img.get('src')
            if img_url and 'http' in img_url:
                try:
                    image_response = requests.get(img_url, headers=headers)
                    if image_response.status_code == 200:
                        # Den Dateinamen aus dem Bild-URL extrahieren
                        image_name = os.path.join(folder_name, f'image_{i + 1}.jpg')
                        with open(image_name, 'wb') as f:
                            f.write(image_response.content)
                        print(f'Bild {i + 1} heruntergeladen: {image_name}')
                    else:
                        print(f'Fehler beim Herunterladen von Bild {i + 1}: {img_url}')
                except Exception as e:
                    print(f'Fehler beim Herunterladen von Bild {i + 1}: {e}')
            else:
                print(f'Ungültige Bild-URL in Bild {i + 1}: {img_url}')
    else:
        print(f'Fehler beim Abrufen der Webseite: {url}')


if __name__ == '__main__':
    # URL der Webseite, von der du Bilder herunterladen möchtest
    url = 'https://www.google.com/search?client=firefox-b-d&sxsrf=APwXEdeh5oSkWy6kFE1kV9GuuGRdjYHfbA:1688026837039&q=hide+face&tbm=isch&sa=X&ved=2ahUKEwjixPj_hej_AhWQSfEDHUrWCHwQ0pQJegQICRAB&biw=1920&bih=955&dpr=1'

    # Der Name des Ordners, in dem die Bilder gespeichert werden sollen
    folder_name = 'downloaded_images'

    download_images(url, folder_name)