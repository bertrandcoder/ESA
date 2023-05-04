import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

#import_dir = r"D:/Dropbox/course/bazar/"
import_dir = "C:/Users/mpica/Dropbox/course/bazar/"
directory = os.fsencode(import_dir)

x = 1
#df_test = []
df_test = pd.DataFrame()
for file in os.listdir(directory):
    print(file)
    file = str(file).replace("b","").replace("\'","")
    #Attention içi a remettre le bon dossier 'import_dir' pour ouvrir le fichier
    doc_path = import_dir+str(file)
    df1 = pd.read_excel(doc_path)
    #print(df1)
    # Vous pouvez constater que la colonne 'Date' comprend 2 types différents
    print(type(df1.loc[0, 'Date']), type(df1.loc[1, 'Date']))
    # Pour conserver que les dates au format str, je vais conserver (df1.loc), dans la colonne Date (df1.Date), les lignes qui ont le format str (isinstance(x,str)). lambda permet de créer une fonction locale
    df2 = df1.loc[df1.Date.apply(lambda x: isinstance(x, str))]
    print(df2)
    
    #df1["Date"]=pd.to_datetime(df1["Date"])
    # # Alternativement, on peut conserver les lignes de df1 ou la colonne 'Date' à la format "datetime"
    df3 = df1.loc[df1.Date.apply(lambda x: isinstance(x, datetime))]
    print(df3)
    
    print(x)
    if x == 1:
        df_problem = df2
        df_correct = df3
    else :
        df_problem = pd.concat([df_problem, df2])
        df_correct = pd.concat([df_correct, df3])
    x +=1
    

#On supprime les Dates qui ne contiennent que " "
df_problem = df_problem[(df_problem.Date != " ")]   
df_problem["Date"]=pd.to_datetime(df_problem["Date"])

df_final = pd.concat([df_correct[['Date','Value']], df_problem[['Date','Value']]])
df_final = df_final.set_index('Date').sort_index()

plt.figure()
df_final.plot()
plt.legend(loc='best')

size = int(len(df_final.index)/2)
df_part1 = df_final[0:size+1]
df_part2 = df_final[size+1:]

fig, axes = plt.subplots(nrows=2, ncols=1)
df_part1.plot(ax=axes[0])
axes[0].set_title('Part 1')
df_part2.plot(ax=axes[1])
axes[1].set_title('Part 2')

# Alternative pour importer
# import glob, os
# for file in glob.glob(import_dir+"*.xlsx"):
	# print(file)

