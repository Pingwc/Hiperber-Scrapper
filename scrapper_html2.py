from requests_html import HTMLSession
from bs4 import BeautifulSoup
import os
import pandas as pd
from compare_classes import Compare_class

Comparator=Compare_class()

#For some reason the xpath of the image of some products is different when there are 1 or more images
#First one when there are 2 or more images, 2nd and 3rd when there's only 1 image
list_xpath = ['//*[@id="infoproduct-content--image"]/div[1]/ngx-hm-carousel/div/section/article[1]/cmp-image-info-product/div/img',
              '//*[@id="infoproduct-content--image"]/div[2]/cmp-image-info-product/div/div[1]/div[2]/img',
              '//*[@id="infoproduct-content--image"]/div[2]/cmp-image-info-product/div/img']

base_url = input("Introduce the URL to scrape:  ")
name_file = input("Introduce the name for the file(must be format csv): ")
session = HTMLSession()
r = session.get(base_url)
r.html.render(sleep=2) #Sleep de al menos 1 segundo para que el headless browser pueda renderizar la mayoria del html del script


products = r.html.xpath('//*[@id="mod-shop"]/div[2]/div/mod-catalog/div/lib-grid/div/div/div[2]/div[2]/cmp-products-grid/div[1]', first=True)
product_list = []

category = r.html.find('#grid-title', first=True).text

for i in products.absolute_links:
    r = session.get(i)
    r.html.render(sleep=1)
    x = 0
    print(i)
    name = r.html.find('div.u-title-3', first=True).text
    print(name)
    brand = r.html.find('#infoproduct-content--brand', first=True)
    
    print(brand)
    brand1 = brand.attrs['']
    price = r.html.find('span.u-title-1', first=True).text
    image = r.html.xpath(list_xpath[x], first = True)
    print(image)
    while image is None:
        x += 1
        image = r.html.xpath(list_xpath[x], first = True)
        
    print(image)
    print(type(image))
    print('xx')
    #obtener solo el atributo src de elemento que da el xpath
    image_link = image.attrs['src']
    #print(image_link)
    print('----')
    
    product = {
        'brand': brand,
        'name': name,
        'price': price,
        'category': category,
        'image_link' : image_link
        
    }
    print(product)
    
    product_list.append(product)    
    
df = pd.DataFrame(product_list)
#'hiperber1.csv'
df.to_csv(name_file, encoding='utf-16')


