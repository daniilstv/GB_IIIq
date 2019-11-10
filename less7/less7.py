from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

'''
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и 
сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

'''

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://passport.yandex.ru/auth/welcome?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru")
assert "Авторизация" in driver.title

'''
Очень долго пытался сделать авторизацию в рамблер-почте, но так и не смог. Полагаю, что там испольуется iframe. 
Как обратиться к элементу внутри я не понял, хотя в коде страницы было явно  видно id='login'.
Ниже мои попытки сфокусироваться на вводе логина.

# frames = driver.find_elements_by_tag_name('iframe')
# print(len(frames))
# for frame in frames:
#     print(frame.size, frame.location, frame.get_attribute('name'))

#driver.switchTo().frame(driver.findElement(By.name("iFrameTitle")));

#driver.switchTo().frame(driver.findElement(By.name("ym-native-frame")))
#driver = driver.find_elements_by_tag_name('ym-native-frame')
#time.sleep(10)

#elem = driver.find_element_by_id('login')

#elem = driver.find_element_by_class_name("rui-FormGroup-medium rui-FormGroup-normal rui-FormGroup-root c0233 c0232")
#elem = driver.findElement(By.cssSelector("_2qpX"))
#elem = driver.find_element_by_xpath('rui-Input-input -metrika-nokeys rui-Input-filled')
#self.quick_wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "login")))

'''


elem = driver.find_element_by_id('passp-field-login')
elem.send_keys("daniilstv")
elem.send_keys(Keys.RETURN)
time.sleep(3)
psw = input("Введите пароль...")
#psw = '***'


elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys(psw)
elem.send_keys(Keys.RETURN)
time.sleep(5)


mail_list = driver.find_elements_by_class_name('mail-MessageSnippet')

# Собираем ссылки на письма
links = []
for link in mail_list:
    links.append(link.get_attribute('href'))

# Пишем в датафрэйм
data = pd.DataFrame()

for link in links[0:5]:
    driver.get(link)
    time.sleep(3)

    subj = driver.find_element_by_class_name('mail-Message-Toolbar-Subject_message').text
    sender = driver.find_element_by_class_name('mail-Message-Sender-Email').text
    time_ = driver.find_element_by_class_name('ns-view-message-head-date').text
    text = driver.find_element_by_class_name('mail-Message-Body-Content').text

    data = data.append({'sender': [sender], 'subj': [subj], 'time_': [time_],
                        'text': [text]}, ignore_index=True)



print(data)

assert "No results found." not in driver.page_source
driver.close()
