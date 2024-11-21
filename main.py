import requests
from bs4 import BeautifulSoup


class Item:
    def __init__(self, titulo, descripcion, precio):
        self.titulo = titulo
        self.descripcion = descripcion
        self.precio = precio

    def __str__(self):
        return f"{self.titulo}, {self.descripcion}, {self.precio}"


listUrl = [
    'https://listado.mercadolibre.com.ec/computacion-notebooks/laptops_Desde_97_NoIndex_True',
    # 'https://listado.mercadolibre.com.ec/computacion-notebooks/laptops_Desde_145_NoIndex_True',
    # 'https://listado.mercadolibre.com.ec/computacion-notebooks/laptops_Desde_193_NoIndex_True'
]
for url in listUrl:
    resp = requests.get(url)

    listaItems = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')

        for item in items:
            titulo = item.find('span', class_='poly-component__brand')

            if titulo:
                tituloTxt = titulo.get_text(strip=True)

                descripH2 = item.find('h2', class_='poly-box poly-component__title')

                if descripH2:  # Verifica si se encontró el <h2>
                    descrip = descripH2.find('a')

                    if descrip:  # Verifica si se encontró el <a>

                        descripTxt = descrip.get_text(strip=True)
                        precio = item.find('span', class_='andes-money-amount__fraction')

                        if precio:
                            preciotxt = precio.get_text(strip=True)

                            listaItems.append(Item(tituloTxt, descripTxt, preciotxt))

        for persona in listaItems:
            print(persona)
    else:
        print("Error")
