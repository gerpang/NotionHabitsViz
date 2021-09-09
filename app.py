from plotly.subplots import make_subplots
import streamlit as st
from updater import Updater
import datetime 
import pandas as pd
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"

# load data
@st.cache
def get_data(refresh=False):
    u = Updater()
    if refresh:
        u.run()
    data = u.get_data(u.savefilepath)
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index).sort_values(ascending=True)
    df.tz_localize('GMT')
    df['Week'] = df.index.week
    return df

df = get_data(refresh=True)
min_date = min(df.index) #datetime.datetime.strptime(min(df.index), "%Y-%m-%d")
max_date = max(df.index) #datetime.datetime.strptime(max(df.index), "%Y-%m-%d")

habit_groups = {
    "Wellness": ['Reflect','Draw','8am'], 
    "Productivity": ['Code','Learn','Focus'], 
    "Health": ['Move','Train','Healthy Eating']
}

# dates = st.sidebar.slider('Select date period', 
# min_value=min_date, 
# max_value=max_date, 
today=datetime.datetime.now()
month_ago=today - datetime.timedelta(30)
# df_show = df[(df.index >= dates[0] )& (df.index <= dates[1])]

st.header("Notion Habits Dashboard")
refresh_button = st.button('Refresh the data')
if refresh_button:
    print('Refreshing data now')
    df = get_data(refresh=True)
st.markdown('There are **{}** days being viewed.'.format(len(df)))
# st.table(df.head())

### Overall 
# high score habit
habits_total = (df.drop('Week',axis=1).sum() / len(df)).sort_values(ascending=True).map('{:.0%}'.format)
st.subheader('Best Habit: {}'.format(habits_total.index[-1]))
fig1 = go.Figure(go.Bar(x=habits_total,y=habits_total.index, orientation='h', ))
st.plotly_chart(fig1)

### Daily Overall Completion Rates
st.subheader("Daily Overall Completion Rates")
fig2 = go.Figure(data=go.Scatter(x=df.index,y=df.drop('Week',axis=1).sum(axis=1)))
fig2.add_vrect(
    x0=month_ago, x1=today, fillcolor='LightSalmon', opacity=0.4, line_width=0, annotation_text='Past Month'
)
st.plotly_chart(fig2)


### Weekly completion rates 
st.subheader("Weekly Completion Rates by Habit")
st.text('Double click on any of the habits to view progress over the weeks.')
df_byweek = df.groupby('Week').sum()
st.write(df_byweek.plot())

### 
# fig3 = make_subplots(rows=3,cols=1)
# subfigs = [df_byweek[group_cols] for group_cols in habit_groups.values()] 

# for i, subfig in enumerate(subfigs):
#     fig3.add_trace(
#         subfig.plot(), row=i, col=1
#     )
#     # fig3.add_trace(
#     #     [go.Scatter(x=subfig.index,y=subfig[col]) for col in subfig], row=i,col=1
#     # )
# # fig3 = go.Figure(df_byweek.plot())
# st.write(fig3)