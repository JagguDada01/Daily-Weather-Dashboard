import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ---------------------------------------------
# Load and preprocess the weather dataset
# ---------------------------------------------
df = pd.read_csv("weather_data.csv")

# Rename columns for consistency and readability
df.rename(columns={
    'datetime': 'Date',
    'temp': 'Temperature',
    'humidity': 'Humidity',
    'conditions': 'Condition'
}, inplace=True)

# Convert date strings to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Remove any extra spaces from condition labels
df['Condition'] = df['Condition'].str.strip()

# Set default date range to the last 30 days
default_end_date = df['Date'].max()
default_start_date = default_end_date - pd.DateOffset(days=30)

# ---------------------------------------------
# Initialize Dash app
# ---------------------------------------------
app = dash.Dash(__name__)
app.title = "Daily Weather Dashboard"

# ---------------------------------------------
# App layout
# ---------------------------------------------
app.layout = html.Div([
    html.Div([
        html.H1("Daily Weather Dashboard", style={'textAlign': 'center', 'marginBottom': '10px'}),

        # Light/Dark mode toggle in the top-right corner
        html.Div([
            dcc.RadioItems(
                id='theme-toggle',
                options=[
                    {'label': '☀️ Light Mode', 'value': 'plotly'},
                    {'label': '🌙 Dark Mode', 'value': 'plotly_dark'}
                ],
                value='plotly',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'},
                style={'display': 'inline-block'}
            )
        ], style={'position': 'absolute', 'top': '20px', 'right': '30px'})

    ], style={'position': 'relative'}),

    # Date range picker and quick-select buttons
    html.Div([
        html.Label("Select Date Range:", style={'fontWeight': 'bold'}),
        dcc.DatePickerRange(
            id='date-range',
            start_date=default_start_date,
            end_date=default_end_date,
            min_date_allowed=df['Date'].min(),
            max_date_allowed=df['Date'].max(),
            display_format='DD-MM-YYYY',
            style={"border": "1px solid #ccc", "padding": "10px", "borderRadius": "8px"}
        ),

        # Predefined range buttons
        html.Div([
            html.Button("Last 7 Days", id='btn-7d', n_clicks=0, style={"margin": "5px"}),
            html.Button("Last 30 Days", id='btn-30d', n_clicks=0, style={"margin": "5px"}),
            html.Button("Last 3 Months", id='btn-90d', n_clicks=0, style={"margin": "5px"})
        ], style={'marginTop': '10px'})
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Graphs section
    dcc.Graph(id='temp-line-chart'),
    dcc.Graph(id='humidity-bar-chart'),
    dcc.Graph(id='condition-pie-chart')
])

# ---------------------------------------------
# Update date picker based on button click
# ---------------------------------------------
@app.callback(
    Output('date-range', 'start_date'),
    Output('date-range', 'end_date'),
    Input('btn-7d', 'n_clicks'),
    Input('btn-30d', 'n_clicks'),
    Input('btn-90d', 'n_clicks')
)
def update_range(n7, n30, n90):
    ctx = dash.callback_context

    # If no button clicked, show last 30 days
    if not ctx.triggered:
        return default_start_date, default_end_date

    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Return appropriate date range based on which button was clicked
    if btn_id == 'btn-7d':
        return default_end_date - pd.DateOffset(days=7), default_end_date
    elif btn_id == 'btn-30d':
        return default_end_date - pd.DateOffset(days=30), default_end_date
    elif btn_id == 'btn-90d':
        return default_end_date - pd.DateOffset(days=90), default_end_date

    return default_start_date, default_end_date

# ---------------------------------------------
# Update all graphs based on selected date range and theme
# ---------------------------------------------
@app.callback(
    [
        Output('temp-line-chart', 'figure'),
        Output('humidity-bar-chart', 'figure'),
        Output('condition-pie-chart', 'figure')
    ],
    [
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
        Input('theme-toggle', 'value')
    ]
)
def update_graphs(start_date, end_date, theme):
    # Filter dataset based on selected date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Temperature line chart
    temp_fig = px.line(
        filtered_df, x='Date', y='Temperature',
        title='Temperature Over Time',
        markers=True,
        labels={'Temperature': 'Temp (°C)'},
        template=theme
    )

    # Humidity bar chart
    humidity_fig = px.bar(
        filtered_df, x='Date', y='Humidity',
        title='Humidity Levels',
        labels={'Humidity': 'Humidity (%)'},
        color='Humidity',
        template=theme
    )

    # Condition distribution pie chart
    condition_counts = filtered_df['Condition'].value_counts().reset_index()
    condition_counts.columns = ['Condition', 'Count']
    pie_fig = px.pie(
        condition_counts, names='Condition', values='Count',
        title='Weather Condition Distribution',
        template=theme
    )

    return temp_fig, humidity_fig, pie_fig

# ---------------------------------------------
# Run the Dash app
# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)