from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from entities.Product import Product
from urllib.parse import urlparse, urlunparse, urlencode
import os
import pandas as pd
from ui.components.MsgArea import MsgArea

# variáveis
PRODUCT_SELECTOR = 'produto'
PRODUCT_NAME_SELECTOR = 'div.titulo-e-preco > h2'
PRICE_PRODUCT_SELECTOR = 'p.preco-produto'
PRODUCT_IMG_SELECTOR = 'div.miniature > img.rounded-corners'
PAGE_SELECTOR = 'div.paginacao > ul > li'
PRODUCT_REF_SELECTOR = 'p.ref-produto'
PRODUCT_DESC_SELECTOR = 'div.detalhes-produto span'
CATALOG_CASHIER = 'div.caixa > h1'

class CatalogAnalyzer():
    folder_path = ''
    file_name = 'relatorio.xlsx'
    catalog_urls = ['https://vendasonline.wikisistemas.com.br/fba0ty3c']

    def __init__(self, msg: MsgArea):
        self.config()
        self.msg = msg
        

    def config(self):
        # config inicial
        options = Options()
        options.add_argument(r"--user-data-dir=C:\ChromeSelenium")
        options.add_argument("--profile-directory=Default")
        #options.add_argument("--start-minimized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options)
      

    def get_pages(self):
        pages = self.driver.find_elements(By.CSS_SELECTOR, PAGE_SELECTOR)
        return pages


    def count_pages(self):
        pages = self.get_pages()
        num_pages = int(len(pages) / 2)
        return num_pages


    def create_next_url(self, current_url: str, current_page: int):
        # url atual em forma de objeto
        url = urlparse(current_url)

        # cria parâmetros de busca
        query = {
            'pagina': current_page,
            'handler': 'pagina'
        }

        # transforma objeto query em string
        query_string = urlencode(query)

        # transforma url objeto em string
        new_url = urlunparse(url._replace(query=query_string))

        return new_url


    def create_table(self, products: list[Product], page = 1, sheet_name=''):

        table_path = self.folder_path + '/' + self.file_name

        products_data = []
        
        for product in products:
            products_data.append( {
                'Nome': product.name, 
                'Preco': product.price, 
                'Desc': product.desc, 
                'URL': product.url, 
                'Página': page, 
                'Ref': product.ref, 
                'Tags': product.get_tags()
                })

        df = pd.DataFrame(products_data)

        # Cria tabela se não existe
        if not os.path.exists(table_path):
                with pd.ExcelWriter(table_path, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

            
        else:
                with pd.ExcelWriter(
                    table_path,
                    engine="openpyxl",
                    mode="a",
                    if_sheet_exists="overlay"
                ) as writer:

                    # Carrega workbook para saber última linha
                    workbook = writer.book

                    if sheet_name in workbook.sheetnames:
                        startrow = workbook[sheet_name].max_row
                    else:
                        startrow = 0

                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False,
                        header=False,
                        startrow=startrow
                    )


    def get_products(self):
        products: list[Product] = []

        product_elements = self.driver.find_elements(By.CLASS_NAME, PRODUCT_SELECTOR)
        num_products = len(product_elements)

        for p in range(0, num_products):

            product_elements[p].click()
            sleep(0.2)

            # pega elementos
            product_name = self.driver.find_element(By.CSS_SELECTOR, PRODUCT_NAME_SELECTOR)
            img_elements = self.driver.find_elements(By.CSS_SELECTOR, PRODUCT_IMG_SELECTOR)
            price_element = self.driver.find_element(By.CSS_SELECTOR, PRICE_PRODUCT_SELECTOR)
            desc_elements = self.driver.find_elements(By.CSS_SELECTOR, PRODUCT_DESC_SELECTOR)
            ref_element = self.driver.find_element(By.CSS_SELECTOR, PRODUCT_REF_SELECTOR)

            # propriedades do produto
            name = product_name.text
            price = price_element.text
            ref = ref_element.text.lower().replace('referência: ', '')
            url = self.driver.current_url
            img = ''
            desc = ''
            tags = []

            if len(img_elements) > 0:
                img = img_elements[0].get_dom_attribute('src')

            for desc_element in desc_elements:
                texto = desc_element.text
                if len(texto) > 0:
                    desc += texto + '\n'

            if len(img) == 0:
                tags.append('(SEM IMAGEM)')

            if len(desc) == 0:
                tags.append('(SEM DESC)')

            # cria produto e adiciona na lista
            produto = Product(name, price, img , desc.strip(), url.strip(), ref, tags)
            products.append(produto)

            sleep(0.1)
            self.driver.back()

        return products


    def remove_old_file(self):
        path = self.folder_path + '/' + self.file_name
        if os.path.exists(path):
            os.remove(path)


    def analyze_catalog(self, url_catalog = ''):

        # entra no catalogo
        self.driver.get(url_catalog)
        sleep(0.5)

        # pega nome do catálogo
        catalog_name = self.driver.find_element(By.CSS_SELECTOR, CATALOG_CASHIER).text
        self.msg.set_msg('Análise: início', f'Começando análise no catálogo "{catalog_name}"')

        # conta o número de páginas
        num_pags = self.count_pages()
        self.msg.set_msg('Análise', f'Número de páginas: {num_pags}')

        # pega informações de cada produto em cada página
        for page in range(1, num_pags + 1):

            current_url = self.driver.current_url
            next_url = self.create_next_url(current_url, page + 1)
            self.msg.set_msg('Análise', f'Analisando URL "{current_url}\n"Página atual: {page}')

            # pega os produtos na página atual
            product = self.get_products()
            self.create_table(product, page, catalog_name)

            # vai para próxima página
            self.driver.get(next_url)
            sleep(0.5)


   