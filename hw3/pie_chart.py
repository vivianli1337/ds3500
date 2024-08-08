# import library
import plotly.graph_objects as go

def make_pie_chart(df):
    """
    Generate a pie chart showing the distribution of total number of incidents per county

    :param df: DataFrame containing the data with columns "Jurisdiction by Geography" and "Number of Incidents".
    :return: fig (go.Figure): Plotly figure object representing the pie chart.
    """
    # summing up total number of incidents for each county
    total_victims_per_county = df.groupby("Jurisdiction by Geography")["Number of Incidents"].sum().reset_index()

    # create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=total_victims_per_county["Jurisdiction by Geography"],
        values=total_victims_per_county["Number of Incidents"],
        hole=0.3  # Adding a hole in the middle to create a donut pie chart
    )])

    # update layout of the pie chart
    fig.update_traces(textinfo='percent+label')  # Adding percentage and label to each pie slice
    fig.update_layout(title_text="Total Number of Victims by County")  # Setting title of the pie chart

    return fig
