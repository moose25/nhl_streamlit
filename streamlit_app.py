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

def get_teams():
    """Fetch all NHL teams."""
    standings = fetch_data("standings/now")
    if standings and "teams" in standings:
        return standings["teams"]
    else:
        st.error("No team data available.")
        return []

def get_team_roster(team_code):
    """Fetch the roster for a given team."""
    return fetch_data(f"roster/{team_code}/current")

# Streamlit App
st.title("NHL Teams and Rosters")

teams = get_teams()
if teams:
    for team in teams:
        # Display team information
        team_name = team.get("name", "Unknown Team")
        team_code = team.get("abbreviation", "N/A")
        st.header(f"{team_name} ({team_code})")

        # Fetch and display roster
        roster = get_team_roster(team_code)
        if roster and "players" in roster:
            roster_data = [
                {
                    "Name": f"{player['firstName']['default']} {player['lastName']['default']}",
                    "Position": player.get("position", "N/A"),
                    "Sweater Number": player.get("sweaterNumber", "N/A")
                }
                for player in roster["players"]
            ]
            st.dataframe(pd.DataFrame(roster_data))
        else:
            st.write("No roster data available.")
else:
    st.write("No teams available to display.")
