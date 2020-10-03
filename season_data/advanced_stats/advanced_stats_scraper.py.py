# -*- coding: utf-8 -*-
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import pandas as pd

seasons_df = pd.read_excel(io='years_nba.xlsx')
seasons_list = [row['seasons'] for index, row in seasons_df.iterrows()]

#slice seasons_list
seasons = [nba_season[0:4] for nba_season in seasons_list]

for nba_season in seasons:
    file_path_thistime = "./" + nba_season + "_advanced_stats.csv"
    client.players_advanced_season_totals(season_end_year=nba_season, output_type=OutputType.CSV, output_file_path=file_path_thistime)


