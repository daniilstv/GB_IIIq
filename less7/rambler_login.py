from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://mail.rambler.ru/")
assert "Рамблер/почта" in driver.title
iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)
elem = driver.find_element_by_id('login')
elem.send_keys('Login')