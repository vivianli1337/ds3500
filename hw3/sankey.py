# import libraries
import pandas as pd
import plotly.graph_objects as go


# create sankey function
def make_sankey(df, source, target, value, title="Sankey Diagram"):
    """ generate a sankey diagram
    :param df: database
    :param source: column source
    :param target: column target
    :param value: column value
    :param title: default
    :return:
    """
    # ensure data types are correct
    df['Number of Incidents'] = pd.to_numeric(df['Number of Incidents'], errors='coerce')  # Convert to numeric
    
    # drop rows with missing values in 'Number of Incidents'
    df = df.dropna(subset=['Number of Incidents'])
    
    # find unique labels
    labels = pd.concat([df[source], df[target]]).unique()

    # mapping from label to integer
    label_to_id = {label: i for i, label in enumerate(labels)}
    
    # mapping dataframe columns to integers
    source_ids = df[source].map(label_to_id)
    target_ids = df[target].map(label_to_id)

    # creating the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source_ids,
            target=target_ids,
            value=df[value]
        ))])

    fig.update_layout(title_text=title, font_size=10)
    return fig
