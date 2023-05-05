import pandas as pd
import glob 



                         


path = r"C:\Users\c102-21\Desktop\code\Data16"

# reading all the excel files
tab = pd.DataFrame()
for file in glob.glob("**/*.xlsx", recursive=True):
    # combining multiple excel worksheets 
    # into single data frames
    df = pd.concat(pd.read_excel(file, sheet_name=None),ignore_index=True, sort=False)
      
    
    tab = tab.append(df, ignore_index=True)



tab.drop(columns = tab.columns[0], axis = 1, inplace= True)

#On supprime la premiere colonne

newdata = pd.DataFrame()


tab['Date'] =  pd.to_datetime(tab['Date'], infer_datetime_format=True)
tab.dtypes

#Je met tout en datetime






import re 
for col in tab['Value']:
    tab['Value'] = pd.to_numeric(tab['Value'].apply(lambda x: re.sub(',', '.', str(x))))
    

newdata=tab.groupby('Date', as_index=False)['Value'].prod()

count = pd.DataFrame()

count=tab['Date'].value_counts()

#je n'arrive pas a diviser






df = pd.read_excel (r"C:\Users\c102-21\Desktop\code\taux_allemand.xlsx")

df2 = df.dropna()






































































test = pd.DataFrame()

# to iterate excel file one by one 
# inside the folder
for file in filenames:
    # combining multiple excel worksheets 
    # into single data frames
    df = pd.concat(pd.read_excel(file, sheet_name=None),ignore_index=True, sort=False)
      
    # Appending excel files one by one
    test = test.append(df, ignore_index=True)

#print(test)

#test=test[test["Date"] !=" "] #supprime toutes les lignes où on a rien dans date
#print(test)

test = test[test['Date'].apply(lambda x: isinstance(x, datetime))] #nécessite l'import du package datetime
#df = df[-df['Date'].apply(lambda x: isinstance(x, str))] #ne nécessite pas l'import de datetime
test.dtypes

test.pop("Unnamed: 0") #supprime cette colonne
test.dtypes

#drop si jai pas de date


test['Date'] =  pd.to_datetime(test['Date'], infer_datetime_format=True)
test.dtypes

#test=test.sort_values(by=['Date']) #pour voir plus facilement les doubles

#freq=test['Date'].value_counts()

test['freq'] = test.groupby('Date')["Date"].transform('count') #entre parenthese fais le count dessus

yo=test.groupby('Date', as_index=False)['Value'].mean() #as index false ca creer un data frame je crois date pas index
#ou groupy('date', as_index=False).agg({"Value":"mean", "count":"sum"})
toto = test.merge(yo, on='Date') 

toto.columns
toto=toto.rename(columns={"Value_y": "moyenne"})

print(toto)

toto = toto.groupby('Date').first()
print(toto)
toto.pop("Value_x")

# lambda fonction appeller localement ??? 
#df1.date = df1["date"]
