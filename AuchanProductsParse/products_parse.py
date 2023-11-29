import requests
from bs4 import BeautifulSoup
import openpyxl

# Важно не забыть обновить куки! иначе ничего работать не будет
cookie = {'qrator_jsr': '1701275055.915.PIaRKwTshc4Xmfnj-fk71dsmv4ad93ef6ppfstjr-00; qrator_jsid=1701275055.915.PIshc4Xmfnj-ess50tnleqpf9vad8resubt2upt46r22'}
data = []


def convert_to_excel(data):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet['A1'] = 'Наименование'
    worksheet['B1'] = 'Идентификатор'
    worksheet['C1'] = 'Цена'
    worksheet['D1'] = 'Промо цена'
    worksheet['E1'] = 'Бренд'
    worksheet['F1'] = 'Ссылка'

    for counter, items in enumerate(data, start=2):
        worksheet[counter][0].value = items[3]
        worksheet[counter][1].value = items[2]
        worksheet[counter][2].value = items[4]
        worksheet[counter][3].value = items[5]
        worksheet[counter][4].value = items[1]
        worksheet[counter][5].value = items[0]

    # Укажите свой путь! \\teams2.xlsx должен находится в конце пути
    workbook.save('D:\\Python Projects\\parser for the Auchan website\\teams2.xlsx')
    workbook.close()


def get_soup(url):
    with requests.get(url, cookies=cookie) as response:
        return BeautifulSoup(response.text, 'html.parser')


for i in range(1, 4):
    categories_page = get_soup('https://www.auchan.ru/'+f'catalog/kollekcii/gotovim-s-perchinkoy/?from=gotovim_s_perchinkoy_2022&page={i}')
    categories = categories_page.findAll('a', attrs={'class': 'productCardPictureLink active css-of3y3a'})

    for cat in categories:

        ulr_product = 'https://www.auchan.ru' + cat['href']
        subcategories_page = get_soup('https://www.auchan.ru'+cat['href'])
        subcategories = subcategories_page.findAll('main', {'class': 'css-164r41r'})

        for item in subcategories:

            brand_products = item.find('a', class_='css-dsyb4t').text
            id_product = item.find('td', class_='css-1v23ygr').text
            name_product = item.find('h1', class_='css-1dud7uh').text
            price_product = item.find('div', class_='css-1rwzh68')
            if price_product is not None:
                price_product = price_product.text.replace("C", "").strip()
            else:
                price_product = 'Цена отсутствует'

            promo_price = item.find('div', class_='css-1he77cg')
            if promo_price is not None:
                promo_price = promo_price.text
            else:
                promo_price = 'Цена отсутствует'

            data.append([ulr_product, brand_products, id_product, name_product, price_product, promo_price])


convert_to_excel(data)
