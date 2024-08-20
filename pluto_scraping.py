#Importo todas las librerias

import requests
import re
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin


# Iniciar el contador de tiempo
start_time = time.time()

## Busco el html para las peliculas en OnDemand 
url='https://pluto.tv/latam/on-demand/618da9791add6600071d68b0'
# Enviar una solicitud HTTP GET a la URL
page=requests.get(url)
# Analizando el contenido HTML usando BeautifulSoup con 'html.parser'
soup=BeautifulSoup(page.text,'html.parser')

## Busco todos los generos de peliculas

movie_url=[]
# Busco los urls de los generos para las peliculas
movie_container=soup.find_all('a',{'type': 'button'},class_='')
for movie in movie_container:
       movie_url.append(movie['href'])

base_url='https://pluto.tv/latam/on-demand/618da9791add6600071d68b0'
movies=[]
for relative_url in movie_url :
    absolute_url = urljoin(base_url, relative_url)
    movies.append(absolute_url)

## Busco los titulos de los generos de peliculas
movie_title = []
movie_container = soup.find_all('a', {'type': 'button'},class_='')
for movie in movie_container:
    # Obtengo el texto entre las etiquetas <a></a> y lo limpio de espacios innecesarios
    title = movie.get_text(strip=True)
    movie_title.append(title)

## Busco los titulos de todas las peliculas, dentro de todos los generos

titles = []
for url in movies:
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Filtrar las secciones que contienen películas
        movie_sections = soup.find_all('div', class_='body-0-2-14')
        
        for section in movie_sections:
            # Dentro de cada sección, buscar los elementos <li>
            for li in section.find_all('li'):
                # Buscar la etiqueta <img> con el atributo alt
                img_tag = li.find('img', alt=True)
                
                if img_tag:
                    # Extraer el título de la película desde el atributo alt
                    titles.append(img_tag['alt'])

## Busco los URLs de todas las peliculas

#Lista para almacenar los URLs de las películas
movie_links = []
# Definir la URL base
base_url = "https://pluto.tv"
# Iterar sobre cada URL
for url in movies:
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Filtrar las secciones que contienen películas
        movie_sections = soup.find_all('div', class_='body-0-2-14') 
        for section in movie_sections:
            # Dentro de cada sección, buscar los elementos <li>
            for li in section.find_all('li'):
                # Buscar la etiqueta <a> con el atributo href
                a_tag = li.find('a', href=True)
                
                if a_tag:
                    # Construir la URL completa usando base_url y el atributo href
                    full_url = base_url + a_tag['href'] + '/details'
                    # Agregar la URL completa a la lista
                    movie_links.append(full_url)

## Busco las duraciones de todas las peliculas

# Lista para almacenar las duraciones de las películas
durations = []
# Función para procesar una URL y extraer la duración
def get_movie_duration(url):
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar la lista <ul> con la clase que contiene la metadata
        metadata_list = soup.find('ul', class_='metadata-0-2-15')
        if metadata_list:
            # Iterar sobre cada <li> en la lista de metadata
            for li in metadata_list.find_all('li'):
                # Verificar si el texto dentro del <li> contiene "hr" o "min"
                if 'hr' in li.text or 'min' in li.text:
                    # Devolver la duración encontrada
                    return li.text.strip()
    # Si no se encuentra la duración o la solicitud falla, devolver "N/A"
    return "Es una serie"

# Ejecutar el proceso de scraping en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_movie_duration, movie_links)
# Agregar los resultados a la lista de duraciones
durations.extend(results)

## Busco las descripciones de todas las peliculas

# Lista para almacenar las descripciones de las películas
descriptions = []
# Función para procesar una URL y extraer la descripción
def get_movie_description(url):
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar el div con la clase que contiene la descripción
        description_div = soup.find('div', class_='description-0-2-16')
        if description_div:
            # Extraer el texto de la etiqueta <p> dentro del div de descripción
            return description_div.find('p').text.strip()
# Ejecutar el proceso de scraping en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_movie_description, movie_links)
# Agregar los resultados a la lista de descripciones
descriptions.extend([description for description in results if description])

## busco el html para las series en Ondemand

url = 'https://pluto.tv/latam/on-demand/619043246d03190008131b89'
# Sending an HTTP GET request to the URL
page=requests.get(url)
# Parsing the HTML content using BeautifulSoup with the 'html.parser'
soup=BeautifulSoup(page.text,'html.parser')

## Busco los URls de todos los generos de las series

