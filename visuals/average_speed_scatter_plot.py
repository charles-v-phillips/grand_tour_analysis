import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.animation as ani
from matplotlib import pyplot as plt


all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')


avg_speed_giro = all_data[(all_data['race'] == 'giro-d-italia') & (all_data['edition'] > 1986)].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_tour = all_data[(all_data['race'] == 'tour-de-france')].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_vuelta = all_data[(all_data['race'] == 'vuelta-a-espana')].groupby('edition').mean()[['avg_speed_of_winner']]



ax = plt.axes()
ax.set_aspect(2)
ax.set_ylabel('Average Speed (kph)')
ax.set_xlabel('Year')
ax.spines['top'].set_alpha(0)
ax.spines['right'].set_alpha(0)
plt.grid(b=True, which='major', color='#666666', linestyle='-',alpha = .4)
ax.set_axisbelow(True)

plt.scatter(avg_speed_giro.index, avg_speed_giro.avg_speed_of_winner,color = '#fb9bbd',s = 8,label = 'giro')
plt.scatter(avg_speed_tour.index,avg_speed_tour.avg_speed_of_winner,color = '#f9db00',s = 8, label = 'tour')
plt.scatter(avg_speed_vuelta.index,avg_speed_vuelta.avg_speed_of_winner, color = 'red',s = 8,label = 'vuelta')


plt.legend(framealpha = 0)


plt.savefig('scatter_of_avg_speed.png',transparent = True)
# plt.show()
# ax.set_facecolor('white')








import seaborn as sns
sns.set_theme(style="whitegrid")


if __name__ == '__main__':
    pass