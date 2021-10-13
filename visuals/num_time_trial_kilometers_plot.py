import pandas as pd
import matplotlib.pyplot as plt

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')
all_data.head()

tt_info_giro = all_data[(all_data['race'] == 'giro-d-italia') & (all_data['is_tt'] == 1)].groupby('edition').sum()[['distance']]
tt_info_tour = all_data[(all_data['race'] == 'tour-de-france') & (all_data['is_tt'] == 1)].groupby('edition').sum()[['distance']]
tt_info_vuelta = all_data[(all_data['race'] == 'vuelta-a-espana') & (all_data['is_tt'] == 1)].groupby('edition').sum()[['distance']]

ax = plt.axes()
ax.set_aspect(.1)
ax.set_ylabel('Time Trial Kilometers')
ax.set_xlabel('Year')
ax.spines['top'].set_alpha(0)
ax.spines['right'].set_alpha(0)




plt.scatter(tt_info_giro.index, tt_info_giro.distance, color = '#fb9bbd', s = 8, label = 'giro')
plt.scatter(tt_info_vuelta.index, tt_info_vuelta.distance,color = 'red', s = 8, label = 'vuelta')
plt.scatter(tt_info_tour.index, tt_info_tour.distance, color = '#f9db00', s = 8, label = 'tour')

plt.savefig('scatter_of_tt_kilometers.png',transparent = True)

if __name__ == '__main__':
    pass