# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Import data
df = pd.read_csv('NBALineup2023.csv')

# Set app configuration and title
st.set_page_config(layout = "wide")
st.title('NBA Lineup Analytics Tool')

# Team selection by user 
team = st.selectbox(
     'Choose Your Team:',
     df['team'].unique())

# Filter data based on the selected team 
df_team = df[df['team'] == team].reset_index(drop=True)

# Extract and display players
df_team['players_list'] = df_team['players_list'].str.replace(r"[\"\' \[\]]", '').str.split(',')
duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
roster = duplicate_roster.unique()

# Player selection
players = st.multiselect(
     'Select your players',
     roster,
     roster[0:5])


# Find the matching line up
df_lineup = df_team[df_team['players_list'].apply(lambda x: set(x)==set(players))]

df_important = df_lineup[['MIN', 'PLUS_MINUS','FG_PCT', 'FG3_PCT']]

# Display the dataframe
st.dataframe(df_important)

# Create columns and plot data
col1, col2, col3, col4 = st.columns(4)

with col1: 
    fig_min = px.histogram(df_team, x="MIN")
    fig_min.add_vline(x=df_important['MIN'].values[0],line_color='red')
    st.plotly_chart(fig_min, use_container_width=True)

with col2: 
    fig_2 = px.histogram(df_team, x="PLUS_MINUS")
    fig_2.add_vline(x=df_important['PLUS_MINUS'].values[0],line_color='red')
    st.plotly_chart(fig_2, use_container_width=True)
    
with col3: 
    fig_3 = px.histogram(df_team, x="FG_PCT")
    fig_3.add_vline(x=df_important['FG_PCT'].values[0],line_color='red')
    st.plotly_chart(fig_3, use_container_width=True)
    
with col4: 
    fig_4 = px.histogram(df_team, x="FG3_PCT")
    fig_4.add_vline(x=df_important['FG3_PCT'].values[0],line_color='red')
    st.plotly_chart(fig_4, use_container_width=True)
    