# Lista para almacenar los URLs de las series
series_url = []
    # Encontrar los elementos que contienen los URLs de las series
series_container = soup.find_all('a', {'type': 'button'}, class_='')
    # Extraer y agregar los URLs relativos a la lista
for series in series_container:
        series_url.append(series['href'])
    # Lista para almacenar los URLs absolutos de las series
base_url = 'https://pluto.tv/latam/on-demand/619043246d03190008131b89'
series = []
    # Convertir los URLs relativos en URLs absolutos
for relative_url in series_url:
        absolute_url = urljoin(base_url, relative_url)
        series.append(absolute_url)

## Busco los titulos de todos los generos de las series

series_title = []
    # Encuentra todos los elementos 'a' que tienen el atributo 'type="button"'
series_container = soup.find_all('a', {'type': 'button'}, class_='')
    # Extrae y agrega los títulos a la lista
for series in series_container:
        # Obtener el texto entre las etiquetas <a></a> y limpiarlo de espacios innecesarios
        title = series.get_text(strip=True)
        series_title.append(title)

series= ['https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/62473ee1a8099000076c0783', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/625db92c5c4b590007b808c6', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/63dd2358a8b22700082367ff', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941e09db549e0007ef2dc9', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941de9e03c74000701ed4f', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dc7fd0bc30007db1b6d', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e2f061eeb7c04000967bf70', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e45bbf395fb000009945cf0', 'https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d']

## Busco los titulos de todas las series, para todos los generos
# Lista para almacenar los títulos de las series
titles2 = []
# Iterar sobre cada URL en la lista de series
for url in series:
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)  
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')   
        # Filtrar las secciones que contienen series
        series_sections = soup.find_all('div', class_='body-0-2-14')  
        for section in series_sections:
            # Dentro de cada sección, buscar los elementos <li>
            for li in section.find_all('li'):
                # Buscar la etiqueta <img> con el atributo alt
                img_tag = li.find('img', alt=True)
                
                if img_tag:
                    # Extraer el título de la serie desde el atributo alt
                    titles2.append(img_tag['alt'])

## Busco los URLs de todas las series, para todos los generos
# Lista para almacenar los URLs de las series
series_links = []
# Definir la URL base
base_url = "https://pluto.tv"
# Iterar sobre cada URL
for url in series:
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')    
        # Filtrar las secciones que contienen series
        series_sections = soup.find_all('div', class_='body-0-2-14')      
        for section in series_sections:
            # Dentro de cada sección, buscar los elementos <li>
            for li in section.find_all('li'):
                # Buscar la etiqueta <a> con el atributo href
                a_tag = li.find('a', href=True)
                if a_tag:
                    # Construir la URL completa usando base_url y el atributo href
                    full_url = base_url + a_tag['href'] + '/season/1'
                    # Agregar la URL completa a la lista
                    series_links.append(full_url)

## Busco la duracion de todas las series: temporadas, episodios, tiempo promedio entre episodios
# Lista para almacenar la información de las series
series_info = []
# Función para procesar una URL y extraer la información de temporadas, episodios y duración
def get_series_info(url):
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url) 
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encontrar todos los elementos <p> que contienen la metadata de los episodios
        episode_metadata = soup.find_all('p', class_='episode-metadata-atc')
        # Crear listas para almacenar temporadas, episodios y duraciones
        seasons = []
        episodes = []
        durations = []
        # Iterar sobre cada elemento de metadata de episodio
        for metadata in episode_metadata:
            # Buscar el patrón TnEm y duración en minutos usando una expresión regular
            match = re.search(r'T(\d+)E(\d+)\s+(\d+)\smin', metadata.text)
            if match:
                season = int(match.group(1))
                episode = int(match.group(2))
                duration = int(match.group(3))
                # Agregar los valores extraídos a las listas correspondientes
                seasons.append(season)
                episodes.append(episode)
                durations.append(duration)
        # Verificar si se encontraron episodios y temporadas
        if seasons and episodes:
            total_seasons = max(seasons)
            total_episodes = max(episodes)
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            # Devolver la información formateada
            return f"{total_seasons} temporadas, {total_episodes} episodios, ~{int(avg_duration)}m por episodio"
    # Si no se encuentra la información, devolver "N/A"
    return "N/A"
# Ejecutar el proceso de scraping en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_series_info, series_links)
# Agregar los resultados a la lista de información de las series
series_info.extend(results)

## Busco las descripciones para todas las series

