# import library
import plotly.graph_objects as go


# function to create bar chart
def make_bar_chart(df):
    """ generate bar chart
    :param df: crime database
    :return:
    """
    bar_fig = go.Figure()

    # adding each gender for each county
    for gender in ["Female", "Male"]:
        df_filtered = df[df["Offender Gender"] == gender]
        bar_fig.add_trace(go.Bar(
            x=df_filtered["Jurisdiction by Geography"],
            y=df_filtered["Number of Incidents"],
            name=gender
        ))

    # update
    bar_fig.update_layout(
        barmode='group',
        title_text='Number of Incidents by County and Gender',
        xaxis_title="Jurisdiction by Geography",
        yaxis_title="Number of Incidents",
        legend_title="Offender Gender"
    )

    return bar_fig
