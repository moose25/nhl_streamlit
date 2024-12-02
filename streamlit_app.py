import streamlit as st
import requests
import pandas as pd

# NHL API Base URLs
NHL_WEB_API_BASE_URL = "https://api-web.nhle.com/v1/"

# Active Teams Based on triCode
ACTIVE_TEAMS = [
    "ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL",
    "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR",
    "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "VAN", "VGK",
    "WPG", "WSH"
]

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

def get_team_roster(team_code):
    """Retrieve the current roster for a specific team."""
    endpoint = f"roster/{team_code}/current"
    return fetch_data(NHL_WEB_API_BASE_URL, endpoint)

# Streamlit App
st.title("NHL Teams and Rosters")

# Fetch and display rosters for active teams
for team_code in ACTIVE_TEAMS:
    roster = get_team_roster(team_code)
    if roster and "players" in roster:
        st.header(f"Roster for {team_code}")
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
        st.write(f"{team_code}: No roster data available.")