# Lista para almacenar las descripciones de las series
series_description = []
# Función para procesar una URL y extraer la descripción de la serie
def get_series_description(url):
    # Enviar una solicitud HTTP GET a la URL
    response = requests.get(url)
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encontrar el div que contiene la descripción de la serie
        description_div = soup.find('div', class_='description-0-2-16')
        if description_div:
            # Extraer el texto de la etiqueta <p> dentro del div de descripción
            description = description_div.find('p').text.strip()
            return description
    # Si no se encuentra la descripción, devolver "N/A"
    return "N/A"
# Ejecutar el proceso de scraping en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(get_series_description, series_links)
# Agregar los resultados a la lista de descripciones de las series
series_description.extend(results)

## Busco el html para los canales en LiveTV
# Specifying the URL from which tv show related data will be fetched
tv_url='https://pluto.tv/latam/live-tv'
# Sending an HTTP GET request to the URL
page=requests.get(tv_url)
# Parsing the HTML content using BeautifulSoup with the 'html.parser'
soup=BeautifulSoup(page.text,'html.parser')

## Busco los titulos de todos los canales
channels_titles = []
# Encuentra todos los elementos 'a' que tienen el atributo 'type="button"'
movie_container = soup.find_all('a', {'type': 'button'})
# Extrae y agrega los títulos a la lista
for movie in movie_container:
    # Buscar el <span> dentro del <a> que contiene el título del canal
    span = movie.find('span')
    if span:
        # Obtener el texto entre las etiquetas <span></span> y limpiarlo de espacios innecesarios
        title = span.get_text(strip=True)
        channels_titles.append(title)

## Busco los URLs para todos los canales

channels_urls = []
# Encuentra todos los elementos 'li' con la clase 'channelItem-0-2-25'
li_items = soup.find_all('li', class_='channelItem-0-2-25')
# Extrae y agrega los URLs a la lista
for li in li_items:
    # Buscar el enlace <a> dentro de cada <li> con 'type="button"'
    a_tag = li.find('a', {'type': 'button'})
    if a_tag:
        # Obtener el URL del canal desde el atributo href
        url = urljoin("https://pluto.tv", a_tag['href']) 
        channels_urls.append(url)

## Busco las descripciones para todos los canales

channels_descriptions = []
# Encuentra todos los elementos 'li' con la clase 'channelItem-0-2-25'
li_items = soup.find_all('li', class_='channelItem-0-2-25')
# Extrae y agrega las descripciones a la lista
for li in li_items:
    # Buscar la etiqueta <img> dentro de cada <li>
    img_tag = li.find('img')
    if img_tag:
        # Obtener la descripción desde el atributo alt
        description = img_tag.get('alt', '').strip()  # Obtener el valor de 'alt' y eliminar espacios innecesarios
        channels_descriptions.append(description)

## Obtengo un .csv para todos los datos que obtube

# Concatenar las listas de películas y series
titles_combined = titles + titles2 + channels_titles
links_combined = movie_links + series_links + channels_urls
durations_combined = durations + series_info 
descriptions_combined = descriptions + series_description +channels_descriptions

# Crear un diccionario de datos con las listas combinadas
data_dict = {
    'Movies, Series and Channels names': titles_combined,
    'Movies, Series and Channels urls': links_combined,
    'Duration': durations_combined,
    'Description': descriptions_combined
}

# Verificar la longitud de cada lista en el diccionario
for key, value in data_dict.items():
    print(f"Length of {key}: {len(value)}")

# Si las longitudes son diferentes, encontrar la longitud de la lista más larga
max_length = max(len(lst) for lst in data_dict.values())

# Rellenar las listas más cortas con 'N/A'
for key, value in data_dict.items():
    if len(value) < max_length:
        data_dict[key] += ['N/A'] * (max_length - len(value))

df_movie = pd.DataFrame(data_dict)

# Calcular el tiempo total de ejecución
end_time = time.time()
execution_time = end_time - start_time

# Redondear el tiempo a segundos enteros
execution_time_seconds = int(execution_time)

# Nombre del archivo con el tiempo de ejecución en segundos incluido
filename = f"pluto_{execution_time_seconds}s.csv"

# Exportar el DataFrame a un archivo CSV
df_movie.to_csv(filename, index=False, encoding='utf-8-sig')

# Imprimir el nombre del archivo y el tiempo de ejecución
print(f"Archivo CSV exportado exitosamente como {filename}.")
print(f"Tiempo de ejecución: {execution_time_seconds} segundos.")