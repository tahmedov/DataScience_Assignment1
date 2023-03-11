from bokeh.io import output_file, show, save
from bokeh.layouts import row, gridplot
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
import pandas as pd
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column

def bokeh_sales_by_time(datafile):
    # Load the data
    df = pd.read_csv(datafile, parse_dates=['Transaction Date'])

    # Compute monthly and daily sales and transactions
    monthly_sales = df.groupby(pd.Grouper(key='Transaction Date', freq='M')).agg({'Amount (Merchant Currency)': 'sum', 'Description': 'count'}).reset_index()
    daily_sales = df.groupby(pd.Grouper(key='Transaction Date', freq='D')).agg({'Amount (Merchant Currency)': 'sum', 'Description': 'count'}).reset_index()

    # Define the data sources for the plots
    monthly_trans_source = ColumnDataSource(monthly_sales)
    daily_trans_source = ColumnDataSource(daily_sales)
    monthly_sales_source = ColumnDataSource(monthly_sales)
    daily_sales_source = ColumnDataSource(daily_sales)

    # Define the figure for the monthly transaction plot
    monthly_trans_fig = figure(x_axis_type='datetime', width=400, height=400, title='Monthly Transactions')
    monthly_trans_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Transaction Count', '@Description')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))
    monthly_trans_fig.line(x='Transaction Date', y='Description', source=monthly_trans_source, color='red', legend_label='Monthly Transactions')

    # Define the figure for the daily transaction plot
    daily_trans_fig = figure(x_axis_type='datetime', width=400, height=400, title='Daily Transactions')
    daily_trans_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Transaction Count', '@Description')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))
    daily_trans_fig.line(x='Transaction Date', y='Description', source=daily_trans_source, color='blue', legend_label='Daily Transactions')

    # Define the figure for the monthly sales plot
    monthly_sales_fig = figure(x_axis_type='datetime', width=400, height=400, title='Monthly Sales')
    monthly_sales_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount (Merchant Currency)}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))
    monthly_sales_fig.line(x='Transaction Date', y='Amount (Merchant Currency)', source=monthly_sales_source, color='red', legend_label='Monthly Sales Volume')

    # Define the figure for the daily sales plot
    daily_sales_fig = figure(x_axis_type='datetime', width=400, height=400, title='Daily Sales')
    daily_sales_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount (Merchant Currency)}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))
    daily_sales_fig.line(x='Transaction Date', y='Amount (Merchant Currency)', source=daily_sales_source, color='blue', legend_label='Daily Sales Volume')

    # Combine the plots into a layout and save it to an HTML file
    layout = gridplot([[monthly_trans_fig, monthly_sales_fig], [daily_trans_fig, daily_sales_fig]])
    output_file('graphs.html')
    save(layout)




def sku_sales_vol(filename):
    # Load the data
    df = pd.read_csv(filename, parse_dates=['Transaction Date'])

    # Clean the column names
    df = df.rename(columns={'Amount (Merchant Currency)': 'Amount', 'Sku Id': 'Sku_Id'})

    # Group by transaction date and Sku_Id
    sales_volume = df.groupby(['Transaction Date', 'Sku_Id']).agg({'Amount': 'sum'}).reset_index()

    # Calculate daily and monthly sales volume for each Sku_Id value
    daily_sales = sales_volume.groupby(['Transaction Date', 'Sku_Id']).agg({'Amount': 'sum'}).reset_index()
    monthly_sales = sales_volume.groupby('Sku_Id').resample('M', on='Transaction Date').agg({'Amount': 'sum'}).reset_index()

    # Define the figure for the daily sales plot
    daily_sales_fig = figure(x_axis_type='datetime', width=800, height=400, title='Daily Sales Volume by SKU')
    daily_sales_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))

    # Define the figure for the monthly sales plot
    monthly_sales_fig = figure(x_axis_type='datetime', width=800, height=400, title='Monthly Sales Volume by SKU')
    monthly_sales_fig.add_tools(HoverTool(
        tooltips=[
            ('Date', '@{Transaction Date}{%F}'),
            ('Sales Volume', '@{Amount}{numeral($ 0.00 a)}')
        ],
        formatters={'@{Transaction Date}': 'datetime'}
    ))

    # Define the line colors for each Sku_Id value
    colors = {'unlockcharactermanager': 'blue', 'premium': 'red'}

    # Define the data source for the daily sales plot
    daily_sales_source = ColumnDataSource(daily_sales)

    # Define the data source for the monthly sales plot
    monthly_sales_source = ColumnDataSource(monthly_sales)

    # Add the glyphs to the daily sales figure
    for sku_id in daily_sales['Sku_Id'].unique():
        filtered_data = daily_sales[daily_sales['Sku_Id'] == sku_id]
        source = ColumnDataSource(filtered_data)
        daily_sales_fig.line(x='Transaction Date', y='Amount', source=source, color=colors[sku_id], line_width=2, legend_label=sku_id)

    # Add the glyphs to the monthly sales figure
    for sku_id in monthly_sales['Sku_Id'].unique():
        filtered_data = monthly_sales[monthly_sales['Sku_Id'] == sku_id]
        source = ColumnDataSource(filtered_data)
        monthly_sales_fig.line(x='Transaction Date', y='Amount', source=source, color=colors[sku_id], line_width=2, legend_label=sku_id)

    # Define the layout
    layout = column(daily_sales_fig, monthly_sales_fig)

    # Add the widgets and plot to the layout
    output_file('graphs.html')
    save(layout)




def plots(filename):
    # Load the data into a DataFrame
    df = pd.read_csv(filename, parse_dates=['Transaction Date'])

    # Generate the Bokeh plots
    monthly_sales, daily_sales, daily_sales_fig, monthly_sales_fig = bokeh_sales_by_time(df)
    sku_sales_vol(df)

    # Combine the plots into a layout and save it to an HTML file
    layout = gridplot([[monthly_sales_fig, monthly_sales], [daily_sales_fig, daily_sales]])
    output_file('graphs.html')
    save(layout)



plots('sales_filtered.csv')

