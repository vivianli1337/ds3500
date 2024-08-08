"""
Vivian Li
DS 3500 Advanced Programming
Prof. Rachlin
2/2/2024

file: sankey.py
description: create sankey function
"""
# import library
import plotly.graph_objects as go

def _code_mapping(df, src, tar):
    """ maps labels in src & tar to int
    :param df: input dataframe
    :param src: source col of labels
    :param tar: target col of labels

    """
    # get distinct labels
    labels = sorted(set(list(df[src]) + list(df[tar])), key=lambda x: str(x))

    # get int code
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for code in the df
    df = df.replace({src: lc_map, tar: lc_map})

    return df, labels


def make_sankey(df, *columns, val=None, threshold=20, **kwargs):
    """
    :param df: input dataframe
    :param columns: source & target col of labels
    :param val: thickness of link for each row
    :return:
    """
    # iterate through src, tar col
    for i in range(0, len(columns), 2):
        src, tar = columns[i], columns[i + 1]

        # initalize default thickness val
        if val:
            values = df[val]
        else:
            values = [1] * len(df)

        # code map for src & tar
        df, labels = _code_mapping(df, src, tar)

        # filter df based on threshold
        df = df[df[val] >= threshold]

        # customization
        line_color = kwargs.get('line_color', 'black')
        width = kwargs.get('width', 0)

        # define link & node dic
        link = {'source': df[src], 'target': df[tar], 'value': df[val],
                'line': {'color': line_color, 'width': width}}

        node = {'label': labels}

        # create sankey diagram
        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()

def main():
    print("hello from sankey library")

#
if __name__ == '__main__':
    main()