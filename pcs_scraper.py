from bs4 import BeautifulSoup
import re
import requests
import datetime
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

#This function gets all the links to all editions of a grand tour
def get_links_to_all_editions(race):
    '''Take race string and return a list of links to all editions of race'''
    soup = make_soup(f'https://www.procyclingstats.com/race/{race}')
    tags = soup.find_all('option', attrs = {'value': re.compile('race\/(tour-de-france|vuelta-a-espana|giro-d-italia)\/[\d]{4}$')})
    l = (['https://www.procyclingstats.com/{}'.format(tag.get('value')) for tag in tags][1:])[::-1]
    return l



#This function gets all the links to all the stages of a particular grand tour
def get_links_to_all_stages_in_particular_edition(url):
    '''Takes edition url and returns list of links to add stages of particular edition'''
    soup = make_soup(url)
    tags = soup.find_all('option',attrs = {'value' : re.compile('race/(tour-de-france|vuelta-a-espana|giro-d-italia)/[\d]{4}/stage-[\d]*/.*')})
    return ['https://www.procyclingstats.com/{}'.format(tag.get('value')) for tag in tags]



def is_time_trial(soup):

    stage_label = soup.find('span', attrs = {'class' : 'blue'})
    # print(stage_label.text)
    if 'ITT' in  stage_label.text or 'TTT' in stage_label.text:
        return 1
    return 0




def get_info_on_particular_stage(url):
    soup = make_soup(url)
    blurb = scrape_blurb(soup) # returns list of info in the side blurb
    is_tt = is_time_trial(soup)
    #get winner and their present day age
    winner,winner_birth_date = get_stage_winner_and_age(soup)
    winners_ages = get_top_3(soup)
    stage_date = blurb[0].replace(',','').split()

    date_of_stage = datetime.datetime(int(stage_date[2]),month_dict[stage_date[1]],int(stage_date[0]))
    blurb[0] = date_of_stage
    #age of winner when they won the stage
    winner_age_when_won = None
    if winner and winner_birth_date : winner_age_when_won = round((date_of_stage - winner_birth_date).days/365,2) ## add this to return_dict
    rv = []
    for age in winners_ages:
        if age is None:
            rv.append(None)
        else:
            rv.append(round((date_of_stage - age).days/365,2))
    print(rv)



    blurb.append(winner)
    blurb.extend(rv)
    blurb.append(is_tt)


    return blurb







#this function scrapes the blurb off of stage result page and returns a dictionary
def scrape_blurb(soup):
    blurb = soup.find(attrs={"class": "w30 right mb_w100"})
    lines = blurb.text.split('\n')
    new_lines = list(filter(lambda s: ':' in s, lines))

    data = [l[1] for l in [l.split(':', 1) for l in new_lines] ]
    return data

def get_top_3(soup):
    ages = []
    winners = soup.find_all('a', attrs={'href': re.compile('rider/.*-.*')})[:3]
    for tag in winners:
        winner_name = None
        if tag:
            winner_name = tag.text

            rider_page_soup = make_soup('https://www.procyclingstats.com/rider/{}'.format(tag.get('href')))
            rider_summary = rider_page_soup.find('div', attrs={'class': 'rdr-info-cont'})

            p = re.compile('birth: ([\d]+)(rd|nd|st|th) +(January|February|March|April|May|June|July|August|September|October|November|December) [\d]{4}')
            birth_date_match = p.search(rider_summary.text)


            if birth_date_match:
                day = int(rider_summary.contents[1])
                month = rider_summary.contents[3].split()[0]
                year = int(rider_summary.contents[3].split()[1])
                ages.append(datetime.datetime(year,month_dict[month],day))
            else:
                ages.append(None)

    return ages





def get_stage_winner_and_age(soup):
    winner_tag = soup.find('a', attrs = {'href': re.compile('rider/.*-.*')})
    winner_name = None
    if winner_tag:
        winner_name = winner_tag.text


        rider_page_soup = make_soup('https://www.procyclingstats.com/rider/{}'.format(winner_tag.get('href')))
        rider_summary = rider_page_soup.find('div',attrs = {'class' : 'rdr-info-cont'})

        p = re.compile('birth: ([\d]+)(rd|nd|st|th) +(January|February|March|April|May|June|July|August|September|October|November|December) [\d]{4}')
        birth_date_match = p.search(rider_summary.text)




        if birth_date_match:
            day = int(rider_summary.contents[1])
            month = rider_summary.contents[3].split()[0]
            year = int(rider_summary.contents[3].split()[1])

            return winner_name, datetime.datetime(year,month_dict[month],day)
        return winner_name, None
    return None, None




def scrape_to_csv(race,save_to,starting_edition = 0):

    with open(save_to, 'w') as f:
        writer = csv.writer(f)
        headers = ['race', 'edition','stage','date','avg_speed_of_winner','race_category','distance','point_scale', 'parcour_type','profile_score', 'vertical_meters', 'departure', 'arrival','race_ranking', 'won_how','winner','winner_age_when_won','second_age_when_won','third_age_when_won','is_tt']
        writer.writerow(headers)
        for i, tour in enumerate(get_links_to_all_editions(race)[starting_edition:], 1):
            print(f'-------------- EDITION {i} --------------')
            for j, stage in enumerate(get_links_to_all_stages_in_particular_edition(tour), 1):
                print(f'----- stage {j} -----')
                info = get_info_on_particular_stage(stage)
                date = info[0]
                line = [race, date.year, j]
                line.extend(info)
                writer.writerow(line)



#scrape_to_csv('giro-d-italia','testing_giro.csv')
if __name__ == '__main__':
    pass