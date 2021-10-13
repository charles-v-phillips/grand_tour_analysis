import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

#TELL alex about this tomorrow :: THIS LINE THROWS AN ERROR BUT NEXT ONE DOESNT ! THOUGHT I NEEDED ..
# all_data = pd.read_csv('../data/all_data.csv')

#THIS LINE WORKS IN INTELLIJ BUT NOT COMMAND LINE
# all_data = pd.read_csv('../data/all_data.csv')

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/all_data.csv')

HIST_BINS = np.linspace(20, 40, 40)
data = all_data[all_data['edition'] < 1900]['winner_age_when_won'].tolist()
n, _ = np.histogram(data, HIST_BINS)

def prepare_animation(bar_container):
    def animate(frame_number):
        data = all_data[(all_data['edition'] < 1960 + 2*frame_number) & (all_data['edition'] > 1900 + 2 * frame_number)]['winner_age_when_won'].tolist()
        n, _ = np.histogram(data,HIST_BINS)
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count)
        return bar_container.patches

    return animate


fig, ax = plt.subplots()
ax.set_ylim(top=350)
_, _, bar_container = ax.hist(data, HIST_BINS, alpha=.7)

ani = animation.FuncAnimation(fig, prepare_animation(bar_container), repeat=True, blit=True,interval=100,frames=80)

plt.show()

if __name__ == '__main__':
    pass



