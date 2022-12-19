from selenium import webdriver
from time import sleep
import threading
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

with open("output.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["National no","Registration number entered in the RU","Medicine","	PRU","ATC","INN","Relax mode","Status",
                     "Date of update","National identification number", "Identifier", "Authorizarion number", "Parallel import decision number",
         "Date of decision on parallel importation", "International nonproprietary name /INN/",
         "Anatomical Therapeutic Chemical Classification /ATC-код/", "Authorization Holder",
         "Producer", "Pharmaceutical Form", "Quantity of active ingredient", "Final Packinging", "Medicament Type",
         "Release Mode", "Status", "Status IAL"])

browsers = []


def initiate_browsers():
    global browsers
    prefs = {
        "translate_whitelists": {"bg": "en"},
        "translate": {"enabled": "true"}
    }
    options = Options()
    options.add_argument("--lang={}".format("en"))
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome("chromedriver", chrome_options=options)
    driver.get("https://portal.ncpr.bg/registers/pages/register/list-medicament7.xhtml")
    browsers.append(driver)


def process(i, page, driver):
    lst = []
    link = i
    driver.get("https://portal.ncpr.bg/registers/pages/register/list-medicament7.xhtml")
    sleep(4)
    pagination = driver.find_elements(by="xpath", value="//span[@class='rf-ds ']//a")
    for p in pagination:
        if p.text == str(page):
            p.click()
    sleep(5)
    table = driver.find_element(by="xpath", value="//tbody[@id='medicamentSearchForm:resultRegisterOneTable:tb']")
    trs = table.find_elements(by="tag name", value="tr")[link]
    cells = trs.find_elements(by="tag name", value="td")
    temp = []
    for cell in cells:
        temp.append(cell.text)

    a = trs.find_element(by="tag name", value="a")
    a.click()

    sleep(5)
    # moin code goes here
    National_identification_number = driver.find_element(By.XPATH, '//span[@id="medicamentView:trackingId"]').text
    identifier = driver.find_element(By.XPATH, "//span[@id='medicamentView:identifier']").text
    authorization_number = driver.find_element(By.XPATH, "//span[@id='medicamentView:authorizationNumber']").text
    parallel_import_decison = driver.find_element(By.XPATH,
                                                  "//span[@id='medicamentView:authorizationNumberParallelImport']").text
    date_of_decision = driver.find_element(By.XPATH,
                                           "//span[@id='medicamentView:authorizationNumberParallelImport']").text
    international_nonproprietary = driver.find_element(By.XPATH, "//span[@id='medicamentView:innName']").text
    try:
        anatomical_therapeutic = driver.find_element(By.XPATH, "//span[@id='medicamentView:atcCode']").text
    except:
        anatomical_therapeutic = ''
    authorization_holder = driver.find_element(By.XPATH, "//span[@id='medicamentView:authorizationHolder']").text
    producer = driver.find_element(By.XPATH, "//span[@id='medicamentView:producer']").text
    pharmaceutical_form = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:medicamentForm')]").text
    quantity_of_active = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:quantity')]").text
    final_packing = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:finalPack')]").text
    # medicine type
    x = driver.find_element(By.XPATH, ("(//span[contains(@id,'medicamentView:medicamentType')])[1]")).text
    y = driver.find_element(By.XPATH, ("(//span[contains(@id,'medicamentView:medicamentType')])[2]")).text
    medicament_type = x + y

    release_mode = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:releaseMode')]").text
    status = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:status')]").text
    status_ial = driver.find_element(By.XPATH, "//span[contains(@id,'medicamentView:statusIAL')]").text

    with open("output.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        #temp will add here
        temp.extend([National_identification_number, identifier, authorization_number, parallel_import_decison,
                         date_of_decision, international_nonproprietary, anatomical_therapeutic, authorization_holder,
                         producer, pharmaceutical_form, quantity_of_active, final_packing, medicament_type,
                         release_mode, status, status_ial])
        writer.writerow(temp
                        )


threads = []
for i in range(0, 1):
    s = threading.Thread(target=initiate_browsers)
    s.start()
    threads.append(s)
for t in threads:
    t.join()

for page in range(0, 1):
    all_threads = []
    for i in range(0, 1):
        s = threading.Thread(target=process, args=(i, page, browsers[i]))
        s.start()
        all_threads.append(s)
    for ss in all_threads:
        ss.join()
