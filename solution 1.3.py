#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import math
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, curdoc
from bokeh.models import ColumnDataSource, RangeTool, Range1d, RadioButtonGroup, CDSView, GroupFilter, Select, CustomJS, Div, Dropdown
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import RadioButtonGroup

# create empty dataframe 
df_all = pd.DataFrame()

# set directory path
directory = r"C:\Users\Toly\Desktop\assignment1 data"

# loop over each CSV file in the directory, read and extract the chosen columns, and append the data to df_all
for filename in os.listdir(directory):
    if filename.endswith(".csv") and filename.startswith("stats"):
        file_path = os.path.join(directory, filename)
        # Try to read the CSV file and extract the desired columns
        df = pd.read_csv(file_path, encoding = 'utf-16')    
        df_all = df_all.append(df, ignore_index=True)
  
# sort the data by the Date column
df_all = df_all.sort_values(by= "Date")
df_all['Date'] = pd.to_datetime(df_all['Date'])
#print(df_all.columns)

# add zero to NaN
df_all.fillna(0, inplace=True)

# drop columns which are not needed
df_all.drop(["Package Name", "Daily ANRs", "Total Average Rating", "Country"], axis=1, inplace=True)
df_all = df_all.loc[(df_all['Daily Crashes'] != 0) | (df_all['Daily Average Rating'] != 0)]
df_all.drop_duplicates(inplace=True)

# reset index
df_all = df_all.reset_index(drop=True)

# save the combined data to a new CSV file
df_all.to_csv(r"C:\Users\Toly\Desktop\test.csv", index=False)


# Load data
daily = pd.read_csv(r"C:\Users\Toly\Desktop\test.csv", parse_dates=['Date'])
daily.columns = daily.columns.str.strip()
dates = pd.to_datetime(daily['Date'])

# Create ColumnDataSource
source = ColumnDataSource(data=daily)

# Create initial plot

p = figure(x_axis_type='datetime', height=300, width=600,
           title='Daily', x_axis_label='Date', y_axis_label='Rating', toolbar_location='right')
crashes_step = p.step('Date', 'Daily Crashes', color='#007A33', legend_label='Crashes', source=source, line_alpha=0.7)
ratings_step = p.step('Date', 'Daily Average Rating', color='#CE1141', legend_label='Ratings', source=source, line_alpha=0.7)

# Create the menu for the dropdown
menu = [("A", "Option 1"), ("B", "option 2"), ("C", "option 3")]

# Create a div to display the selected option
div = Div()

dropdown = Dropdown(label="Select an option", menu=menu, button_type="warning")
# Define a JavaScript callback to update the div with the selected option
callback = CustomJS(args=dict(div=div, dropdown=dropdown), code="""
    var selected_option = dropdown.item;
    var option_variable = 42;
    dropdown.button_label = selected_option;
    if (selected_option == "A") {
        div.text = option_variable;
    }
""")

# Create the dropdown menu with the callback

dropdown.js_on_event("menu_item_click", CustomJS(
    code="console.log('dropdown: ' + this.item, this.toString())"))
#ropdown.js_on_change('value', callback)
# Create a layout with the Select widget and the plot
layout = column(p, dropdown, div)

p.legend.title = 'Legend Title'
p.legend.label_text_font_size = '12pt'
p.legend.location = 'top_left'
# Show the plot
output_file("gridplot.html")
output_notebook()
show(layout)


# In[ ]:





# In[ ]:




