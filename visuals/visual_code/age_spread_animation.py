import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.text import Text

#TELL alex about this tomorrow :: THIS LINE THROWS AN ERROR BUT NEXT ONE DOESNT ! THOUGHT I NEEDED ..
# all_data = pd.read_csv('../data/all_data.csv')

#THIS LINE WORKS IN INTELLIJ BUT NOT COMMAND LINE
# all_data = pd.read_csv('../data/all_data.csv')

all_data = pd.read_csv('/data/try_again2.csv')
a = all_data[['edition','second_age_when_won']].rename({'second_age_when_won' : 'age'},axis = 1)
b = all_data[['edition','winner_age_when_won']].rename({'winner_age_when_won' : 'age'},axis = 1)
c = all_data[['edition','third_age_when_won']].rename({'third_age_when_won' : 'age'},axis = 1)
all_data = pd.concat([a,b,c])

HIST_BINS = np.linspace(20, 40, 20)
data = all_data[all_data['edition'] < 1900]['age'].tolist()
n, _ = np.histogram(data, HIST_BINS)

def prepare_animation(bar_container,mean,std):
    def animate(frame_number):
        data = all_data[(all_data['edition'] < 1920 + 1*frame_number) & (all_data['edition'] > 1900 + 1 * frame_number)]['age']
        print()
        data_list = data.tolist()
        n, _ = np.histogram(data_list,HIST_BINS)
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count)

        mean.set_text('mean : {}'.format(round(data.mean(),1)))
        std.set_text('std : {}'.format(round(data.std(), 1)))

        return bar_container.patches

    return animate

sns.set_palette('deep')
fig, ax = plt.subplots()
ax.set_ylim(top=600)
ax.spines['top'].set_alpha(0)
ax.spines['right'].set_alpha(0)
ax.set_aspect(.03)


mean = ax.text(30,600,"mean : ")
std = ax.text(30,500,"std : ")

_, _, bar_container = ax.hist(data, HIST_BINS, alpha=.7)

ani = animation.FuncAnimation(fig, prepare_animation(bar_container,mean,std), repeat=True, blit=False,interval=150,frames=80)





plt.show()


if __name__ == '__main__':
    pass



