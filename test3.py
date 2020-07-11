from bs4 import BeautifulSoup
import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    path = r'C:\Users\HP\Desktop\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)

    linlist=[]
    career = []
    career_not_found = []
    job_page = []
    count = 0

    with open('data.txt','r') as f:
        for lines in f.readlines():
            linlist.append(lines)

    for link in linlist[:12]:
            count = 0
            driver.get(link)
            content1 = driver.find_elements_by_tag_name('a')
            for tags in content1:
                try:
                    if 'Careers' in tags.text:
                        lin = tags.get_attribute('href')
                        print(lin)
                        career.append(lin)
                        count += 1
                        break
                except Exception:
                    pass
            if count == 0:
                career_not_found.append(link)

    for link2 in career_not_found:
        driver.get(link2)
        content2 = driver.find_elements_by_tag_name('span')
        for tags2 in content2:
            try:
                if 'Careers' in tags2.text:
                    tags2.click()
                    job = driver.find_elements_by_tag_name('a')
                    for j in job:
                        if 'jobs' in j.text.lower():
                            lin2 = j.get_attribute('href')
                            job_page.append(lin2)
                            break
                        elif 'india' in j.text.lower():
                            lin2 = j.get_attribute('href')
                            job_page.append(lin2)
                            break
                        elif 'openings' in j.text.lower():
                            lin2 = j.get_attribute('href')
                            job_page.append(lin2)
                            break
            except Exception:
                pass

    button_not_found = []
    for link3 in career:
        count1 = 0
        driver.get(link3)
        content3 = driver.find_elements_by_tag_name('button')
        for tags3 in content3:
            try:
                if 'jobs' in tags3.text.lower():
                    print(tags3.text.lower())
                    tags3.click()
                    count1 += 1
                    break
                elif 'job' in tags3.text.lower():
                    print(tags3.text.lower())
                    tags3.click()
                    count1 += 1
                    break
            except Exception:
                pass
        if count1 == 0:
            button_not_found.append(link3)

    for link4 in button_not_found:
        driver.get(link4)
        content4 = driver.find_elements_by_tag_name('a')
        for tags4 in content4:
            try:
                if 'credit' not in tags4.text.lower():
                    if 'apply' in tags4.text.lower():
                        print(tags4.text)
                        lin3 = tags4.get_attribute('href')
                        job_page.append(lin3)
                        break
                    elif 'jobs' in tags4.text.lower():
                        print(tags4.text)
                        lin3 = tags4.get_attribute('href')
                        job_page.append(lin3)
                        break
                    elif 'experienced' in tags4.text.lower():
                        print(tags4.text)
                        lin3 = tags4.get_attribute('href')
                        job_page.append(lin3)
                        break
                    elif 'openings' in tags4.text.lower():
                        print(tags4.text)
                        lin3 = tags4.get_attribute('href')
                        job_page.append(lin3)
                        break
            except Exception:
                pass


scrape()
