import requests
from bs4 import BeautifulSoup

resp = requests.get('https://listado.mercadolibre.com.ec/computacion-notebooks/laptops_NoIndex_True')
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

    return all_urls


def extract_products_links(all_urls):
    products_links = []
    for result in all_urls:
        response = requests.get(result)
        page = BeautifulSoup(response.text, 'html.parser')
        items = page.find_all('li', class_='ui-search-layout__item')
        for item in items[:1]:
            descrip = item.find('a')

            href = descrip.get('href')
            products_links.append(href)

    return products_links


def get_detail_item(products):
    for item in products[:1]:
        response = requests.get(item)
        page = BeautifulSoup(response.text, 'html.parser')

        desc = page.find('h1')
        title = desc.get_text(strip=True)

        find_seller = page.find('button', class_='ui-pdp-seller__link-trigger-button')
        seller = find_seller.find_all('span')[1]
        name_sell = seller.text.strip()

        status_product = page.find('span', class_='ui-pdp-subtitle')
        statustext = status_product.text.strip()

        price_meta = page.find('meta', itemprop='price')
        if price_meta:
            price = price_meta['content']
        else:
            price = None



urls = extract_urls_from_pagination(base_url)
links_products = extract_products_links(urls)
get_detail_item(links_products)
