# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import datetime
import requests
from io import BytesIO

# Load sunspot data from CSV file
sunspots_df = pd.read_csv('sunspots.csv')

# Convert column names to uppercase
sunspots_df.columns = sunspots_df.columns.str.upper()

# Create Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    # Panel 1: Historical Sunspot Activity
    html.Div([
        dcc.Graph(id='historical-sunspot-activity'),
        # Dashboard controls for selecting range and smoothing
        dcc.RangeSlider(
            id='MONTH-RANGE',
            marks={month: str(month) for month in sunspots_df['MONTH']},
            min=sunspots_df['MONTH'].min(),
            max=sunspots_df['MONTH'].max(),
            step=1,
            value=[sunspots_df['MONTH'].min(), sunspots_df['MONTH'].max()]
        ),
        dcc.Slider(
            id='SMOOTHING-SLIDER',
            min=1,
            max=30,
            step=1,
            marks={i: str(i) for i in range(1, 31)},
            value=10,
            tooltip={'placement': 'bottom', 'always_visible': True}
        )
    ]),

    # Panel 2: Sunspot Cycle Variability
    html.Div([
        dcc.Graph(id='sunspot-cycle-variability'),
        # Dashboard control for tuning cycle period
        dcc.Slider(
            id='CYCLE-PERIOD-SLIDER',
            min=10,
            max=12,
            step=0.1,
            marks={i: str(i) for i in range(10, 13)},
            value=11,
            tooltip={'placement': 'bottom', 'always_visible': True}
        )
    ]),

    # Panel 3: Real-Time Image of the Sun
    html.Div([
        html.Img(id='real-time-sun-image', src='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg', width='100%')
    ])
])

# Callback for updating historical sunspot activity graph
@app.callback(
    Output('historical-sunspot-activity', 'figure'),
    [Input('MONTH-RANGE', 'value'),
     Input('SMOOTHING-SLIDER', 'value')]
)
def update_historical_sunspot_activity(selected_months, smoothing_period):
    filtered_df = sunspots_df[(sunspots_df['MONTH'] >= selected_months[0]) & (sunspots_df['MONTH'] <= selected_months[1])]
    smoothed_data = filtered_df['NUM_SUNSPOTS'].rolling(window=smoothing_period).mean()

    fig = px.line(filtered_df, x='MONTH', y='NUM_SUNSPOTS', title='Historical Sunspot Activity')
    fig.add_scatter(x=filtered_df['MONTH'], y=smoothed_data, mode='lines', name=f'Smoothed ({smoothing_period} months)')
    return fig

# Callback for updating sunspot cycle variability graph
@app.callback(
    Output('sunspot-cycle-variability', 'figure'),
    [Input('CYCLE-PERIOD-SLIDER', 'value')]
)
def update_sunspot_cycle_variability(cycle_period):
    sunspots_df['CYCLE MODULUS'] = sunspots_df['MONTH'] % cycle_period

    fig = px.scatter(sunspots_df, x='MONTH', y='CYCLE MODULUS', title='Sunspot Cycle Variability')
    return fig

# Callback for updating real-time image of the sun
@app.callback(
    Output('real-time-sun-image', 'src'),
    [Input('CYCLE-PERIOD-SLIDER', 'value')]  # Just to have a callback for real-time image
)
def update_real_time_sun_image(cycle_period):
    # Use the provided NASA link for the real-time image
    return 'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
