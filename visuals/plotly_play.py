import plotly.express as px
import pandas as pd
df = px.data.gapminder()

all_data = pd.read_csv('/Users/charlesphillips/nycdsa/project_1_pcs/data/try_again2.csv')
a = all_data[['edition','second_age_when_won']].rename({'second_age_when_won' : 'age'},axis = 1)
b = all_data[['edition','winner_age_when_won']].rename({'winner_age_when_won' : 'age'},axis = 1)
c = all_data[['edition','third_age_when_won']].rename({'third_age_when_won' : 'age'},axis = 1)
all_data = pd.concat([a,b,c])




fig = px.bar(df, x="continent", y="pop", color="continent",
  animation_frame="year", animation_group="country", range_y=[0,4000000000])
fig.show()

if __name__ == '__main__':
    pass