import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
plt.style.use('ggplot')

color =  sns.color_palette()
sns.set(rc={'figure.figsize':(25, 15)})

import plotly
#connected = True mean it will download the latest version
#of plotly javascript library.

plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go 

import plotly.figure_factory as ff
import cufflinks as cf

import warnings
warnings.filterwarnings('ignore')

#-----------------------------------------------------------------
df = pd.read_csv("C:\\Users\\user\\Desktop\\DataScience\\googleplaystore\\googleplaystore.csv")

df.drop_duplicates(subset='App', inplace=True)#drop the repeat App 
df = df[df['Android Ver'] != np.nan]
df = df[df['Android Ver'] != 'NaN']
df = df[df['Installs'] != 'Free']
df = df[df['Installs'] != 'Pain']

print("Number of apps in the datasets", len(df))

#----------------------------------------------------------------
"""convert all app size to MB"""
"""Remove the '+' from Number of  Installs to make  it numeric"""
"""Convert all review text to English language using Google Translator library"""

# - Installs : Remove + and ,
df["Installs"] = df['Installs'].apply(lambda x: x.replace(
'+', '')if '+' in str(x) else x)

df['Installs'] = df['Installs'].apply(lambda x: x.replace(
',', '')if ',' in str(x) else x)

df['Installs'] = df['Installs'].apply(lambda x: int(x))
print(df['Installs'])

# - Size : MB
df['Size'] = df['Size'].apply(lambda x : x.replace(
'Varies with device', 'NaN') if 'Varies with device' in str(x) else x)

df['Size'] = df['Size'].apply(lambda x: x.replace(
'M', '') if 'M' in str(x) else x)

df['Size'] = df['Size'].apply(lambda x: x.replace(
',','') if ',' in str(x) else x)

df['Size'] = df['Size'].apply(lambda x: float(str(x).replace(
'k',''))/1000 if 'k' in str(x) else x)

df['Size'] = df['Size'].apply(lambda x:float(x))

# - Price:$
df['Price'] = df['Price'].apply(lambda x:x.replace(
"$", '') if '$' in str(x) else x)

df['Price'] = df['Price'].apply(lambda x: float(x))

#- Review:
df['Reviews'] = df['Reviews'].apply(lambda x: int(x))

#Basuc EDA
x = df["Rating"].dropna()
y = df['Size'].dropna()
z = df['Installs'][df.Installs!=0].dropna()
p = df['Reviews'][df.Reviews!=0].dropna()
t = df['Type'].dropna()
price = df['Price']

p = sns.pairplot(pd.DataFrame(list(zip(x, y, np.log(z), np.log10(p), t, price)),
                            columns=['Rating', 'Size', 'Installs', 'Review', 'Type', 'Price']), hue = 'Type', palette='Set2')

plt.show()

#Android market breakdown
#Which category has the highest share of (active) apps in the market?
number_of_apps_in_category = df['Category'].value_counts().sort_values(ascending=True)

data = [go.Pie(
            labels = number_of_apps_in_category.index,
            values=number_of_apps_in_category.values,
            hoverinfo = 'label+value'
)]

plotly.offline.iplot(data, filename='active_category')
plt.show()