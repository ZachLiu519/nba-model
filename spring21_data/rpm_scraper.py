from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time, random

def scrape_rpm(years):
    
    bpms = []
    
    for year in years:
    
        url = 'http://www.espn.com/nba/statistics/rpm/_/year/{y}/page/'.format(y = year)
        html = urlopen(url)            
        soup = BeautifulSoup(html)
        page_num = int(soup.find_all(class_ = "page-numbers")[0].getText()[-2:])
        start, end = year - 2000, year - 2000 + 1

        for page in range(1, page_num+1):
            url = 'http://www.espn.com/nba/statistics/rpm/_/year/{y}/page/{p}'.format(y = year, p = page)
            html = urlopen(url)
            
            time.sleep(random.random()*10)
            
            soup = BeautifulSoup(html)
            rows = soup.findAll("tr")[1:]
            for row in rows:
                data = row.getText(separator=u' ').split(' ')
                i = data.index(",")
                name = ""
                for j in range(1, i):
                    name += data[j]
                    if j < i-1:
                        name += " "
                data = data[:1] + [name] + data[i+2:]
                data.append(name + "20{s}-{e}".format(s=start, e=end))
                bpms.append(data)
            print("success for page {p}".format(p = page))
        
        time.sleep(random.random()*15)
        print("success for year {y}".format(y = year))

    headers = soup.find_all(class_ = "colhead")[0].getText(separator=u' ').split(" ")
    headers.append("KEY")
    df = pd.DataFrame(bpms, columns=headers)
    return df

BPM_15_20 = scrape_rpm(list(range(2015, 2021)))
BPM_15_20.to_excel('BPM_15_20.xlsx')