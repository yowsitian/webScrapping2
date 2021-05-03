import re
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from urllib.request import urlopen
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

urlList = [ 
    {'id': 'theStar', 'link': 'https://www.thestar.com.my/search/?q='},
    {'id': 'borneoPost','link': 'https://www.theborneopost.com/search_gcse/?q='},
    {'id': 'newStraitsTimes', 'link': 'https://www.nst.com.my/search?keywords='},
]

#to verify the webpage is exist
def checkValidity(url):
    r = requests.get(url, verify = False)
    if r.status_code == 200:
        return r
    return False

def retrieveArticleLinks(inputList):
    print("Retrieving links...")
    for i in inputList:
        index = 0
        while len(i['listLinks'])  < 3 and index != len(urlList):
            url = urlList[index]['link'] + i['link']
            r = checkValidity(url)
            if r:
                driver.get(url)
                contentNews = []
                if urlList[index]['id'] == 'theStar':
                    contentNews = driver.find_elements_by_xpath("//h2[@class='f18']/a")
                elif urlList[index]['id'] == 'borneoPost':
                    contentNews = driver.find_elements_by_xpath("//div[@class='gs-title']/a")
                else:
                    contentNews = driver.find_elements_by_xpath("//div[@class='article-teaser']/a")
                for n in np.arange(0,len(contentNews)):
                    if n == 3:
                       break
                    i['listLinks'].append(contentNews[n].get_attribute("href"))
                index += 1
    print("Retrieval succeeded.")
    return inputList
    
def scrapeWeb(url):
    print("Scraping...")
    r = checkValidity(url)
    result = ''
    resultArr = []
    if r:
        driver.get(url)
        body = []
        stopWords = False
        wordClassifier = False

        if "www.thestar.com" in url:
            body = driver.find_elements_by_xpath("//div[@id='story-body']/p")
        elif "www.theborneopost.com" in url:
            body = driver.find_elements_by_xpath("//div[@class='post-content description ']/p")
        elif "www.nst.com" in url:
            body = driver.find_elements_by_xpath("//div[@class='field field-body']/p")
        elif "stopwords" in url:
            stopWords = True
            article = BeautifulSoup(r.content, "html.parser")
            body = article.find_all('td')
        elif "positivewordsresearch.com" in url:
            wordClassifier = True
            article = BeautifulSoup(r.content, "html.parser")
            body = article.find('div',attrs={"class": "entry-content"})   
            body = body.findAll('p')
        
        arrOutput = stopWords or wordClassifier

        if arrOutput:
            clean = re.compile('<.*?>')
            for n in np.arange(0,len(body)):
                body[n] = re.sub(clean, ' ',str(body[n]))

        if len(body) != 0:
            for n in np.arange(0,len(body)):
                if arrOutput:
                    body[n] = body[n].replace(",","")
                    tempArr = body[n].split()
                    for i in tempArr:
                        resultArr.append(i) 
                else:
                    result += str(body[n].get_attribute('textContent')) 

    print("Done scraping.")   

    if arrOutput:
        return resultArr
    return result