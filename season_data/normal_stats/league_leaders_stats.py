#this file uses the nba_api to create and then concatenate dataframes of each seasons' league leaders for major statistics only
#import endpoints and necessary parameters for the api
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.library.parameters import PerMode48
import pandas as pd

#reads in seasons and formats as a list
seasons_df = pd.read_excel(io='years_nba.xlsx')
seasons_list = [row['seasons'] for index, row in seasons_df.iterrows()]

#obtain most recent year's league leaders data as pergame averages data
league_leaders_upto_2020_raw = leagueleaders.LeagueLeaders(per_mode48=PerMode48.per_game, season=seasons_list[0])
stats_upto_2020_df = league_leaders_upto_2020_raw.get_data_frames()[0]

#add column of year
num_rows = stats_upto_2020_df.shape[0]
year = [seasons_list[0]] * num_rows
stats_upto_2020_df['Year'] = year

#obtain each years' data, format as dataframe, and then concatenate with original dataframe
for nba_season in seasons_list:
    if nba_season == seasons_list[0]:
        continue
    stats_raw = leagueleaders.LeagueLeaders(per_mode48=PerMode48.per_game, season=nba_season)
    stats_df = stats_raw.get_data_frames()[0]

    num_rows = stats_df.shape[0]
    year = [nba_season] * num_rows
    stats_df['Year'] = year

    #finally, concatenate this year's dataframe with the master dataframe, established above
    frames = [stats_upto_2020_df, stats_df]
    stats_upto_2020_df = pd.concat(frames)

#write file to excel spreadsheet
writer = pd.ExcelWriter('nba_league_leaders_1985to2020.xlsx')
stats_upto_2020_df.to_excel(writer)
writer.save()
print("DataFrame is successfully written to the excel file")
