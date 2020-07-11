from bs4 import BeautifulSoup
import requests
import re
import os
from selenium import webdriver


def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

    url = "https://www.ambitionbox.com/list-of-companies?utm_source=naukri&utm_medium=gnb"
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, 'html.parser')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    path = r'C:\Users\HP\Desktop\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    driver.get(url)

    Total = soup.find('p', {'class': 'sbold-section-header subtitle'})
    li = str(Total)
    li = li.split(' ')
    for i in li:
        if ',' in i:
            num = i

    num = num.replace(',','')
    pages = int(num)//30
    count1 = 1
    links = []
    while count1<pages-10:
        url1 = "https://www.ambitionbox.com/list-of-companies?page=" + str(count1)
        driver.get(url1)
        Company_links = driver.find_elements_by_class_name("ab-company-result-card")
        count = 0
        for el in Company_links:
            meta = el.find_elements_by_tag_name('meta')
            for i in meta:
                data = i.get_attribute('content')
                if 'https' in data:
                    if count % 2 == 0:
                        links.append(data)
                    count = count + 1
        count1 = count1 +1

    Company_list = []
    Company_website=[]
    for l in links:
        link = 'Not found'
        driver.get(l)
        content2 = session.get(l, verify=False).content
        soup2 = BeautifulSoup(content2, 'html.parser')
        Name = soup2.find('h1', {'class': 'company-name bold-display'})
        Company_name = Name.text
        Company_name = Company_name.strip()
        Company_name = Company_name.replace(',','|')
        Content_click = driver.find_elements_by_class_name('ctas-a-medium')[2].click()
        try:
            Website = driver.find_elements_by_class_name('website')
            for el in Website:
                link = el.get_attribute('href')
        except:
            Company_website.append(link)
        with open('companies.csv','a',encoding = 'utf8') as f:
            line = Company_name + "," + link + "\n"
            f.write(line)

scrape()


