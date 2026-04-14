python
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
data = pd.read_excel('Indices_Summary_March.xlsx')

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('March 2026 Sector Indices Dashboard'),
    
    # Dropdown for selecting an index
    html.Label('Select Index:'),
    dcc.Dropdown(
        id='index-dropdown',
        options=[{'label': i, 'value': i} for i in data['index_name'].unique()],
        value=data['index_name'].unique()[0]
    ),

    # Date picker range
    html.Label('Select Date Range:'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=data['date'].min(),
        end_date=data['date'].max()
    ),

    # Graph output
    dcc.Graph(id='trend-graph')
])

# Callback to update graph
@app.callback(
    Output('trend-graph', 'figure'),
    [Input('index-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_index, start_date, end_date):
    filtered_data = data[(data['index_name'] == selected_index) &
                         (data['date'] >= start_date) &
                         (data['date'] <= end_date)]
    fig = px.line(filtered_data, x='date', y='closing_value', title=f'Trend for {selected_index}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
