from bokeh.io import curdoc
from bokeh.models.widgets import Div
from bokeh.layouts import column, row


from bokeh.models import ColumnDataSource, Select, RadioButtonGroup, HoverTool
from bokeh.plotting import figure, show


import pandas as pd

def bokeh_sales_by_time(datafile):
    # Load the data
    df = pd.read_csv(datafile, parse_dates=['Transaction Date'])
    monthly_sales = df.groupby(pd.Grouper(key='Transaction Date', freq='M')).agg({'Description': 'count'}).reset_index()
    daily_sales = df.groupby(pd.Grouper(key='Transaction Date', freq='D')).agg({'Description': 'count'}).reset_index()

    # Define the data source for the plot
    source = ColumnDataSource(df)

    # Define the options for the x-axis selector
    x_axis_options = ['Month', 'Day']

    # Define the options for the y-axis selector
    y_axis_options = ['Transaction Count']

    # Define the figure
    p = figure(x_axis_type='datetime', width=800, height=400, title='Sales over time')
    p.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Transaction Count', '@Description')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))

    # Add the glyphs to the figure
    line_glyph = p.line(x='Transaction Date', y='Description', source=source, color='blue', legend_label='Transaction Count')

    # Define the update function for the x-axis selector
    def update_x_axis(attr, old, new):
        if new == 'Month':
            p.xaxis.axis_label = 'Month'
            data = monthly_sales
            line_glyph.data_source.data = data
        elif new == 'Day':
            p.xaxis.axis_label = 'Day'
            data = daily_sales
            line_glyph.data_source.data = data

    # Define the update function for the y-axis selector
    def update_y_axis(attr, old, new):
        if new == 'Transaction Count':
            p.yaxis.axis_label = 'Transaction Count'
            line_glyph.y = 'Description'
            line_glyph.data_source.data = source.data

    # Create the x-axis selector
    x_axis_selector = Select(title='X-Axis', options=x_axis_options, value='Month')
    x_axis_selector.on_change('value', update_x_axis)

    # Create the y-axis selector
    y_axis_selector = RadioButtonGroup(labels=y_axis_options, active=0)
    y_axis_selector.on_change('active', update_y_axis)

    # Add the widgets to the layout
    layout = column(x_axis_selector, y_axis_selector, p)

    # Register the layout with the current document
    curdoc().add_root(layout)

    # Display the plot
    curdoc().title = 'Amount of Transactions'

bokeh_sales_by_time('sales_filtered.csv')


from bokeh.models.widgets import Div

def sales_vol():
    # Load the data
    df = pd.read_csv('sales_filtered.csv', parse_dates=['Transaction Date'])
    
    # Clean the column name
    df = df.rename(columns={'Amount (Merchant Currency)': 'Amount'})

    daily_sales_volume = df.groupby(pd.Grouper(key='Transaction Date', freq='D')).agg({'Amount': 'sum'}).reset_index()
    monthly_sales_volume = df.groupby(pd.Grouper(key='Transaction Date', freq='M')).agg({'Amount': 'sum'}).reset_index()

    # Calculate daily and monthly average sales volume
    daily_avg = daily_sales_volume['Amount'].mean()
    monthly_avg = monthly_sales_volume['Amount'].mean()

    # Define the data source for the plot
    daily_source = ColumnDataSource(daily_sales_volume)
    monthly_source = ColumnDataSource(monthly_sales_volume)

    # Define the options for the x-axis selector
    x_axis_options = ['Month', 'Day']

    # Define the figure
    p = figure(x_axis_type='datetime', width=800, height=400, title='Sales Volume over time')
    p.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))

    # Add the glyphs to the figure
    daily_line_glyph = p.line(x='Transaction Date', y='Amount', source=daily_source, color='blue', legend_label='Daily Sales Volume')
    monthly_line_glyph = p.line(x='Transaction Date', y='Amount', source=monthly_source, color='red', legend_label='Monthly Sales Volume')


    # Define the update function for the x-axis selector
    def update_x_axis(attr, old, new):
        if new == 'Month':
            p.xaxis.axis_label = 'Month'
            daily_line_glyph.visible = False
            monthly_line_glyph.visible = True
            p.x_range.end = pd.Timestamp.now().date().replace(day=1)
        elif new == 'Day':
            p.xaxis.axis_label = 'Day'
            daily_line_glyph.visible = True
            monthly_line_glyph.visible = False
            p.x_range.end = pd.Timestamp.now().date()

    # Create the x-axis selector
    x_axis_selector = Select(title='X-Axis', options=x_axis_options, value='Day')
    x_axis_selector.on_change('value', update_x_axis)

    # Create the div widgets for displaying the daily and monthly average sales volume
    daily_avg_div = Div(text=f"Daily Average Sales Volume: {daily_avg:.2f}")
    monthly_avg_div = Div(text=f"Monthly Average Sales Volume: {monthly_avg:.2f}")

    # Add the widgets and plot to the layout
    layout = column(x_axis_selector, p, daily_avg_div, monthly_avg_div)

    # Add the layout to the current document
    curdoc().add_root(layout)

    # Display the plot
    curdoc().title = 'Sales volume'

