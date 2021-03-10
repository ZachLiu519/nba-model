from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def scrape_allNBA_teams(team_type = 'league'):
    """
    Parameters
    ----------
    team_type : string, optional
        one of {'league', 'defense', 'rookie'}
        The default is ''league'

    Returns
    -------
    awards : DataFrame
        NBA All-NBA teams from the past 50 years

    """
    url='https://www.basketball-reference.com/awards/all_{0}.html'.format(team_type)

    html = urlopen(url)
    soup = BeautifulSoup(html)

    #get headers
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]


    #get data and convert for DataFrame
    rows = soup.findAll('tr')[1:]
    all_nba = [[th.getText() for th in rows[i].findAll('th')] + [td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    awards = pd.DataFrame(all_nba, columns = headers)

    return awards[awards[headers[0]].astype(bool)]

def scrape_FA(year):
    url = 'https://www.basketball-reference.com/friv/free_agents.cgi?year={0}'.format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    print(soup)

    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    print(headers)

    rows = soup.findAll('tr')[1:]
    rows = [row for row in rows if (not row.get('class'))]
    all_FA = [[th.getText() for th in row.findAll('th')] + [td.getText() for td in row.findAll('td')] for row in rows]
    FA = pd.DataFrame(all_FA, columns = headers)
    FA['end season'] = year
    
    return FA[FA[headers[0]].astype(bool)]
    
FA_last_5_years = pd.concat([scrape_FA(year=i) for i in range(2016, 2021)], axis=0)

FA_last_5_years.drop(columns = ['2015-16 Stats', '2016-17 Stats', '2017-18 Stats', '2018-19 Stats', '2019-20 Stats' ], inplace=True)

# FA_last_5_years.to_csv("free_agents_16to20.csv")

FA_last_5_years.to_excel('FA_16_20.xlsx')

    