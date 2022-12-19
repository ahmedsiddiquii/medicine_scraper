from selenium import webdriver
from time import sleep
import threading
import csv
from selenium.webdriver.chrome.options import Options
with open("output.csv","w",encoding="utf-8") as file:
    writer=csv.writer(file)
    writer.writerow(["National no","Registration number entered in the RU","Medicine","	PRU","ATC","INN","Relax mode","Status",
                     "Date of update"])


def process(i,page):
    link = i

    options = Options()
    options.add_argument("--lang={}".format("en"))

    driver = webdriver.Chrome("chromedriver",chrome_options=options)
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

    with open("output.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(temp)
    # input()
for page in range(0,5000):
    all_threads=[]
    for i in range(0,4):
        s=threading.Thread(target=process,args=(i,page,))
        s.start()
        all_threads.append(s)
    for ss in all_threads:
        ss.join()