#!/usr/bin/env python
# coding: utf-8

# In[92]:


import geopandas as gpd
import os
import pandas as pd
import json
import fiona
import os




shapefile = r'ne_110m_admin_0_countries.shp'
#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
mapping = {
    'USA': 'US',
    'GBR': 'GB',
    'FRA': 'FR',
    'DEU': 'DE',
    'CHN': 'CN',
    # add more mappings as needed
}
gdf['country_code'] = gdf['country_code'].replace(mapping)

gdf.plot()

#Read csv file using pandas

df_all = pd.DataFrame()
df_all2 = pd.DataFrame() 
# set directory path
directory = r"C:\Studiejaar 3\Semester 2\Data science\assignment1 data"

# loop over each CSV file in the directory, read and extract the chosen columns, and append the data to df_all
for filename in os.listdir(directory):
    if filename.startswith("sale"):
        file_path = os.path.join(directory, filename)
        # Try to read the CSV file and extract the desired columns
        df = pd.read_csv(file_path)    
        df_all = df_all.append(df, ignore_index=True)
       
df_all['Transaction Date'] = pd.to_datetime(df_all['Transaction Date']) 
columns_to_keep = ['Transaction Date', 'Buyer Country']
df_all=df_all[columns_to_keep]        

# loop over each CSV file in the directory, read and extract the chosen columns, and append the data to df_all
for filename in os.listdir(directory):
    if filename.endswith(".csv") and filename.startswith("stats"):
        file_path = os.path.join(directory, filename)
        # Try to read the CSV file and extract the desired columns
        df = pd.read_csv(file_path, encoding = 'utf-16')    
        df_all2 = df_all2.append(df, ignore_index=True)

df_all2 = df_all2.sort_values(by= "Date")
df_all2['Date'] = pd.to_datetime(df_all2['Date']) 
columns_to_keep2 = ['Date', 'Daily Average Rating']
df_all2=df_all2[columns_to_keep2]
df_all2.fillna(0, inplace=True)

merged_df = pd.merge(df_all, df_all2, left_on='Transaction Date', right_on='Date')
merged_df.drop(['Transaction Date'], axis=1, inplace=True)
merged_df = merged_df.drop_duplicates()
merged_df['Date'] = merged_df['Date'].dt.strftime('%Y-%m-%d')
merged_df = merged_df.loc[merged_df['Daily Average Rating'] != 0]
merged_df.to_csv(r"C:\Studiejaar 3\Semester 2\Data science\assignment1 data\test2.csv", index=False)

# merge dataframes gdf and merged_df
merged = gdf.merge(merged_df, left_on = 'country_code', right_on = 'Buyer Country')
#print(merged.head())
#Read data to json.

merged_json = json.loads(merged.to_json())
#Convert to String like object.
json_data = json.dumps(merged_json)

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 50)
#Define custom tick labels for color bar.
tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p = figure(title = 'Share of adults who are obese, 2016', height = 600 , width = 950, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'per_cent_obesity', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify figure layout.
p.add_layout(color_bar, 'below')

#Display figure inline in Jupyter Notebook.
output_notebook()
output_file("geo.html")
#Display figure.
show(p)


# In[ ]:





# In[ ]:




