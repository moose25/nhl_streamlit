import streamlit as st
import requests
import pandas as pd

# NHL API Base URL
NHL_API_BASE_URL = "https://api.nhle.com/stats/rest/en/"

# Helper Functions
def fetch_data(endpoint, params=None):
    """Fetch data from the NHL API."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def get_teams():
    """Retrieve all NHL teams."""
    return fetch_data("team")

def get_team_roster(team_abbreviation):
    """Retrieve the current roster for a specific team."""
    endpoint = f"team/{team_abbreviation}/roster"
    return fetch_data(endpoint)

# Streamlit App
st.title("NHL Teams and Rosters")

# Fetch and display all teams
teams = get_teams()
if teams and "data" in teams:
    teams = teams["data"]
    for team in teams:
        team_name = team.get("fullName", "Unknown Team")
        team_abbreviation = team.get("abbreviation", "N/A")
        st.header(f"{team_name} ({team_abbreviation})")

        # Fetch and display team roster
        roster = get_team_roster(team_abbreviation)
        if roster and "roster" in roster:
            roster_data = [
                {
                    "Name": player.get("person", {}).get("fullName", "N/A"),
                    "Position": player.get("position", {}).get("abbreviation", "N/A"),
                    "Jersey Number": player.get("jerseyNumber", "N/A"),
                }
                for player in roster["roster"]
            ]
            st.dataframe(pd.DataFrame(roster_data))
        else:
            st.write("No roster data available.")
else:
    st.write("No teams available to display.")
