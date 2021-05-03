from scraper import retrieveArticleLinks
from scraper import scrapeWeb
import pandas as pd

companyList = [
    {'id': 'citylink', 'link':'City-link%20Express', 'listLinks':[],'contents':''},
    {'id': 'poslaju','link':'Pos%20Laju', 'listLinks':[],'contents':''},
    {'id': 'gdex', 'link':'GDEX', 'listLinks':[],'contents':''},
    {'id': 'jnt', 'link':'J%20%26%20T%20express', 'listLinks':[],'contents':''},
    {'id': 'dhl', 'link':'DHL', 'listLinks':[],'contents':''},
]

companyList = retrieveArticleLinks(companyList)
for i in companyList:
    index = 0
    #pass article link by link
    while index < 3:
        i['contents'] += str(scrapeWeb(i['listLinks'][index]))
        index += 1

stopWords = scrapeWeb("https://www.ranks.nl/stopwords")
positiveWords = scrapeWeb("https://positivewordsresearch.com/list-of-positive-words/")
negativeWords = scrapeWeb("https://positivewordsresearch.com/list-of-negative-words/")

def writeFile(name,arr):
    file1 = open(name,"w")
    string = ''
    for i in arr:
        string += str(i)+" "
    file1.write(string)
    file1.close()

writeFile("negativeWords.txt",negativeWords)
writeFile("positiveWords.txt",positiveWords)
writeFile("stopWords.txt",stopWords)
df = pd.DataFrame(companyList) 
df.to_csv('contents.csv', index=False, encoding='utf-8')


