import pandas as pd
import numpy as np
"""Open All DataFiles and put them into all_data DataFrame"""
tour_data = pd.read_csv('data/tour-data.csv')
vuelta_data = pd.read_csv('data/vuelta-data.csv')
giro_data = pd.read_csv('data/giro-data.csv')
all_data = pd.concat([tour_data, vuelta_data, giro_data])



"""Cleaning Section"""

#Strip 'kph' from avg_speed and cast to float
extr = tour_data['avg_speed_of_winner'].str.extract('^ ([\d]+.[\d]*)', expand=False)
tour_data['avg_speed_of_winner'] = pd.to_numeric(extr)
tour_data['avg_speed_of_winner'] = pd.to_numeric(extr)

#Strip 'k' from distance and cast to float
extr = tour_data['distance'].str.extract('^  ([\d]+.[\d]*)', expand=False)
tour_data['distance'] = pd.to_numeric(extr)

#Strip 'k' from distance and cast to float
extr = all_data['avg_speed_of_winner'].str.extract('^ ([\d]+.[\d]*)', expand=False)
all_data['avg_speed_of_winner'] = pd.to_numeric(extr)
all_data['avg_speed_of_winner'] = pd.to_numeric(extr)


#Strip
extr = all_data['distance'].str.extract('^  ([\d]+.[\d]*)', expand=False)
all_data['distance'] = pd.to_numeric(extr)



extr = all_data['vertical_meters']
extr = extr.apply(lambda s : s.strip())
extr = extr.replace('',np.nan)
extr = extr.apply(lambda s : float(s))
all_data['vertical_meters'] = extr

all_data.to_csv('data/all_data.csv')


if __name__ == '__main__':
    pass