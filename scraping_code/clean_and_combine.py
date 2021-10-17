import pandas as pd
import numpy as np


def combine_and_clean(f1,f2,f3,save_to_file):
    tour_data = pd.read_csv(f1)
    vuelta_data = pd.read_csv(f2)
    giro_data = pd.read_csv(f3)
    all_data = pd.concat([tour_data, vuelta_data, giro_data])


    # Strip 'k' from distance and cast to float
    extr = tour_data['distance'].str.extract('^  ([\d]+.[\d]*)', expand=False)
    tour_data['distance'] = pd.to_numeric(extr)

    # Strip 'kph' from distance and cast to float
    extr = all_data['avg_speed_of_winner'].str.extract('^ ([\d]+.[\d]*)', expand=False)
    all_data['avg_speed_of_winner'] = pd.to_numeric(extr)

    extr = all_data['vertical_meters']
    extr = extr.apply(lambda s: s.strip())
    extr = extr.replace('', np.nan)
    extr = extr.apply(lambda s: float(s))
    all_data['vertical_meters'] = extr

    indeces1 = all_data[all_data['winner_age_when_won'] < 10].index
    indeces2 = all_data[all_data['second_age_when_won'] < 10].index
    indeces3 = all_data[all_data['third_age_when_won'] < 10].index
    all_data.drop(indeces1, inplace=True)
    all_data.drop(indeces2, inplace=True)
    all_data.drop(indeces3, inplace=True)


    all_data.to_csv(save_to_file, index=False)



# """Open All DataFiles and put them into all_data DataFrame"""
# tour_data = pd.read_csv('data/tour-data.csv')
# vuelta_data = pd.read_csv('data/vuelta-data.csv')
# giro_data = pd.read_csv('data/giro-data.csv')
# all_data = pd.concat([tour_data, vuelta_data, giro_data])
#
#
#
# """Cleaning Section"""
#
# #Strip 'kph' from avg_speed and cast to float
# extr = tour_data['avg_speed_of_winner'].str.extract('^ ([\d]+.[\d]*)', expand=False)
# tour_data['avg_speed_of_winner'] = pd.to_numeric(extr)
# tour_data['avg_speed_of_winner'] = pd.to_numeric(extr)
#
# #Strip 'k' from distance and cast to float
# extr = tour_data['distance'].str.extract('^  ([\d]+.[\d]*)', expand=False)
# tour_data['distance'] = pd.to_numeric(extr)
#
# #Strip 'kph' from distance and cast to float
# extr = all_data['avg_speed_of_winner'].str.extract('^ ([\d]+.[\d]*)', expand=False)
# all_data['avg_speed_of_winner'] = pd.to_numeric(extr)
# all_data['avg_speed_of_winner'] = pd.to_numeric(extr)
#
#
# #Strip
# extr = all_data['distance'].str.extract('^  ([\d]+.[\d]*)', expand=False)
# all_data['distance'] = pd.to_numeric(extr)
#
#
#
# extr = all_data['vertical_meters']
# extr = extr.apply(lambda s : s.strip())
# extr = extr.replace('',np.nan)
# extr = extr.apply(lambda s : float(s))
# all_data['vertical_meters'] = extr
#
# all_data.to_csv('data/all_data.csv')

combine_and_clean('testing_giro.csv','testing_tour.csv','testing_vuelta.csv', '../data/try_again2.csv')

if __name__ == '__main__':
    pass