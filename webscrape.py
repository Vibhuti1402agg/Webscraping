from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
import os

def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

    url = "https://jobs.puchd.ac.in/list-jobs.php"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, 'html.parser')
    Work = soup.find_all('td', {'class': ['tdheads','tdfaculty']})
    Departments = soup.find_all('td',{'class':['tdheads']})
    Deps=[]
    for dep in Departments:
        Deps.append(dep.text)
    info=[]
    for data in Work:
        info.append(data.text)
    all_info={}
    Now = ''
    for item in info:
        if item in Deps:
            Now = item
            if item not in all_info:
                all_info[item]=[]
        if item not in Deps:
            all_info[Now].append(item)
    count=1
    with open('webscrape.csv','a') as f:
        for depar in all_info:
            max = len(all_info[depar])
            i=max-1
            while i>=0:
                if "," in all_info[depar][i-3]:
                    all_info[depar][i-3] = all_info[depar][i-3].replace(",","/")
                line = str(count) + "," + depar + "," + all_info[depar][i-3] + "," + all_info[depar][i-2][5:] + "," + all_info[depar][i-1][11:] + "\n"
                f.write(line)
                count=count+1
                i=i-4

scrape()


