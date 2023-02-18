#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
from math import exp
import random


# Charger l'ensemble des données d'entraînement
np.random.seed(2023)

y = np.random.binomial(n = 1, p = 0.7, size = 30)
x = np.random.normal(0,1,30)
c = np.ones(30)

df= np.array([c,x,y]).T

print(df) # affichage de l'échantillon


# In[13]:



# regression logistique: p(yi=1)= exp(cons + b*xi)/(1+)

# Initialisation
theta = np.array([0.5,0.5]) # paramètres initiaux


learning_rate = 0.1 # Définir le taux d'apprentissage


epoch = 20 # Définir le nombre maximal d'époque




# In[14]:



# Boucle d'entraînement
for j in range(epoch):
    np.random.shuffle(df) 
    
    for i in range(30):
        
        p=exp(df[i][0:2].dot(theta.T))/(1+exp(df[i][0:2].dot(theta.T)))
        
        d1 = (df[i][2]-p)*df[i][0]
        d2 = (df[i][2]-p)*df[i][1]
        
        theta[0] = theta[0] + learning_rate * d1
        theta[1] = theta[1] + learning_rate * d2

        
print(f"constante = {theta[0]}, beta = {theta[1]}")


# In[ ]:




