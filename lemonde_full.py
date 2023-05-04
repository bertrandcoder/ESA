import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import csv

import string
import datetime as dt
import datetime
import time
from time import time, sleep, strftime, gmtime
from dateutil import parser

# # # ETAPE 1 : récupération des résultats de la recherche
url = 'https://www.lemonde.fr/recherche/?search_keywords=croissance&start_at=19%2F12%2F1944&end_at=19%2F11%2F2021&search_sort=relevance_desc'
print(url)    
soup = BeautifulSoup(urllib.request.urlopen(url, timeout=10),'html.parser')

insert_list = []
print(soup.original_encoding)

url_list = []

for x in soup.findAll("a", {"class":"teaser__link"}):
    # possible içi de récupérer le résumé par ex.
    if x.has_attr('href'):
        url_list.append(x['href'])
print(url_list)


# # ETAPE 2 : RECUPERATION DU CONTENU DES ARTICLES
dates = []
articles = []
for element in url_list :
    url = element
    print(url)    
    soup = BeautifulSoup(urllib.request.urlopen(url, timeout=10),'html.parser')
    # print(soup)

    insert_list = []
    # print(soup.original_encoding)
    texts = []
    date = ""
    
    # # Récupération de la date
    for x in soup.findAll("span", {"class":"meta__date meta__date--header"}):
        date = x.get_text()
        print(date)
        dates.append(str(date))
    # Dans les articles issus de la recherche, il y a des articles de blog ou autres qui ne sont pas codés pareil en html au niveau de la date. 
    # La classe n'étant pas la même, il faut faire une boucle spécifique pour la récupérer dans ces cas précis.
    if not date :
        for y in soup.findAll("span", {"class":"meta__date"}):
            date = y.get_text()
            print(date)
            dates.append(str(date))
            
    # # Récupération du texte       
    for x in soup.findAll("p", {"class":"article__paragraph"}):
        text = x.get_text()
        texts.append(str(text))
    article = ' '.join(texts)
    print(article)
    articles.append(str(article))

# Fusion des liens, dates, résumés et textes dans une seule Dataframe pour export
articles_list = [url_list, dates,articles]
df = pd.DataFrame (articles_list).transpose()
df.columns = ['url', 'date','article']
print (df)
df.to_excel("output_lemonde.xlsx",sheet_name='economie') 

