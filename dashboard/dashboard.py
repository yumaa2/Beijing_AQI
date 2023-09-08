from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit as st

def create_polusi_harian_df(df):
    polusi_harian_df = df
    polusi_harian_df = polusi_harian_df.reset_index()
    polusi_harian_df['date'] = polusi_harian_df['date'].dt.strftime('%Y-%m-%d')
    return polusi_harian_df

def create_avg_polusi_perminggu_df(df):
    avg_polusi_perminggu = df
    avg_polusi_perminggu['date'] = pd.to_datetime(avg_polusi_perminggu.date)
    avg_polusi_perminggu['date'] = avg_polusi_perminggu['date'].dt.strftime('%A')

    avg_polusi_perminggu_df = pd.concat([avg_polusi_perminggu.groupby(by = ['date', 'PM2_5_index']).agg({'PM2_5' : 'nunique'}).rename(columns={'PM2_5_index' : 'pollutan_index', 'PM2_5' : 'pollutan'}),
                      avg_polusi_perminggu.groupby(by = ['date', 'NO2_index']).agg({'NO2' : 'nunique'}).rename(columns={'NO2_index' : 'pollutan_index', 'NO2' : 'pollutan'}),
                      avg_polusi_perminggu.groupby(by = ['date', 'SO2_index']).agg({'SO2' : 'nunique'}).rename(columns={'SO2_index' : 'pollutan_index', 'SO2' : 'pollutan'}),
                      avg_polusi_perminggu.groupby(by = ['date', 'CO_index']).agg({'CO' : 'nunique'}).rename(columns={'CO_index' : 'pollutan_index', 'CO' : 'pollutan'}),
                      avg_polusi_perminggu.groupby(by = ['date', 'O3_index']).agg({'O3' : 'nunique'}).rename(columns={'O3_index' : 'pollutan_index', 'O3' : 'pollutan'}),
                      avg_polusi_perminggu.groupby(by = ['date', 'PM10_index']).agg({'PM10' : 'nunique'}).rename(columns={'PM10_index' : 'pollutan_index', 'PM10' : 'pollutan'})]).reset_index().rename(columns={
    'date':'day',
    'PM2_5_index':'pollutan_index',
    'pollutan':'polluted_days_count'})

    avg_polusi_perminggu_df = avg_polusi_perminggu_df.groupby(by=['day', 'pollutan_index']).agg({'polluted_days_count':'sum'}).reset_index()
    avg_polusi_perminggu_df['day'] = pd.Categorical(avg_polusi_perminggu_df['day'], ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    avg_polusi_perminggu_df.sort_values(by='day')

    d1_df = avg_polusi_perminggu_df[avg_polusi_perminggu_df.pollutan_index != 'Good']
    d2_df = d1_df[avg_polusi_perminggu_df.pollutan_index != 'Excellent']
    d3_df = d2_df[avg_polusi_perminggu_df.pollutan_index != 'Lightly Polluted']
    avg_polusi_perminggu_df = d3_df

    avg_polusi_perminggu_df = avg_polusi_perminggu_df.groupby(by= 'day').agg({
    'polluted_days_count' : 'sum'
    }).reset_index()

    return avg_polusi_perminggu_df

def create_distribusi_polusi_df(df):
    PM2_5_isum = df.groupby(by = 'PM2_5_index').agg({
    'PM2_5' : 'nunique'
    }).reset_index()
    PM2_5_isum.rename(columns={
        'PM2_5_index' : 'pollutan_index',
        'PM2_5' : 'days_count'}, inplace = True)

    PM10_isum = df.groupby(by = 'PM10_index').agg({
        'PM10' : 'nunique'
    }).reset_index()
    PM10_isum.rename(columns={
        'PM10_index' : 'pollutan_index',
        'PM10' : 'days_count'}, inplace = True)

    NO2_isum = df.groupby(by = 'NO2_index').agg({
        'NO2' : 'nunique'
    }).reset_index()
    NO2_isum.rename(columns={
        'NO2_index' : 'pollutan_index',
        'NO2' : 'days_count'}, inplace = True)

    SO2_isum = df.groupby(by = 'SO2_index').agg({
        'SO2' : 'nunique'
    }).reset_index()
    SO2_isum.rename(columns={
        'SO2_index' : 'pollutan_index',
        'SO2' : 'days_count'}, inplace = True)

    CO_isum = df.groupby(by = 'CO_index').agg({
        'CO' : 'nunique'
    }).reset_index()
    CO_isum.rename(columns={
        'CO_index' : 'pollutan_index',
        'CO' : 'days_count'}, inplace = True)

    O3_isum = df.groupby(by = 'O3_index').agg({
        'O3' : 'nunique'
    }).reset_index()
    O3_isum.rename(columns={
        'O3_index' : 'pollutan_index',
        'O3' : 'days_count'}, inplace = True)
    
    PM2_5_isum['pollutan'] = 'PM2.5'
    PM10_isum['pollutan'] = 'PM10'
    NO2_isum['pollutan'] = 'NO2'
    SO2_isum['pollutan'] = 'SO2'
    CO_isum['pollutan'] = 'CO'
    O3_isum['pollutan'] = 'O3'

    distribusi_polusi_df = pd.concat([PM2_5_isum, PM10_isum, NO2_isum, SO2_isum, CO_isum, O3_isum])
    return distribusi_polusi_df

#__________________________________________________
main_data_df = pd.read_csv('main_data.csv')
main_data_df.sort_values(by = 'date', inplace = True)
main_data_df.reset_index(inplace=True)
main_data_df['date'] = pd.to_datetime(main_data_df.date)
main_data_df.info()

#__________________________________________________
polusi_harian_df = create_polusi_harian_df(main_data_df)
avg_polusi_perminggu_df = create_avg_polusi_perminggu_df(main_data_df)
distribusi_polusi_df = create_distribusi_polusi_df(main_data_df)

#__________________________________________________
st.header('Beijing Polution')
st.subheader('Polusi Harian')

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'])

color_PM2_5 = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.PM2_5_index.tail(7)]
color_PM10 = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.PM10_index.tail(7)]
color_SO2 = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.SO2_index.tail(7)]
color_NO2 = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.NO2_index.tail(7)]
color_CO = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.CO_index.tail(7)]
color_O3 = ['green' if x == 'Excellent' else(
    'yellow' if x == 'Good' else(
        'orange' if x == 'Lightly Polluted' else(
            'red' if x == 'Moderately Polluted' else(
                'darkred' if x == 'Heavely Polluted' else 'purple')))) for x in polusi_harian_df.O3_index.tail(7)]

