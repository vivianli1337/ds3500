"""
contributors: Ryan Wu, Daniel Veretenov, Vivian Li
course: DS3500 Advanced Programming
prof: Prof. Rachlin
date: Feb. 16, 2024
"""
# import libraries and functions
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from sankey import make_sankey
from bar_chart import make_bar_chart
from pie_chart import make_pie_chart
from crime import make_line_chart

# get data of criminals & crime
df1 = pd.read_csv('Downloads/hw3/county_age_gen_crime_2022.csv')
df1 = df1.fillna(0)
df1["Number of Incidents"] = df1["Number of Incidents"].apply(lambda x: int(x.replace(',', '')) if isinstance(x, str) else x)

# sum the number of incidents for each gender in each jurisdiction
summed_df_bar = df1.groupby(["Jurisdiction by Geography", "Offender Gender"])["Number of Incidents"].sum().reset_index()
summed_df_bar = summed_df_bar[summed_df_bar["Jurisdiction by Geography"] != "Missing"]  

# get the crime data & time
crime = pd.read_csv('Downloads/hw3/crime.csv', encoding='latin1')
# drop  unnecessary cols and rows
columns_to_drop = ['OFFENSE_CODE', 'OFFENSE_DESCRIPTION', 'DISTRICT', 'REPORTING_AREA', 'SHOOTING',
                   'UCR_PART', 'STREET', 'Lat', 'Long', 'Location']
crime.drop(columns=columns_to_drop, inplace=True)
crime.dropna(inplace=True)

# crate dash ap
app = dash.Dash(__name__)

# create layout
app.layout = html.Div([
    html.P("Select sankey:"),
    html.Div([
        dcc.Dropdown(
            id='sankey-dropdown',
            options=[
                {'label': 'Gender to Race', 'value': 'gender_to_race'},
                {'label': 'Jurisdiction to Race', 'value': 'jurisdiction_to_race'},
                {'label': 'Gender to Race to Jurisdiction', 'value': 'gender_to_race_to_jurisdiction'}
            ],
            value='gender_to_race'
        ),
        dcc.Graph(id='sankey-graph')
    ]),
    html.Div([
        dcc.Graph(id='bar-chart'),
        html.P("Select Counties:"),
        dcc.Checklist(
            id='county-checklist',
            options=[
                {'label': 'All Counties', 'value': 'all'},
                {'label': 'Suffolk County', 'value': 'Suffolk County'},
                {'label': 'Hampden County', 'value': 'Hampden County'},
                {'label': 'Bristol County', 'value': 'Bristol County'},
                {'label': 'Middlesex County', 'value': 'Middlesex County'},
                {'label': 'Worcester County', 'value': 'Worcester County'},
                {'label': 'Essex County', 'value': 'Essex County'},
                {'label': 'Plymouth County', 'value': 'Plymouth County'},
                {'label': 'Norfolk County', 'value': 'Norfolk County'},
                {'label': 'Barnstable County', 'value': 'Barnstable County'},
                {'label': 'Berkshire County', 'value': 'Berkshire County'},
                {'label': 'Hampshire County', 'value': 'Hampshire County'},
                {'label': 'Dukes County', 'value': 'Dukes County'},
                {'label': 'Franklin County', 'value': 'Franklin County'},
                {'label': 'Nantucket County', 'value': 'Nantucket County'}
            ],
            value=['all'],
            labelStyle={'display': 'block'}
        ),
        html.P("Select Desired Minimal Number of Incidents:"),
        dcc.Input(
            id='min-incidents-input',
            type='number',
            placeholder='Enter minimum number of incidents',
            value=0
        ),
    ]),
    html.Div([
        dcc.Graph(id='pie-chart')
    ]),
    html.P("Select day:"),
    html.Div([
        dcc.RadioItems(
            id='line-chart-radio',
            options=[
                {'label': 'All Days', 'value': 'All'},
                {'label': 'Monday', 'value': 'Monday'},
                {'label': 'Tuesday', 'value': 'Tuesday'},
                {'label': 'Wednesday', 'value': 'Wednesday'},
                {'label': 'Thursday', 'value': 'Thursday'},
                {'label': 'Friday', 'value': 'Friday'},
                {'label': 'Saturday', 'value': 'Saturday'},
                {'label': 'Sunday', 'value': 'Sunday'}
            ],
            value='All',
            inline=True
        ),
        dcc.Graph(id='line-chart')
    ]),
])


