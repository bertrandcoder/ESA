# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:00:42 2023

@author: LENOVO
"""

import pandas as pd
import ntpath
import os 
import matplotlib.pyplot as plt
import datetime 
from bs4 import BeautifulSoup
import requests







url= 'https://elpais.com/economia/2023-05-04/el-mercado-laboral-cerro-abril-con-un-record-de-206-millones-de-ocupados-tras-crear-240000-puestos-de-trabajo.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


title = soup.find('title').text
date= soup.find("time")["datetime"]

text_list=''

for text in soup.findAll("p" , {"class":""}):
    text_list+=text.text

df=pd.DataFrame({'titre':[title,''] ,
                 'date':[date,''] ,
                'text':[text_list,'']})

df.to_excel('article.xlsx',index=False)

# methode 1 de traduction (il faut au prealable installer le package)

from deep_translator import GoogleTranslator

title_eng =  GoogleTranslator(source='auto',target='english').translate(title)

text_list_eng =  GoogleTranslator(source='auto',target='english').translate(text_list)

# methode 2

from translate import Translator
translator= Translator(to_lang="english")

litle_eng2 = translator.translate(title)
text_list_eng2 = translator.translate(text_list)

# Le texte ne doit pas avoir plus de 500 caracteres
print(text_list)
