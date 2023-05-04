# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:15:07 2023

@author: mpica
"""
import pandas as pd
import time
import statsmodels.api as sm
import stargazer
from stargazer.stargazer import Stargazer

import os
os.chdir("D:/Dropbox/course/Univ. Orléans/M1 - Intro à Python/database")
# df_btc = pd.read_csv(r"C:\Users\mpica\Downloads\bitstampUSD_1-min_data_2017-01-01_to_2021-03-31.csv")
# df_twitter = pd.read_excel(r"C:\Users\mpica\Downloads\BTC.xlsx")

df_btc = pd.read_csv(r"D:\Dropbox\course\Univ. Orléans\M1 - Intro à Python\database\bitstampUSD_1-min_data_2017-01-01_to_2021-03-31_new.csv")
df_twitter = pd.read_excel(r"D:\Dropbox\course\Univ. Orléans\M1 - Intro à Python\database\BTC.xlsx")

# Conversion des dates en format datetime
print(df_twitter["date"].dtypes)
df_twitter["date"] = pd.to_datetime(df_twitter["date"])
print(df_twitter["date"].dtypes)

print(df_btc["Timestamp"].dtypes)
df_btc["Timestamp"] = pd.to_datetime(df_btc["Timestamp"],unit="s")
print(df_btc["Timestamp"].dtypes)

# tweets_short = df_twitter[:6000]
# btc_short = df_btc[:10000]

tweets_short = df_twitter
btc_short = df_btc

# Changement de fréquence : Méthode 1, via l'object period[X]
tic = time.perf_counter()
periods = ['D','H']
for period in periods :
    tweets_short['temp_date']=tweets_short['date'].dt.to_period(period)
    print(tweets_short["temp_date"].dtypes)
    btc_short['temp_date']=btc_short['Timestamp'].dt.to_period(period)
    print(btc_short["temp_date"].dtypes)
    if period == 'D':
        tweets_daily = tweets_short['sentiment'].groupby(by=tweets_short["temp_date"]).agg(['mean','count'])
        btc_daily = btc_short.groupby(by=btc_short["temp_date"]).agg({'Close':'last', "Volume_(Currency)":"sum"})
        # Fusion des deux df en une seule (pas obligatoire)
        # df_daily = pd.merge(tweets_daily, btc_daily, on=["temp_date","temp_date"])
    else:
        tweets_hourly = tweets_short['sentiment'].groupby(by=tweets_short["temp_date"]).agg(['mean','count'])
        btc_hourly = btc_short.groupby(by=btc_short["temp_date"]).agg({'Close':'last', "Volume_(Currency)":"sum"})
        # Fusion des deux df en une seule (pas obligatoire)
        # df_hourly = pd.merge(tweets_hourly, btc_hourly, on=["temp_date","temp_date"])
toc = time.perf_counter()
print(f"Done in {toc - tic:0.4f} seconds")

# Changement de fréquence : Méthode 2, via resample
tic = time.perf_counter()
periods = ['D','H']
for period in periods :
    if period == 'D':
        tweets_daily=tweets_short.resample(period, on='date').agg({"sentiment": ["mean", "count"]})
        tweets_daily.columns = tweets_daily.columns.droplevel()
        btc_daily=btc_short.resample(period, on='Timestamp').agg({'Close':'last', "Volume_(Currency)":"sum"})
        # Fusion des deux df en une seule (pas obligatoire)
        df_daily = pd.merge(tweets_daily, btc_daily, left_index=True, right_index=True)
    else:
        tweets_hourly=tweets_short.resample(period, on='date').agg({"sentiment": ["mean", "count"]})
        tweets_hourly.columns = tweets_hourly.columns.droplevel()
        btc_hourly=btc_short.resample(period, on='Timestamp').agg({'Close':'last', "Volume_(Currency)":"sum"})    
        # Fusion des deux df en une seule (pas obligatoire)
        df_hourly = pd.merge(tweets_hourly, btc_hourly, left_index=True, right_index=True)
toc = time.perf_counter()
print(f"Done in {toc - tic:0.4f} seconds")


df_hourly["L_vol"] = df_hourly['count'].shift(1)
df_hourly["L_sentiment"] = df_hourly['mean'].shift(1)
df_daily["L_vol"] = df_daily['count'].shift(1)
df_daily["L_sentiment"] = df_daily['mean'].shift(1)

df_daily = df_daily.dropna(subset=["Close"])
df_daily['L_vol'] = df_daily['L_vol'].fillna(0)
df_daily['L_sentiment'] = df_daily['L_sentiment'].fillna(0)

df_hourly = df_hourly.dropna(subset=["Close"])
df_hourly['L_vol'] = df_hourly['L_vol'].fillna(0)
df_hourly['L_sentiment'] = df_hourly['L_sentiment'].fillna(0)

model = sm.OLS(df_daily["Close"], df_daily["L_vol"], intercept=False)
results1 = model.fit(cov_type='HC1')    
model = sm.OLS(df_hourly["Close"], df_hourly["L_vol"], intercept=False)
results2 = model.fit(cov_type='HC1')   

stargazer = Stargazer([results1,results2])

xxx = stargazer.render_html()
print(xxx)
file = open("../results.html","w")
file.write(xxx)
file.close()