# define callback function for dropdown sankey diagram
@app.callback(
    Output('sankey-graph', 'figure'),
    [Input('sankey-dropdown', 'value')]
)
# update the sankey
def update_sankey(selected_sankey):
    if selected_sankey == 'gender_to_race':
        gr_data = df1.groupby(['Offender Gender', 'Offender Race'])['Number of Incidents'].sum().reset_index()
        return make_sankey(gr_data, 'Offender Gender', 'Offender Race',
                           'Number of Incidents', "Gender to Race Sankey Diagram")
    elif selected_sankey == 'jurisdiction_to_race':
        jr_data = df1.groupby(['Jurisdiction by Geography', 'Offender Race'])['Number of Incidents'].sum().reset_index()
        return make_sankey(jr_data, 'Jurisdiction by Geography', 'Offender Race',
                           'Number of Incidents', "Jurisdiction to Race Sankey Diagram")
    elif selected_sankey == 'gender_to_race_to_jurisdiction':
        grouped_data = df1.groupby(['Offender Gender', 'Offender Race',
                                    'Jurisdiction by Geography'])['Number of Incidents'].sum().reset_index()
        labels = pd.concat([
            grouped_data['Offender Gender'],
            grouped_data['Offender Race'],
            grouped_data['Jurisdiction by Geography']
        ]).unique()
        label_to_id = {label: i for i, label in enumerate(labels)}
        source_ids = grouped_data.apply(lambda row: label_to_id[row['Offender Gender']], axis=1)
        target_ids = grouped_data.apply(lambda row: label_to_id[row['Offender Race']], axis=1)
        race_to_jurisdiction_target_ids = grouped_data.apply(lambda row: label_to_id[row['Jurisdiction by Geography']],
                                                             axis=1)
        source_ids_full = pd.concat([source_ids, grouped_data['Offender Race'].map(label_to_id)])
        target_ids_full = pd.concat([target_ids, race_to_jurisdiction_target_ids])
        values_full = pd.concat([grouped_data['Number of Incidents'], grouped_data['Number of Incidents']])
        return go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            link=dict(
                source=source_ids_full,
                target=target_ids_full,
                value=values_full
            ))]).update_layout(title_text="Gender to Race to Jurisdiction Sankey Diagram", font_size=10)


# define callback function for bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('county-checklist', 'value'),
     Input('min-incidents-input', 'value')]
)
# update the bar chart
def update_bar_chart(selected_counties, min_incidents):
    if 'all' in selected_counties:
        filtered_df = summed_df_bar.copy()
    else:
        filtered_df = summed_df_bar[summed_df_bar['Jurisdiction by Geography'].isin(selected_counties)]

    filtered_df = filtered_df[filtered_df['Number of Incidents'] >= min_incidents]
    updated_fig = make_bar_chart(filtered_df)

    return updated_fig


# define callback function for pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('sankey-dropdown', 'value')]
)
# update the pie chart
def update_pie_chart(data):
    return make_pie_chart(df1)  # Use the original DataFrame for the pie chart


# define callback function for line graph
@app.callback(
    Output('line-chart', 'figure'),
    [Input('line-chart-radio', 'value')]
)
# update the pie chart
def update_line_chart(selected_day):
    if selected_day == 'All':
        filtered_data = crime.copy()
    else:
        filtered_data = crime[crime['DAY_OF_WEEK'] == selected_day]
    fig = make_line_chart(filtered_data)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
