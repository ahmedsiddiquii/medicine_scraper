from selenium import webdriver
from time import sleep
import threading
page=2

def process(i):
    link = i

    driver = webdriver.Chrome("chromedriver")
    driver.get("https://portal.ncpr.bg/registers/pages/register/list-medicament7.xhtml")
    driver.get("https://portal.ncpr.bg/registers/pages/register/list-medicament7.xhtml")
    pagination = driver.find_elements(by="xpath", value="//span[@class='rf-ds ']//a")
    for p in pagination:
        if p.text == str(page):
            p.click()
    sleep(5)
    table = driver.find_element(by="xpath", value="//tbody[@id='medicamentSearchForm:resultRegisterOneTable:tb']")
    trs = table.find_elements(by="tag name", value="tr")[link]
    cells=trs.find_elements(by="tag name",value="td")
    temp=[]
    for cell in cells:
        temp.append(cell.text)
    print(temp)

    a = trs.find_element(by="tag name", value="a")
    a.click()

    #moin code goes here
    input()

for i in range(0,2):
    s=threading.Thread(target=process,args=(i,))
    s.start()