import streamlit as st
import requests
import pandas as pd

# NHL API Base URL
NHL_API_BASE_URL = "https://api-web.nhle.com/v1/"

# Helper Functions
def fetch_data(endpoint):
    """Fetch data from the NHL API."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def get_standings():
    """Retrieve current team standings."""
    return fetch_data("standings/now")

def get_team_roster(team_code):
    """Retrieve the current roster for a team."""
    return fetch_data(f"roster/{team_code}/current")

def get_team_stats(team_code):
    """Retrieve current stats for a team."""
    return fetch_data(f"club-stats/{team_code}/now")

# Streamlit App
st.title("NHL Teams, Rosters, and Stats")

# Fetch and display standings
st.header("Current Standings")
standings = get_standings()
if standings and "teams" in standings:
    for team in standings["teams"]:
        team_name = team["name"]
        team_code = team["abbreviation"]
        st.subheader(f"{team_name} ({team_code})")

        # Fetch and display team roster
        st.markdown("### Roster")
        roster = get_team_roster(team_code)
        if roster and "players" in roster:
            roster_data = [{
                "Name": f"{player['firstName']['default']} {player['lastName']['default']}",
                "Position": player["position"],
                "Sweater Number": player["sweaterNumber"]
            } for player in roster["players"]]
            st.dataframe(pd.DataFrame(roster_data))
        else:
            st.write("No roster data available.")

        # Fetch and display team stats
        st.markdown("### Team Stats")
        stats = get_team_stats(team_code)
        if stats:
            stats_data = stats.get("overallStats", {})
            st.write(f"**Wins:** {stats_data.get('wins', 'N/A')}")
            st.write(f"**Losses:** {stats_data.get('losses', 'N/A')}")
            st.write(f"**Points:** {stats_data.get('points', 'N/A')}")
        else:
            st.write("No stats data available.")
else:
    st.write("Standings data not available.")
