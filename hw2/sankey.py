"""
file: sankey.py
description: provide a wrapper that maps a df to a sankey diagram
"""
import plotly.graph_objects as go
# _ = hidden function - dont call directly


def _code_mapping(df, src, tar):
    """ maps labels in src & tar to int"""
    # list of items w/ no duplicates
    # sorted(set(list(bio['cancer']) + list(bio['gene'])))

    # get distinct labels
    labels = sorted(set(list(df[src]) + list(df[tar])))

    # get int code
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for code in the df
    df = df.replace({src: lc_map, tar: lc_map})

    return df, labels


def make_sankey(df, src, tar, val=None, **kwargs):
    """
    :param df: input dataframe
    :param src: source col of labels
    :param tar: target col of labels
    :param val: thickness of link for each row
    :return:
    """
    if val:
        values = df[val]
    else:
        values = [1] * len(df)

    df, labels = _code_mapping(df, src, tar)

    line_color = kwargs.get('line_color', 'black')
    width = kwargs.get('width', 0)
    link = {'source': df[src], 'target': df[tar], 'value': values,
            'line':{'color': line_color, 'width': width}}

    node = {'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    return fig


def show_sankey(df, src, tar, val=None, **kwargs):
    fig = make_sankey(df, src, tar, val, **kwargs)
    fig.show()


def main():
    print("hello from sankey library")

#
if __name__ == '__main__':
    main()