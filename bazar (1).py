import pandas as pd
import os
from datetime import datetime, timedelta

import_dir = "D:/Dropbox/course/Univ. Orléans/Intro à Python/bazar/"
directory = os.fsencode(import_dir)

x = 1
for file in os.listdir(directory):
    file = str(file).replace("b","").replace("\'","")
    #Attention içi a remettre le bon dossier 'import_dir' pour ouvrir le fichier
    doc_path = import_dir+str(file)
    df1 = pd.read_excel(doc_path)
    # Vous pouvez constater que la colonne 'Date' comprend 2 types différents
    print(type(df1.loc[0, 'Date']), type(df1.loc[1, 'Date']))
    
    # Pour ne conserver que les dates, je vais conserver (df1.loc), dans la colonne Date (df1.Date), les lignes qui n'ont pas le format str (not isinstance(x,str)). lambda permet de créer une fonction locale
    df2 = df1.loc[df1.Date.apply(lambda x: not isinstance(x, str))]
    print(df2)
    
    # # Alternativement, on peut conserver les lignes de df1 ou la colonne 'Date' à la format "datetime"
    # df3 = df1.loc[df1.Date.apply(lambda x: isinstance(x, datetime))]
    # print(df3)
    
    print(x)
    if x == 1:
        df_final = df2
    else :
        df_final = df_final.append(df2)
    x +=1
df_final['count'] = 1
print(x)
print(df_final)
df_final_merged = df_final.groupby('Date', as_index=False).agg({'Value':'mean', 'count':'sum'})
print(df_final_merged)
df_final.to_excel(import_dir+'export.xlsx')


# Alternative pour importer
# import glob, os
# for file in glob.glob(import_dir+"*.xlsx"):
	# print(file)