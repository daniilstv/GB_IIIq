from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from pymongo import MongoClient

'''
2) Написать программу, которая собирает «Хиты продаж» с сайтов техники mvideo, onlinetrade и складывает данные в БД. 
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

'''


client = MongoClient('mongodb://127.0.0.1:27017')
db = client['mvideo']
client.mvideo.docs.drop()
docs = db.docs
#
# def db_mvideo_writer(df):
#     data = pd.DataFrame()
#     client.mvideo.docs.drop()
#     mvideo_db = client['mvideo']
#     docs = mvideo_db.docs
#     result = docs.insert_many(df.to_dict(orient='records'))
#     return result.inserted_ids

def get_elems():
    block = driver.find_element_by_class_name('accessories-product-list')
    elems = block.find_elements_by_class_name('gallery-list-item')
    return elems

def collect_data(elems):
    for elem in elems:
        name = elem.find_element_by_class_name('sel-product-tile-title').text
        price = elem.find_element_by_class_name('c-pdp-price__current').text
        result = docs.insert_one({'name': name, 'price': price})
    return print(result)

# chrome_options = Options()
# chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('ChromeDriverManager().install()')


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.mvideo.ru/')

elems = get_elems()

collect_data(elems)

buttons = block.find_element_by_class_name('carousel-paging').find_elements_by_tag_name('a')[1:]
for button in buttons:
    button.click()
    time.sleep(2)
    elems = get_elems()
    collect_data(elems)

