"""
Vivian Li
DS 3500 Advanced Programming
Prof. Rachlin
2/2/2024

file: hw2_filter.py
description: create groupby df + filter columns
"""
def gb(df, src, tar, col):
    """
    :param df: input dataframe
    :param src: selected source column to groupby
    :param tar: selected target column to groupby
    :param col: name of new column
    :return:
    """
    # grouped by src + tar + filter missing info
    gb_df = df.groupby([src, tar]).size().reset_index(name=col)

    if src == src:
        gb_df = gb_df[gb_df[src] != 0]
        gb_df = gb_df[gb_df[src] != 'Nationality unknown']
        gb_df = gb_df[gb_df[src] != 'None']

    if tar == tar:
        gb_df = gb_df[gb_df[tar] != 0]
        gb_df = gb_df[gb_df[tar] != 'Nationality unknown']
        gb_df = gb_df[gb_df[tar] != 'None']

    return gb_df