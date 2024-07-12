import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return None

def preprocess_data(df):
    df['players_list'] = df['players_list'].str.replace(r"[\"\' \[\]]", '').str.split(',')
    return df

def get_team_data(df, team):
    return df[df['team'] == team].reset_index(drop=True)

def get_roster(df_team):
    duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
    return duplicate_roster.unique()

def get_lineup(df_team, players):
    return df_team[df_team['players_list'].apply(lambda x: set(x) == set(players))]

def plot_histograms(df_team, df_important, columns):
    for col in columns:
        fig = px.histogram(df_team, x=col)
        fig.add_vline(x=df_important[col].values[0], line_color='red')
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(layout="wide")
    st.title('NBA Lineup Analytics Tool')
    
    df = load_data('NBALineup2023.csv')
    if df is None:
        return
    
    df = preprocess_data(df)
    
    team = st.selectbox('Choose Your Team:', df['team'].unique())
    df_team = get_team_data(df, team)
    roster = get_roster(df_team)
    
    players = st.multiselect('Select your players', roster, roster[0:5])
    
    if len(players) != 5:
        st.error("Please select exactly 5 players.")
        return
    
    df_lineup = get_lineup(df_team, players)
    if df_lineup.empty:
        st.error("No lineup found for the selected players.")
        return
    
    df_important = df_lineup[['MIN', 'PLUS_MINUS', 'FG_PCT', 'FG3_PCT']]
    st.dataframe(df_important)
    
    columns = ['MIN', 'PLUS_MINUS', 'FG_PCT', 'FG3_PCT']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1: 
        plot_histograms(df_team, df_important, [columns[0]])
    
    with col2: 
        plot_histograms(df_team, df_important, [columns[1]])
    
    with col3: 
        plot_histograms(df_team, df_important, [columns[2]])
    
    with col4: 
        plot_histograms(df_team, df_important, [columns[3]])

if __name__ == "__main__":
    main()
