from bs4 import BeautifulSoup
import re
import requests
import datetime
import numpy as np
import csv

month_dict = {  'January' : 1,
                'February' : 2,
                'March' : 3,
                'April': 4,
                'May' : 5,
                'June' : 6,
                'July' : 7,
                'August' : 8,
                'September' : 9,
                'October' : 10,
                'November' :11,
                'December' : 12
                }

race_names = ['tour-de-france', 'vuelta-a-espana','giro-d-italia']

def make_soup(url):
    '''Take url and return Beautiful Soup Object'''
    request = requests.get(url)
    return BeautifulSoup(request.text,'html.parser')


def get_links_to_all_editions(race):
    '''Take race string and return a list of links to all editions of race'''
    soup = make_soup(f'https://www.procyclingstats.com/race/{race}')
    tags = soup.find_all('option', attrs = {'value': re.compile('race\/(tour-de-france|vuelta-a-espana|giro-d-italia)\/[\d]{4}$')})
    l = (['https://www.procyclingstats.com/{}'.format(tag.get('value')) for tag in tags][1:])[::-1]
    return l

def get_link_to_final_results_page(url):


    soup = make_soup(url)
    tag = soup.find('option', attrs={
        'value': re.compile('race/(tour-de-france|vuelta-a-espana|giro-d-italia)/[\d]{4}/gc.*')})

    a = 'https://www.procyclingstats.com/{}'.format(tag.get('value'))
    return a

def get_info(url):
    soup = make_soup(url)
    winner = soup.find('a', attrs={'href': re.compile('rider/.*-.*')})
    tables = soup.find_all('tbody')
    gc_table = tables[1]
    gc_winner = gc_table.find('a',attrs={'href': re.compile('rider/.*-.*')})
    if not gc_winner: return np.nan,np.nan,np.nan
    winner_weight = 0
    age_when_won = np.nan

    rider_page_soup = make_soup('https://www.procyclingstats.com/rider/{}'.format(gc_winner.get('href')))
    rider_summary = rider_page_soup.find('div', attrs={'class': 'rdr-info-cont'})
    p = re.compile(
        'birth: ([\d]+)(rd|nd|st|th) +(January|February|March|April|May|June|July|August|September|October|November|December) [\d]{4}')
    birth_date_match = p.search(rider_summary.text)
    if birth_date_match:
        day = int(rider_summary.contents[1])
        month = rider_summary.contents[3].split()[0]
        year = int(rider_summary.contents[3].split()[1])
        winner_birth_date = datetime.datetime(year, month_dict[month], day)
    else:
        winner_birth_date = np.nan


    weight_pattern = re.compile('Weight: [\d]{2} kg')

    weight_match = weight_pattern.search(rider_summary.text)
    if weight_match:
        weight_string = weight_match.group(0)
        weight_info = weight_string.split()
        weight = int(weight_info[1])
        winner_weight = weight
    else:
        winner_weight = np.nan

    date_string = soup.find(text=re.compile(
        '[\d]+ (January|February|March|April|May|June|July|August|September|October|November|December) +[\d]{4}'))
    stage_date = date_string.text.split()
    stage_date = list(map(lambda s: s.replace(',', ''), stage_date))
    stage_date = datetime.datetime(int(stage_date[2]), month_dict[stage_date[1]], int(stage_date[0]))

    if stage_date and winner_birth_date:
        age_when_won = round((stage_date - winner_birth_date).days/365,2)

    return age_when_won, winner_weight,stage_date.year






for race in race_names:
    f = open(f'{race}_gc_final_results_info.csv', 'w')
    writer = csv.writer(f)
    headers = ['race','year','edition', 'age', 'weight']
    print(f'-------------------- {race} --------------------')
    for i,edition in enumerate(get_links_to_all_editions(race),1):
        gc_results = get_link_to_final_results_page(edition)
        age,weight,year = get_info(gc_results)
        row = [race, year, i, age, weight]
        writer.writerow(row)

        print(f'----- {i}   {year}-----')
        print(f'AGE : {age}     WEIGHT : {weight}')
    f.close()



if __name__ == '__main__':
    pass