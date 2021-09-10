from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st
from updater import Updater
import datetime
import math
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


raw_df = get_data(refresh=True)
min_date = min(raw_df.index)  # .strftime('%d%m%Y')
max_date = max(raw_df.index)  # .strftime('%d%m%Y')

habit_groups = pd.read_csv('data/habit_groups.csv', header=0)


def update_info():
    start_date = datetime.datetime.strftime(
        min(df.index), "%d %b %y")
    end_date = datetime.datetime.strftime(
        max(df.index), "%d %b %y")
    st.sidebar.info('Start: **%s** End: **%s**' % (start_date, end_date))


# def df_filter(message, df):

#     df = df.reset_index()

#     slider_1, slider_2 = st.sidebar.slider(
#         '%s' % (message), 0, len(df)-1, [0, len(df)-1], 1)
#     filtered_df = df.loc[slider_1:slider_2+1]

#     filtered_df = filtered_df.set_index('index')

#     return filtered_df


def df_filter_month(df):
    min_month = min(df.index.month)
    max_month = max(df.index.month)
    month = st.sidebar.selectbox(
        'Select a month to view', range(min_month, max_month+1))
    filtered_df = df[df.index.month == month]
    return filtered_df


df = df_filter_month(raw_df)
# df = df_filter('Move sliders to filter dataframe', month_df)
update_info()
st.header("Notion Habits Dashboard")
refresh_button = st.button('Refresh the data')
if refresh_button:
    df = get_data(refresh=True)

# Overall
# high score habit
habits_total = (df.drop('Week', axis=1).sum() /
                len(df)).sort_values(ascending=True)
st.subheader('Best Habit: {}'.format(habits_total.index[-1]))
habits_df = pd.DataFrame(habits_total).reset_index()
habits_df.columns = ['Habit', '%Completion']
habits_df = habits_df.merge(habit_groups)
# fig1 = go.Figure(go.Bar(x=habits_total,y=habits_total.index, orientation='h', ))
fig1 = px.bar(habits_df, x='%Completion', y='Habit',
              color='Group', orientation='h')
fig1.update_traces(hovertemplate="%{x:.0%}")
fig1.update_layout(yaxis_categoryorder='total ascending')
st.plotly_chart(fig1)

# Daily Overall Completion Rates
st.subheader("Daily Overall Completion Rates")
fig2 = go.Figure(data=go.Scatter(
    x=df.index, y=df.drop('Week', axis=1).sum(axis=1)))
# fig2.add_vrect(
#     x0=month_ago, x1=today, fillcolor='LightSalmon', opacity=0.4, line_width=0, annotation_text='Past Month'
# )
st.plotly_chart(fig2)


# Weekly completion rates
st.subheader("Weekly Completion Rates by Habit")
df_byweek = df.groupby('Week').sum()
fig3 = make_subplots(rows=3, cols=3)

for index, row in habit_groups.iterrows():
    r = math.floor(index / 3) + 1
    c = index % 3 + 1
    col_byweek = df_byweek[row[1]]
    fig3.add_trace(go.Scatter(x=col_byweek.index,
                   y=col_byweek, name=row[1]), row=r, col=c)

st.write(fig3)
