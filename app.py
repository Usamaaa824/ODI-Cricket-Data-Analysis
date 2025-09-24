import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ODI Cricket Data Analysis", layout="wide")
st.title("🏏 ODI Cricket Analysis ")

df = pd.read_csv('ODI_Match_info.csv')

# Matches per season

fig1 = px.histogram(df, x='season',title='Matches per season')

st.plotly_chart(fig1, use_container_width=True)

# Top 10 teams by win

top_teams = df['winner'].value_counts().reset_index().head(10)
top_teams.columns = ['Team', 'Wins']

fig2 = px.bar(top_teams,
             x="Team", y="Wins",
             labels={'Team': 'Team', 'Wins': 'Wins'},
             title="Top 10 Teams by Wins")

st.plotly_chart(fig2, use_container_width=True)

#Toss Decision Distribution (Bat vs Field)

fig3 = px.pie(df, names="toss_decision", title="Toss Decision Distribution (Bat vs Field)")

st.plotly_chart(fig3, use_container_width=True)


# Top 10 Player of the Match Winners

top_players = df['player_of_match'].value_counts().reset_index().head(10)
top_players.columns = ['Player', 'Awards']

fig4 = px.bar(top_players,
             x="Player", y="Awards",
             labels={'Player': 'Player', 'Awards': 'Awards'},
             title="Top 10 Player of the Match Winners")

st.plotly_chart(fig4, use_container_width=True)


# Top 15 Venues by Matches

venue_counts = df['venue'].value_counts().reset_index().head(15)
venue_counts.columns = ['Venue', 'Matches']

fig5 = px.bar(venue_counts,
             x="Venue", y="Matches",
             labels={'Venue': 'Venue', 'Matches': 'Matches'},
             title="Top 15 Venues by Matches")

st.plotly_chart(fig5, use_container_width=True)

# Matches Played per Year

df['date'] = pd.to_datetime(df['date'])   # convert date
df['year'] = df['date'].dt.year

fig6 = px.line(df.groupby("year").size().reset_index(name="matches"),
              x="year", y="matches",
              title="Matches Played per Year")

st.plotly_chart(fig6, use_container_width=True)



fig7 = px.histogram(df, x="win_by_runs", nbins=50,
                   title="Distribution of Wins by Runs")
st.plotly_chart(fig7, use_container_width=True)

fig8 = px.histogram(df, x="win_by_wickets", nbins=10,
                   title="Distribution of Wins by Wickets")
st.plotly_chart(fig8, use_container_width=True)



wins_by_city = df.groupby(["city", "winner"]).size().reset_index(name="wins")

fig9 = px.density_heatmap(wins_by_city, x="city", y="winner", z="wins",
                         color_continuous_scale="Blues",
                         title="Teams Winning at Different Cities")

st.plotly_chart(fig9, use_container_width=True)


st.subheader("Stats & Insights")


tosses = df['toss_winner'].value_counts().reset_index()
tosses.columns = ['team', 'toss_wins']

fig10 = px.bar(tosses, x="team", y="toss_wins",
             title="Total Toss Wins per Country",
             labels={"team": "Country", "toss_wins": "Toss Wins"})

st.plotly_chart(fig10, use_container_width=True)


matches_played = df['team1'].value_counts() + df['team2'].value_counts()
tosses_won = df['toss_winner'].value_counts()

toss_win_pct = (tosses_won / matches_played * 100).reset_index()
toss_win_pct.columns = ['team', 'toss_win_percent']

fig11 = px.bar(toss_win_pct, x="team", y="toss_win_percent",
             title="Toss Win % per Country")

st.plotly_chart(fig11, use_container_width=True)


df['toss_win_match_win'] = df['toss_winner'] == df['winner']

toss_outcomes = df.groupby('toss_winner')['toss_win_match_win'].value_counts().unstack().fillna(0)

fig12 = px.bar(toss_outcomes, barmode='stack',
             title="Match Outcomes when Winning Toss",
             labels={'value': 'Matches'})

st.plotly_chart(fig12, use_container_width=True)

decision_outcomes = df.groupby(['toss_decision', 'toss_winner']).apply(
    lambda x: (x['winner'] == x['toss_winner']).mean()
).reset_index(name='win_rate')

fig13 = px.bar(decision_outcomes, x='toss_winner', y='win_rate',
             color='toss_decision', barmode='group',
             title="Win Rate: Batting First vs Bowling First after Toss")

st.plotly_chart(fig13, use_container_width=True)


special_countries = ["India", "Australia", "Pakistan"]
subset = df[df['toss_winner'].isin(special_countries)]

fig14 = px.histogram(subset, x="toss_winner", color="toss_decision",
                   title="Toss Decisions (Bat vs Field) - Special Countries",
                   barmode="stack")

st.plotly_chart(fig14, use_container_width=True)



df['year'] = pd.to_datetime(df['date']).dt.year

toss_yearly = df.groupby(['year', 'toss_winner']).size().reset_index(name='toss_wins')

fig15 = px.line(toss_yearly, x="year", y="toss_wins", color="toss_winner",
              title="Toss Wins per Year by Country")

st.plotly_chart(fig15, use_container_width=True)

