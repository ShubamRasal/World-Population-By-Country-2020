# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 20:37:44 2022

@author: Shubham
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#Load and clean data:
#---------------------
df = pd.read_csv("D:\Practice Data Sets\world-population-by-country-2020\world-population-by-country-2020.csv",header=0,encoding='unicode_escape')

#Clean:
#------

df['Net Change'] = pd.to_numeric(df['Net Change'],errors='coerce')

#Convert string % to float:
#---------------------------

print(df)
print(df.info())

df['Urban Pop %'] = df['Urban Pop %'].str.rstrip("%")
df['Urban Pop %'] = pd.to_numeric(df['Urban Pop %'],errors='coerce')
df['Urban Pop %'] = df['Urban Pop %'].astype(float)/100

#Get top 2- largest populations:
#--------------------------------
subset = df[:20].sort_values('Population 2020')

#Calculate # for urban and rural pop.
#-------------------------------------
subset['urban'] = subset['Population 2020'] * subset['Urban Pop %']
subset['rural'] = subset['Population 2020'] - subset['urban']
subset['urban'] = subset['urban'].round()
subset['rural'] = subset['rural'].round()

#plot:
#------

fig, ax = plt.subplots(1, figsize=(10,10))
ax.barh(subset['Country (or dependency)'], subset['rural'],color='#62A87C')
ax.barh(subset['Country (or dependency)'], subset['urban'],left=subset['rural'],color='#313B72')

#label bars with values:
#-------------------------

for idx, val in subset.iterrows():
    val = val['Population 2020']
    if (val > 10**9):
        plt.text(val+10**6, 10-idx, '{:,.2f}mi'.format(val/10**6,va='center'))
    else:
        plt.text(val+10**6, 19-idx, '{:,.2f}mi'.format(val/10**6),va='center')
        
#remove spines:
#---------------
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.xticks([])
plt.ylim(-1,20)

#legend, title:
#----------------

plt.legend(['Rural Pop.','Urban pop'],ncol=2,loc='upper left', frameon=False, bbox_to_anchor=(.55,.9115),
           bbox_transform=fig.transFigure)
plt.title("World's 20 largest countries by total populations",loc='left')

plt.show()

#Top 20 Countries by Net Change (Positive and Negative)
#--------------------------------------------------------

#get top 20 countries by Net Positive Change:
#---------------------------------------------

subset_pos = df.sort_values('Net Change',ascending=False)[:20].sort_values('Net Change')

#get top 20 countries by Net Negative Change:
#---------------------------------------------

subset_neg = df.sort_values('Net Change')[:20]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

ax1.barh(subset_pos['Country (or dependency)'],subset_pos['Net Change'],color='#62A87C')
ax1.set_title('Top 20 Countries - Positive net change in population', loc='center',fontsize=13)

ax2.barh(subset_neg['Country (or dependency)'],subset_neg['Net Change'],color='#313B72')
ax2.set_title('Top 20 Countries - Negative net change in population',loc='center',fontsize=13)
ax2.yaxis.tick_right()

for ax in (ax1, ax2):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])

for i, val in enumerate(subset_pos['Net Change']):
    ax1.text(val+10**5, i, '+{:,.2f}mi' .format(val/10**6),
             va='center',fontsize=11)

for i, val in enumerate(subset_neg['Net Change']):
    ax2.text(val-15**3, i, '{:,.2f}k' .format(val/10**3),
             va='center',fontsize=11, ha='right')

#Real Map Visualization:
#-------------------------

#Import graphical modules:
#---------------------------

import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)

#Map using Plotly:
#-----------------
"""
valores = df['Migrants (net)'] #In this line you can select any numerical column

data = dict(type = 'choropleth',
            locations = df['Country (or dependency)'],
            locationmode = "country names",
            colorscale = 'Cividis',
            z = valores,
            reversescale = True,
            text = df['Country (or dependency)'],
            colorbar = {'title' : valores.name}
            )
layout = dict(title = valores.name,
              geo = dict(showframe = False,
                         projection = {'type': 'hyperelliptical'}))
choromap = go.Figure(data=[data],layout=layout)
iplot(choromap,validate=False)
"""
#-------------------------------------------------------------------------------

# Fertility Rates:
#-------------------

fertility = df.head(20)['Fert. Rate'].sort_values(ascending= True).astype(float)
fertility

#Populatioon Density:
#----------------------
df.columns
pop_density = df.head(20)['Density  (P/Kmý)'].replace(',','',regex=True).sort_values(ascending=True).astype(int).astype(str)
pop_density

sns.set_theme(style="darkgrid")
f, ax = plt.subplots(figsize=(8,6.5))
sns.despine(f, left=True, bottom=True)
sns.scatterplot(x='Fert. Rate', y='Density  (P/Kmý)',data=df.head(20).replace(',','',regex=True).sort_values(by=['Density  (P/Kmý)','Fert. Rate'], ascending=True),
                palette="ch:r=-.2,d=.3_r",
                sizes=(1, 8), linewidth=0,
                ax=ax)

# There is no correlation between fertility rate and population density:
#------------------------------------------------------------------------










