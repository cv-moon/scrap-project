import csv
import time
import requests
from bs4 import BeautifulSoup

base_url = 'https://listado.mercadolibre.com.ec/computacion-notebooks/laptops_NoIndex_True'


def extract_urls_from_pagination(base_url):
    all_urls = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Aquí debes ajustar el selector según la estructura de tu HTML
    links = soup.find_all('a', class_='andes-pagination__link')  # Ejemplo de selector

    for link in links[1:-1]:
        href = link.get('href')
        all_urls.append(href)

    print("Obteniendo rutas...")

    return all_urls


def extract_products_links(all_urls):
    products_links = []
    for result in all_urls:
        response = requests.get(result)
        page = BeautifulSoup(response.text, 'html.parser')
        items = page.find_all('li', class_='ui-search-layout__item')
        for item in items:
            descrip = item.find('a')
            href = descrip.get('href')
            products_links.append(href)

    print("Obteniendo links de cada producto...")
    return products_links


def extract_seller_name(page):
    try:
        seller_name_element = page.find('span', class_='ui-pdp-seller__label-sold').find_next_sibling('span')
        seller_name = seller_name_element.text.strip() if seller_name_element else ""
    except AttributeError:
        seller_name = ""  # O cualquier otro valor por defecto
    return seller_name


def extract_nota_seller(page):
    try:
        seller_note_element = page.find('ul', class_='ui-seller-data-status__thermometer')
        seller_note = seller_note_element.text.strip() if seller_note_element else ""
    except AttributeError:
        seller_note = ""  # O cualquier otro valor por defecto
    return seller_note


def extract_status_product(page):
    try:
        status_element = page.find('span', class_='ui-pdp-subtitle')
        status = status_element.text.strip() if status_element else ""
    except AttributeError:
        status = ""  # O cualquier otro valor por defecto
    return status


def get_detail_item(product):
    print('link', product)
    response = requests.get(product)
    page = BeautifulSoup(response.text, 'html.parser')

    desc = page.find('h1')
    title = desc.get_text(strip=True)

    vendedor = extract_seller_name(page)
    calif_vendedor = extract_nota_seller(page)

    estado = extract_status_product(page)

    price_meta = page.find('meta', itemprop='price')
    precio = ""
    if price_meta:
        precio = price_meta['content']

    all_tables = page.find_all('table', class_='andes-table')

    marca = ""
    linea = ""
    modelo = ""
    memoria_ram = ""
    tipo_memoria_ram = ""
    memoria_video = ""
    ssd = ""
    hdd = ""
    marca_procesador = ""
    linea_procesador = ""
    modelo_procesador = ""
    nucleos = ""
    resolucion = ""
    sistema_operativo = ""
    version_sistema = ""
    edicion_sistema = ""

    # Iterate through the table rows
    for table in all_tables:
        for row in table.find_all('tr'):

            header = row.find(['div', 'th'], class_=['andes-table__header__container', 'andes-table__header'])
            data = row.find(['span', 'td'], class_=["andes-table__column--value", 'andes-table__column'])

            header_text = header.text.strip()
            data_text = data.text.strip()
            if "Marca" == header_text:
                marca = data_text
            elif "Línea" == header_text:
                linea = data_text
            elif "Modelo" == header_text:
                modelo = data_text
            elif "Memoria RAM" == header_text:
                memoria_ram = data_text
            elif "Tipo de memoria RAM" == header_text:
                tipo_memoria_ram = data_text
            elif "Memoria de video" == header_text:
                memoria_video = data_text  # Extract the memory part
            elif "Capacidad de disco SSD" == header_text:
                ssd = data_text
            elif "Capacidad del disco rígido" == header_text:
                hdd = data_text
            elif "Marca del procesador" == header_text:
                marca_procesador = data_text
            elif "Línea del procesador" == header_text:
                linea_procesador = data_text
            elif "Modelo del procesador" == header_text:
                modelo_procesador = data_text
            elif "Cantidad de núcleos" == header_text:
                nucleos = data_text
            elif "Resolución de la pantalla" == header_text:
                resolucion = data_text
            elif "Nombre del sistema operativo" == header_text:
                sistema_operativo = data_text
            elif "Versión del sistema operativo" == header_text:
                version_sistema = data_text
            elif "Edición del sistema operativo" == header_text:
                edicion_sistema = data_text
    print("Obteniendo detalles por producto...")
    return [marca, linea, modelo, memoria_ram, tipo_memoria_ram, memoria_video, ssd, hdd, marca_procesador,
            linea_procesador, modelo_procesador, nucleos, resolucion, sistema_operativo, version_sistema,
            edicion_sistema, precio, estado, vendedor, calif_vendedor]


def generate_csv(products):
    print("Generando csv...")
    cabeceras = ['marca', 'linea', 'modelo', 'memoria_ram', 'tipo_memoria_ram', 'memoria_video', 'ssd', 'hdd',
                 'marca_procesador', 'linea_procesador', 'modelo_procesador', 'nucleos', 'resolucion',
                 'sistema_operativo', 'version_sistema', 'edicion_sistema', 'precio', 'estado', 'vendedor',
                 'calif_vendedor']

    # Nombre del archivo CSV
    nombre_archivo = 'laptops.csv'

    # Abrir el archivo en modo escritura
    with open(nombre_archivo, 'w', newline='') as csvfile:
        # Crear un objeto escritor CSV
        writer = csv.writer(csvfile)

        # Escribir la fila de cabeceras
        writer.writerow(cabeceras)

        # Escribir las filas de datos
        writer.writerows(products)

    print(f"Archivo CSV '{nombre_archivo}' creado exitosamente.")


urls = extract_urls_from_pagination(base_url)
links_products = extract_products_links(urls)
products_arr = []
count = 0

current = 0
page_size = 100
total_pages = len(links_products)

while current * page_size < len(links_products):
    start_index = current * page_size
    end_index = start_index + page_size
    for url in links_products[start_index:end_index]:
        detail_product = get_detail_item(url)
        products_arr.append(detail_product)
        count += 1
        print(count)
    current += 1
    time.sleep(3)

generate_csv(products_arr)
