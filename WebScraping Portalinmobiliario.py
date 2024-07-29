#Rastrear las direcciones de los inmuebles en distintas publicaciones guardadas en un archivo csv e imprimirlas en la terminal
# import libraries 
from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
from selenium import webdriver

sys.stdout.reconfigure(encoding='utf-8')

import smtplib


# Leer las URLs desde el archivo CSV
csv_file = 'urls_inmuebles.csv'
df = pd.read_csv(csv_file)
#browser = webdriver.Chrome()

for url in df['url']:

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #browser.get(url)

    # Connect to Website and pull in data

    #url = 'https://www.portalinmobiliario.com/arriendo/departamento/san-joaquin-metropolitana/888888369-edificio-altavista-nva#position%3D2%26search_layout%3Dgrid%26type%3Ditem%26tracking_id%3Dac0efcb3-f36a-46af-8683-5a3d67b230cc'

    # Realizar la solicitud GET para obtener el contenido de la página
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:

        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Encontrar el primer div con la clase 'ui-vip-location'
        parent_div = soup.find('div', class_='ui-vip-location')

        if parent_div:
            # Encontrar el primer div hijo con la clase 'ui-pdp-media ui-vip-location__subtitle ui-pdp-color--BLACK'
            child_div = parent_div.find('div', class_='ui-pdp-media ui-vip-location__subtitle ui-pdp-color--BLACK')
        
            if child_div:
            
                # Encontrar la etiqueta <p> con la clase específica dentro del div padre
                p_tag = child_div.find('p', class_='ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title')
        
                if p_tag:
                    # Obtener el texto del <p>
                    text = p_tag.get_text(strip=True)
                    print(text)
                else:
                    print("No se encontró la etiqueta <p> con la clase especificada.")

            else:
                print("No se encontró el div hijo con la clase especificada.")
        else:
            print("No se encontró el div padre con la clase especificada.")

    else:
        print(f"Error al recuperar la página. Código de estado: {response.status_code}")
