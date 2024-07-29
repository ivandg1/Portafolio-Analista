#Se realiza Scraping en las publicaciones, cuyas url están guardadas en un archivo csv, y se obtiene el precio y la dirección de los inmuebles de cada una, 
#Los datos son llevados a un nuevo archivo csv.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Leer las URLs desde el archivo CSV
csv_file = 'urls_inmuebles.csv'
df = pd.read_csv(csv_file)

# Lista para almacenar los resultados
data = []

# Iterar sobre las URLs en la columna A del archivo CSV
for url in df['url']:  # Asegúrate de que la columna se llama 'A' o ajusta el nombre según corresponda
    # Realizar la solicitud GET para obtener el contenido de la página
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Especificar la codificación correcta
        response.encoding = response.apparent_encoding
        
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar la dirección
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
                    address_text = p_tag.get_text(strip=True)
                else:
                    address_text = "No se encontró la etiqueta <p> con la clase especificada."

            else:
                address_text="No se encontró el div hijo con la clase especificada."
        else:
            address_text="No se encontró el div padre con la clase especificada."
        
        # Encontrar el precio
        price = soup.find('span', class_='andes-money-amount__fraction')
        price_text = price.get_text(strip=True) if price else 'No encontrado'
        
        # Agregar los resultados a la lista
        data.append({'url': url, 'direccion': address_text, 'precio': price_text})
    else:
        data.append({'url': url, 'direccion': 'Error al recuperar', 'precio': 'Error al recuperar'})

# Crear un DataFrame con los resultados
results_df = pd.DataFrame(data)

# Guardar los resultados en un archivo CSV
results_df.to_csv('arriendos_santiago.csv', index=False, encoding='utf-8')

print("Scraping completado y resultados guardados en 'arriendos_santiago.csv'.")
