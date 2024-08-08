"""Vivian Li
DS 3500 Advanced Programming
Prof. Rachlin
2/2/2024

file: hw2_artist.py
description: hw 2
"""
# import libraries
import hw2_sankey as sk
import pandas as pd
import hw2_filter as ft


def main():
    # load artist data w/ 3 columns
    artist = pd.read_json("/Users/vivianli/Documents/ds3500_24/project/pythonProject/hw2/artists.json")
    artist = artist[['Nationality', 'Gender', 'BeginDate']]

    # restore BeginDate as decade & standardize col values
    artist['BeginDate'] = artist['BeginDate'] // 10 * 10
    artist = artist.rename(columns={'BeginDate': 'Decade'})
    artist['Decade'] = artist['Decade'].astype(int)
    artist['Gender'] = artist['Gender'].str.lower()

    # grouped by nationality & decade w/ new col name "ArtistCount:
    nat_dec = ft. gb(artist, 'Nationality', 'Decade', 'ArtistCount')

    # create sankey diagram
    sk.make_sankey(nat_dec, 'Nationality', 'Decade', val='ArtistCount')

    # grouped by nationality & gender w/ new col name "ArtistCount:
    nat_gen = ft.gb(artist, 'Nationality', 'Gender', 'ArtistCount')

    # create sankey diagram
    sk.make_sankey(nat_gen, 'Nationality', 'Gender', val='ArtistCount')

    # grouped by gender & decade w/ new col name "ArtistCount:
    gen_dec = ft.gb(artist, 'Gender', 'Decade', 'ArtistCount')

    # create sankey diagram
    sk.make_sankey(gen_dec, 'Gender', 'Decade', val='ArtistCount')

    # stack df
    nat_gen.columns = ['src', 'tar', 'val']
    gen_dec.columns = ['src', 'tar', 'val']
    stacked = pd.concat([nat_gen, gen_dec], axis=0)

    # create sankey diagram
    sk.make_sankey(stacked, 'src', 'tar', val='val')

main()