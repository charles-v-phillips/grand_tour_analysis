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

# returns soup object
def make_soup(url):
    '''Take url and return Beautiful Soup Object'''
    request = requests.get(url)
    return BeautifulSoup(request.text,'html.parser')



race_names = ['milano-sanremo', 'amstel-gold-race','liege-bastogne-liege','il-lombardia','la-fleche-wallone','paris-roubaix']




'(milano-sanremo|amstel-gold-race|tirreno-adriatico|liege-bastogne-liege|il-lombardia|la-fleche-wallone)'

def get_links_to_all_editions(race):
    '''Take race string and return a list of links to all editions of race'''
    soup = make_soup(f'https://www.procyclingstats.com/race/{race}')
    tags = soup.find_all('option', attrs = {'value': re.compile('race\/(milano-sanremo|amstel-gold-race|tirreno-adriatico|liege-bastogne-liege|il-lombardia|la-fleche-wallone|paris-roubaix)\/[\d]{4}$')})
    l = (['https://www.procyclingstats.com/{}'.format(tag.get('value')) for tag in tags][1:])[::-1]
    return l

def get_top_3(url):
    soup = make_soup(url)
    ages = []
    weights = []
    winners = soup.find_all('a', attrs={'href': re.compile('rider/.*-.*')})[:3]
    for tag in winners:
        rider_page_soup = make_soup('https://www.procyclingstats.com/rider/{}'.format(tag.get('href')))
        rider_summary = rider_page_soup.find('div', attrs={'class': 'rdr-info-cont'})
        p = re.compile(
            'birth: ([\d]+)(rd|nd|st|th) +(January|February|March|April|May|June|July|August|September|October|November|December) [\d]{4}')
        birth_date_match = p.search(rider_summary.text)
        if birth_date_match:
            day = int(rider_summary.contents[1])
            month = rider_summary.contents[3].split()[0]
            year = int(rider_summary.contents[3].split()[1])
            ages.append(datetime.datetime(year, month_dict[month], day))
        else:
            ages.append(np.nan)


        weight_pattern = re.compile('Weight: [\d]{2} kg')

        weight_match = weight_pattern.search(rider_summary.text)
        if weight_match:
            weight_string = weight_match.group(0)
            weight_info = weight_string.split()
            weight = int(weight_info[1])
            weights.append(weight)
        else:
            weights.append(np.nan)





    date_string = soup.find(text = re.compile('[\d]+ (January|February|March|April|May|June|July|August|September|October|November|December) +[\d]{4}'))
    stage_date = date_string.text.split()
    stage_date = list(map(lambda s : s.replace(',',''),stage_date))
    date = datetime.datetime(int(stage_date[2]), month_dict[stage_date[1]], int(stage_date[0]))

    ages = [round((date - age).days/365,2) if isinstance(age,datetime.datetime) else age for age in ages]
    return ages, date.year, weights

for race in race_names:
    f = open(f'{race}.csv','w')
    writer = csv.writer(f)
    headers = ['race','year', 'edition', 'first_age', 'second_age', 'third_age','first_weight','second_weight','third_weight']
    writer.writerow(headers)

    print('-'*70 + f'{race}' + '-'*70)
    for i,edition in enumerate(get_links_to_all_editions(race),1):

        ages,year,weights = get_top_3(edition)
        print(f'{i} + ------ + {year}')
        row = [race,year,i]
        row.extend(ages)
        row.extend(weights)
        writer.writerow(row)
    f.close()












if __name__ == '__main__':
    pass