from bs4 import BeautifulSoup
import requests
import re
import os
from selenium import webdriver


def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

    url = "https://www.naukri.com/top-jobs-by-designations#desigtop600"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    path = r'C:\Users\HP\Desktop\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)

    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, 'html.parser')

    Work = soup.find('div', {'class': 'multiColumn colCount_four'})
    jobs = Work.find_all('a')
    job_list = []
    for j in jobs:
        j = j.get('href')
        job_list.append(j)

    for link in job_list:
        driver.get(link)
        data = driver.find_elements_by_tag_name('a')
        job_links =[]
        job_data=[]
        for b in data:
            l=b.get_attribute('href')
            job_links.append(l)

        for a in job_links:
            if a and 'job-listings' in a:
                driver.get(a)
                job = driver.find_elements_by_class_name('top')
                for j in job:
                    j=j.text
                    j = j.splitlines()
                    job_data.append(j)

        with open('naukriscrape.csv', 'a') as f:
            for line in job_data:
                n = len(line)
                city = line[n - 2].replace(",", "|")
                sal = line[n - 3].replace(",", "|")
                if sal != 'Not disclosed' :
                    sal = sal[1:]
                exp = line[n - 4].replace(",", "|")
                company = line[1].replace(",", "|")
                post = line[0].replace(",", "|")
                row = post + "," + company + "," + exp + "," + sal + "," + city + '\n'
                f.write(row)

scrape()


