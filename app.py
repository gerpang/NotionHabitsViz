from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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
    data = u.get_saved_data(u.savefilepath)
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index).sort_values(ascending=True)
    df.tz_localize('GMT')
    return df


raw_df = get_data(refresh=True)
df = raw_df.copy()
min_date = min(raw_df.index)  # .strftime('%d%m%Y')
max_date = max(raw_df.index)  # .strftime('%d%m%Y')

habit_groups = pd.read_csv('data/habit_groups.csv', header=0)


def update_display_date():
    start_date = datetime.datetime.strftime(
        min(df.index), "%d %b %y")
    end_date = datetime.datetime.strftime(
        max(df.index), "%d %b %y")
    st.sidebar.info('Start: **%s** End: **%s**' % (start_date, end_date))


def df_filter_months(message, df):
    slider_1, slider_2 = st.slider(
        '%s' % (message),
        min(df.index.month), max(df.index.month),
        [min(df.index.month), max(df.index.month)],
        # len(df)-1, [0, len(df)-1],
        1)
    filtered_df = df.loc[(df.index.month >= slider_1) &
                         (df.index.month <= slider_2)]
    return filtered_df


def df_filter_month(df):
    min_month = min(df.index.month)
    max_month = max(df.index.month)
    month = st.selectbox(
        'Select a month to view', range(min_month, max_month+1))
    filtered_df = df[df.index.month == month]
    return filtered_df


# df = df_filter('Move sliders to filter dataframe', month_df)

# SIDEBAR
refresh_button = st.sidebar.button('Refresh the data')
if refresh_button:
    df = get_data(refresh=True)
view = st.sidebar.selectbox(
    'View by:', ['Year', 'Month-On-Month', 'Month Breakdown'])

st.header("Notion Habits Dashboard - {}".format(view))
if view == 'Year':
    st.write('IN PROGRESS')

elif view == 'Month-On-Month':
    df = df_filter_months('Select months to view', raw_df)
    update_display_date()
    # st.dataframe(df)

    st.subheader("Daily Overall Completion Rates")
    fig2 = go.Figure(data=go.Scatter(
        x=df.index, y=df.sum(axis=1)))
    st.plotly_chart(fig2)

    st.subheader("Habits by Month")
    month_fig = plt.figure(figsize=(12, 8))
    sns.heatmap(df.groupby(
        df.index.month).sum(), cmap='rocket_r', annot=True)
    st.pyplot(month_fig)
    st.write('Interactive:')
    st.plotly_chart(df.groupby(df.index.month).sum().plot.bar())

    st.subheader("Daily Completion by Month")
    df2 = pd.DataFrame(df.sum(axis=1))
    df2.index = pd.DatetimeIndex(df2.index)
    df2.columns = ['Completion']
    df2['Month'] = df2.index.month
    df2['Day'] = df2.index.day
    df2p = df2.pivot_table(values='Completion',
                           index='Day', columns='Month')
    sns.set(rc={'figure.figsize': (11.7, 8.27)})
    day_fig = plt.figure(figsize=(12, 8))
    sns.heatmap(df2p, cmap='rocket_r', annot=True)
    st.pyplot(day_fig)


elif view == 'Month Breakdown':
    df = df_filter_month(raw_df)
    update_display_date()

    # Overall
    # high score habit
    habits_total = (df.sum() /
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
        x=df.index, y=df.sum(axis=1)))
    # fig2.add_vrect(
    #     x0=month_ago, x1=today, fillcolor='LightSalmon', opacity=0.4, line_width=0, annotation_text='Past Month'
    # )
    st.plotly_chart(fig2)

    # Weekly completion rates
    st.subheader("Weekly Completion Rates by Habit")
    df_byweek = df.groupby(df.index.week).sum()  # 'Week').sum()
    fig3 = make_subplots(rows=3, cols=3)

    for index, row in habit_groups.iterrows():
        r = math.floor(index / 3) + 1
        c = index % 3 + 1
        col_byweek = df_byweek[row[1]]
        fig3.add_trace(go.Scatter(x=col_byweek.index,
                                  y=col_byweek, name=row[1]), row=r, col=c)

    st.write(fig3)
