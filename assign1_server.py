from bokeh.io import curdoc
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

#bokeh_sales_by_time('sales_filtered.csv')


import pandas as pd



from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.plotting import figure, curdoc
import pandas as pd

def sales_vol():
    # Load the data
    df = pd.read_csv('sales_filtered.csv', parse_dates=['Transaction Date'])
    
    # Clean the column name
    df = df.rename(columns={'Amount (Merchant Currency)': 'Amount'})

    daily_sales_volume = df.groupby(pd.Grouper(key='Transaction Date', freq='D')).agg({'Amount': 'sum'}).reset_index()
    monthly_sales_volume = df.groupby(pd.Grouper(key='Transaction Date', freq='M')).agg({'Amount': 'sum'}).reset_index()

    # Define the data source for the plot
    source = ColumnDataSource(daily_sales_volume)

    # Define the options for the x-axis selector
    x_axis_options = ['Month', 'Day']

    # Define the figure
    p = figure(x_axis_type='datetime', width=800, height=400, title='Sales Volume over time')
    p.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount}{($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime', '@{Amount}': 'printf'}
    ))

    # Add the glyphs to the figure
    line_glyph = p.line(x='Transaction Date', y='Amount', source=source, color='blue', legend_label='Sales Volume')


    # Define the update function for the x-axis selector
    def update_x_axis(attr, old, new):
        if new == 'Month':
            p.xaxis.axis_label = 'Month'
            source.data = monthly_sales_volume
            line_glyph.x = 'Transaction Date'
            p.x_range.end = pd.Timestamp.now().date().replace(day=1)
        elif new == 'Day':
            p.xaxis.axis_label = 'Day'
            source.data = daily_sales_volume
            line_glyph.x = 'Transaction Date'
            p.x_range.end = pd.Timestamp.now().date()

    # Create the x-axis selector
    x_axis_selector = Select(title='X-Axis', options=x_axis_options, value='Day')
    x_axis_selector.on_change('value', update_x_axis)

    # Add the widgets and plot to the layout
    layout = column(x_axis_selector, p)

    # Add the layout to the current document
    curdoc().add_root(layout)

    # Display the plot
    curdoc().title = 'Sales volume'

# Run the app
sales_vol()



def bokeh_2(datafile):
    # Load the data
    df = pd.read_csv(datafile, parse_dates=['Transaction Date'])

    # Define the data source for the plot
    source = ColumnDataSource(df)

    # Define the options for the x-axis selector
    x_axis_options = ['Sku Id', 'Buyer Currency', 'Buyer country', 'Time of Day']

    # Define the options for the y-axis selector
    y_axis_options = ['Transaction Count', 'Sales Volume']

    # Define the figure
    p = figure(x_axis_label='X Axis', y_axis_label='Y Axis', width=800, height=400, title='Sales over time')
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
        if new == 'Sku Id':
            p.xaxis.axis_label = 'Sku Id'
            line_glyph.data_source.data = df.groupby(['Transaction Date', 'Sku Id']).agg({'Amount (Buyer Currency)': 'sum', 'Description': 'count'}).reset_index()
        elif new == 'Buyer Currency':
            p.xaxis.axis_label = 'Buyer Currency'
            line_glyph.data_source.data = df.groupby(['Transaction Date', 'Buyer Currency']).agg({'Amount (Buyer Currency)': 'sum', 'Description': 'count'}).reset_index()
        elif new == 'Buyer country':
            p.xaxis.axis_label = 'Buyer country'
            line_glyph.data_source.data = df.groupby(['Transaction Date', 'Buyer country']).agg({'Amount (Buyer Currency)': 'sum', 'Description': 'count'}).reset_index()
        elif new == 'Time of Day':
            p.xaxis.axis_label = 'Time of Day'
            df['Time of Day'] = pd.cut(df['Transaction Date'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'])
            line_glyph.data_source.data = df.groupby(['Transaction Date', 'Time of Day']).agg({'Amount (Buyer Currency)': 'sum', 'Description': 'count'}).reset_index()

    # Define the update function for the y-axis selector
    def update_y_axis(attr, old, new):
        if new == 'Transaction Count':
            p.yaxis.axis_label = 'Transaction Count'
            line_glyph.y = 'Description'
        elif new == 'Sales Volume':
            p.yaxis.axis_label = 'Sales Volume'
            line_glyph.y = 'Amount (Buyer Currency)'

    # Create the x-axis selector
    x_axis_selector = Select(title='X-Axis', options=x_axis_options, value='Sku Id')
    x_axis_selector.on_change('value', update_x_axis)

    # Create the y-axis selector
    y_axis_selector = RadioButtonGroup(labels=y_axis_options, active=0)
    y_axis_selector.on_change('active', update_y_axis)

    # Add the widgets to the layout
    layout = column(row(x_axis_selector, y_axis_selector), p)

    # Register the layout with the current document
    curdoc().add_root(layout)

    # Display the plot
    curdoc().title = 'Sales per attribute'

#bokeh_2('sales_filtered.csv')
