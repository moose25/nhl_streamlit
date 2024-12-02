import streamlit as st
import requests
import pandas as pd

# NHL API Base URL
NHL_WEB_API_BASE_URL = "https://api-web.nhle.com/v1/"
NHL_STATS_API_BASE_URL = "https://api.nhle.com/stats/rest/en/"

# Helper Functions
def fetch_data(base_url, endpoint, params=None):
    """Fetch data from the NHL API."""
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def get_teams():
    """Retrieve all NHL teams."""
    return fetch_data(NHL_STATS_API_BASE_URL, "team")

def get_team_roster(team_abbreviation):
    """Retrieve the current roster for a specific team."""
    endpoint = f"roster/{team_abbreviation}/current"
    return fetch_data(NHL_WEB_API_BASE_URL, endpoint)

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
        if team_abbreviation != "N/A":
            roster = get_team_roster(team_abbreviation)
            if roster and "players" in roster:
                roster_data = [
                    {
                        "Name": f"{player['firstName']['default']} {player['lastName']['default']}",
                        "Position": player.get("position", "N/A"),
                        "Jersey Number": player.get("sweaterNumber", "N/A"),
                    }
                    for player in roster["players"]
                ]
                st.dataframe(pd.DataFrame(roster_data))
            else:
                st.write("No roster data available.")
        else:
            st.write("Invalid team abbreviation.")
else:
    st.write("No teams available to display.")