# Run the app
sales_vol()


from bokeh.models import Legend


def sku_sales_vol():
    # Load the data
    df = pd.read_csv('sales_filtered.csv', parse_dates=['Transaction Date'])

    # Clean the column names
    df = df.rename(columns={'Amount (Merchant Currency)': 'Amount', 'Sku Id': 'Sku_Id'})

    # Group by transaction date and Sku_Id
    sales_volume = df.groupby([pd.Grouper(key='Transaction Date', freq='D'), 'Sku_Id']).agg({'Amount': 'sum'}).reset_index()

    # Calculate daily and monthly average sales volume for each Sku_Id value
    daily_avg = sales_volume.groupby('Sku_Id')['Amount'].mean().to_dict()
    monthly_avg = sales_volume.groupby(['Sku_Id', pd.Grouper(key='Transaction Date', freq='M')])['Amount'].sum().groupby('Sku_Id').mean().to_dict()

    # Define the figure
    p = figure(x_axis_type='datetime', width=800, height=400, title='Sales Volume by SKU over Time')
    p.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))

    # Define the line colors for each Sku_Id value
    colors = {'unlockcharactermanager': 'blue', 'premium': 'red'}

    # Define the update function for the x-axis selector
    def update_x_axis(attr, old, new):
        pass

    # Define the data source for the plot
    source = ColumnDataSource(sales_volume)

    # Add the glyphs to the figure
    glyphs = {}
    for sku_id in sales_volume['Sku_Id'].unique():
        filtered_data = sales_volume[sales_volume['Sku_Id'] == sku_id]
        source = ColumnDataSource(filtered_data)
        glyphs[sku_id] = p.line(x='Transaction Date', y='Amount', source=source, color=colors[sku_id], line_width=2, legend_label=sku_id)

    # Create the legend
    legend = Legend(items=[(sku_id, [glyphs[sku_id]]) for sku_id in sales_volume['Sku_Id'].unique()])

    # Create the div widget for displaying the daily or monthly average sales volume
    avg_divs = {}
    for sku_id in sales_volume['Sku_Id'].unique():
        avg_divs[sku_id] = Div(text=f"Daily Average Sales Volume ({sku_id}): {daily_avg[sku_id]:.2f}<br>Monthly Average Sales Volume ({sku_id}): {monthly_avg[sku_id]:.2f}", width=400, height=100)

    # Define the layout
    layout = column(p, *avg_divs.values())

    # Add the widgets and plot to the layout


    # Add the layout to the current document
    curdoc().add_root(layout)

    # Display the plot
    curdoc().title = 'Sales volume by SKU'

sku_sales_vol()

import pandas as pd
from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.transform import cumsum

from bokeh.palettes import Category20
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.transform import cumsum
from bokeh.transform import factor_cmap

from bokeh.layouts import column
import pandas as pd


from bokeh.palettes import Category20

from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
import pandas as pd

from bokeh.transform import factor_cmap

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
from bokeh.palettes import Category20

from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.palettes import Category20
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
import pandas as pd

def sku_sales_bar(filename):
    # Load the data
    df = pd.read_csv(filename)

    # Clean the column names
    df = df.rename(columns={'Buyer Country': 'Buyer_Country', 'Sku Id': 'Sku_Id'})

    # Create the figures
    figures = []
    for sku_id in df['Sku_Id'].unique():
        # Filter the data by Sku_Id
        filtered_data = df[df['Sku_Id'] == sku_id]

        # Group the data by Buyer_Country and count the number of occurrences
        country_counts = filtered_data.groupby('Buyer_Country').size().reset_index(name='counts')

        # Define the colors for the bar chart
        colors = Category20[20] * 2
        
        # Create a ColumnDataSource object
        data_source = ColumnDataSource(country_counts)

        # Create the figure
        p = figure(title=f'Buyer Countries for Sku_Id {sku_id}', x_range=FactorRange(factors=country_counts['Buyer_Country'].unique()), width=800, height=400)

        # Create the vbar glyph and add it to the plot
        glyph = p.vbar(x='Buyer_Country', top='counts', width=0.9, legend_label='counts', source=data_source, 
                       fill_color=factor_cmap('Buyer_Country', palette=colors, factors=country_counts['Buyer_Country'].unique()))
        
        # Define the hovertool
        hover = HoverTool(tooltips=[('Buyer Country', '@Buyer_Country'), ('Counts', '@counts')])

        # Add the hovertool to the plot
        p.add_tools(hover)

        # Add the figure to the list of figures
        figures.append(p)

    # Display the figures
    show(column(*figures))

#sku_sales_bar('sales_filtered.csv')









