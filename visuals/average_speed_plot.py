import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')

avg_speed_giro = all_data[(all_data['race'] == 'giro-d-italia') & (all_data['edition'] > 1986)].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_tour = all_data[(all_data['race'] == 'tour-de-france')].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_vuelta = all_data[(all_data['race'] == 'vuelta-a-espana')].groupby('edition').mean()[['avg_speed_of_winner']]


plt.grid(False)
# ax = plt.axes()
# ax.set_facecolor('white')

plt.plot(avg_speed_giro,color = '#fb9bbd')
plt.plot(avg_speed_tour,color = '#f9db00')
plt.plot(avg_speed_vuelta, color = 'red')

# plot = avg_speed_giro.plot(color = '#fb9bbd')


plt.show()

if __name__ == '__main__':
    pass