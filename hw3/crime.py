# import library
import plotly.graph_objects as go


#
def make_line_chart(df):
    """ Generate a line chart showing the different number of crimes committed per hour in each day
    :param df: DataFrame containing the crime data: 'DAY_OF_WEEK', 'HOUR'
    :return fig (go.Figure): Plotly figure object representing the line chart.
    """

    # group by 'DAY_OF_WEEK' and 'HOUR', and count the number of occurrences
    grouped_data = df.groupby(['DAY_OF_WEEK', 'HOUR']).size().reset_index(name='Crime_Count')

    # pivot the data to have 'HOUR' as columns and 'DAY_OF_WEEK' as rows
    pivot_data = grouped_data.pivot(index='HOUR', columns='DAY_OF_WEEK', values='Crime_Count')

    # create an interactive line plot using plotly
    fig = go.Figure()

    for day in pivot_data.columns:
        fig.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[day], mode='lines+markers', name=day))

    # update the layout
    fig.update_layout(title='Number of Crimes by Hour and Day of Week',
                      xaxis_title='Hour',
                      yaxis_title='Number of Crimes',
                      xaxis=dict(tickmode='linear', tick0=0, dtick=1),
                      legend=dict(title='Day of Week'),
                      showlegend=True,
                      margin=dict(l=0, r=0, t=40, b=0))

    # show the plot
    return fig
