import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/try_again2.csv')
ages = pd.concat([all_data['winner_age_when_won'],all_data['second_age_when_won'],all_data['third_age_when_won']])
# .reset_index(drop=True)
hist = sns.histplot(ages, kde = True, bins = 20)
sns.despine()

# ax = plt.axes()
# ax.set_ylabel('Count')
# ax.set_xlabel('Age of Stage Winner')
# ax.spines['top'].set_alpha(0)
# ax.spines['right'].set_alpha(0)

hist.set_xlabel('Age of Stage Winner')
hist.set_ylabel('Count')

# ax = hist.axes()
# ax.spines['top'].set_alpha(0)
# ax.spines['right'].set_alpha(0)



plt.show()

# plt.savefig('hist_of_age_of_winner.png',transparent = True)

if __name__ == '__main__':
    pass