import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')

hist = sns.histplot(data = all_data, x = 'winner_age_when_won', kde = True)
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





plt.savefig('hist_of_age_of_winner.png',transparent = True)

if __name__ == '__main__':
    pass