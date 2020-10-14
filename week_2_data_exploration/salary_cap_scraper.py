import requests
from bs4 import BeautifulSoup
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

page = requests.get("https://basketball.realgm.com/nba/info/salary_cap")
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.findAll('table', {'class': 'basketball compact'})

salary_cap = soup.findAll('td', {'data-th': "Salary Cap"})
salary_caps = [int(locale.atof(i.get_text()[1:])) for i in salary_cap]
del salary_caps[42]

seasons = []
start = 1984
end = 2027
while end >= start:
    seasons.append(str(end) + "-" + str(end+1)[2:])
    end -= 1

print(seasons, len(seasons))
print(salary_caps, len(salary_caps))

df = pd.DataFrame({"season": seasons, "salary_cap": salary_caps})
df.to_excel('week_2_data_exploration/salary_caps.xlsx')