import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')


avg_speed_giro = all_data[(all_data['race'] == 'giro-d-italia') & (all_data['edition'] > 1986)].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_tour = all_data[(all_data['race'] == 'tour-de-france')].groupby('edition').mean()[['avg_speed_of_winner']]
avg_speed_vuelta = all_data[(all_data['race'] == 'vuelta-a-espana')].groupby('edition').mean()[['avg_speed_of_winner']]

avg_speed_of_each_edition = all_data.groupby(['race','edition'])[['avg_speed_of_winner']].mean()

print(avg_speed_giro.head())
# sns.relplot(data = avg_speed_of_each_edition,x = 'edition',y = 'avg_speed_of_winner',hue = 'race')
x_val = avg_speed_of_each_edition.loc['vuelta-a-espana']['avg_speed_of_winner']
y_val = avg_speed_of_each_edition.loc['tour-de-france']['avg_speed_of_winner']
sns.jointplot(x = x_val, y = y_val, kind = 'kde')
plt.show()

if __name__ == '__main__':
    pass