with tab1:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['PM2_5'],
    data = polusi_harian_df,
    ax = ax,
    palette = color_PM2_5
    )
    
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan PM2.5', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['PM10'],
    data = polusi_harian_df,
    palette = color_PM10,
    ax = ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan PM10', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['NO2'],
    data = polusi_harian_df,
    palette = color_NO2,
    ax = ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan NO2', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

with tab4:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['SO2'],
    data = polusi_harian_df,
    palette = color_SO2,
    ax = ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan SO2', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

with tab5:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['CO'],
    data = polusi_harian_df,
    palette = color_CO,
    ax = ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan CO', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

st.subheader('Distribusi Polusi Kota Beijing Berdasarkan Polutan dan Indeks AQI (Maret 2013 - Februari 2017)')
with tab6:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(
    x = polusi_harian_df['date'].tail(7),
    y = polusi_harian_df['O3'],
    data = polusi_harian_df,
    palette = color_O3,
    ax = ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Polutan 03', fontsize=15)
    ax.xaxis.set_tick_params()

    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'purple']
    labels = ['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted']
    legenda = [mpatches.Patch(color = colors[i], label = "{:s}".format(labels[i])) for i in range(len(labels))]
    fig.legend(handles = legenda, loc = 'upper right')

    st.pyplot(fig)

#________________________

tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(['Excellent', 'Good', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted', 'Severely Polluted'])

with tab12:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Severely Polluted'].sort_values(by = 'days_count', ascending = False), color = 'purple', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Severely Polluted' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)
with tab11:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Heavely Polluted'].sort_values(by = 'days_count', ascending = False), color = 'darkred', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Heavely Polluted' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)
with tab10:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Moderately Polluted'].sort_values(by = 'days_count', ascending = False), color = 'red', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Moderately Polluted' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)
with tab9:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Lightly Polluted'].sort_values(by = 'days_count', ascending = False), color = 'orange', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Lightly Polluted' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)
with tab8:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Good'].sort_values(by = 'days_count', ascending = False), color = 'yellow', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Good' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)
with tab7:
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x="days_count", y="pollutan", data = distribusi_polusi_df[distribusi_polusi_df.pollutan_index == 'Excellent'].sort_values(by = 'days_count', ascending = False), color = 'green', ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("'Excellent' Days Count", loc="center", fontsize=25)
    ax.tick_params(axis ='y', labelsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    st.pyplot(fig)

st.subheader('Hari dengan Tingkat Polusi Tinggi')
with st.container():
    fig = plt.figure(figsize=(10, 8))

    warna = ['grey', 'grey', 'grey', 'grey', 'red', 'red', 'darkred']

    sns.barplot(
        x = 'day',
        y = 'polluted_days_count',
        data = avg_polusi_perminggu_df,
        ci = None,
        palette = warna
    )
    plt.title('Moderately, Heavily, Severely Polluted Day Count SUM (2013 - 2017)', size = 20)

    st.pyplot(fig)

expander = st.expander("Apa yang harus dilakukan?")
expander.write("Gunakanlah masker setiap hari saat berpergian keluar di kota Beijing terutama pada hari Kamis, Jum'at dan Sabtu, karena pada hari tersebut tingkat polusinya sangat tinggi.")