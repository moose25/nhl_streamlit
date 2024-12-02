import streamlit as st
import requests
import pandas as pd

# NHL API Base URL
NHL_WEB_API_BASE_URL = "https://api-web.nhle.com/v1/"

# Active NHL Teams
ACTIVE_TEAMS = [
    "ANA", "ARI", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL",
    "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR",
    "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "VAN", "VGK",
    "WPG", "WSH"
]

def fetch_data(endpoint):
    """Fetch data from the NHL API."""
    url = f"{NHL_WEB_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

def get_team_roster(team_code):
    """Retrieve the current roster for a specific team."""
    endpoint = f"roster/{team_code}/current"
    return fetch_data(endpoint)

def format_player_data(player):
    """Format player data for display."""
    return {
        "Name": f"{player['firstName']['default']} {player['lastName']['default']}",
        "Position": player.get("positionCode", "N/A"),
        "Jersey Number": player.get("sweaterNumber", "N/A"),
        "Height (cm)": player.get("heightInCentimeters", "N/A"),
        "Weight (kg)": player.get("weightInKilograms", "N/A"),
        "Birth Date": player.get("birthDate", "N/A"),
        "Birth City": player.get("birthCity", {}).get("default", "N/A"),
        "Birth Country": player.get("birthCountry", "N/A"),
    }

st.title("NHL Teams and Rosters")

# Fetch and display rosters for active teams
for team_code in ACTIVE_TEAMS:
    roster = get_team_roster(team_code)
    if roster:
        st.header(f"Roster for {team_code}")
        
        for category in ["forwards", "defensemen", "goalies"]:
            if category in roster and roster[category]:
                st.subheader(category.capitalize())
                players_data = [format_player_data(player) for player in roster[category]]
                st.dataframe(pd.DataFrame(players_data))
            else:
                st.write(f"No {category} data available.")
    else:
        st.write(f"{team_code}: No roster data available.")
