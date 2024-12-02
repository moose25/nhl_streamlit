import streamlit as st
import requests
import pandas as pd

# NHL API Base URLs
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

def get_active_teams():
    """Retrieve active NHL teams with valid triCodes."""
    teams_data = fetch_data(NHL_STATS_API_BASE_URL, "team")
    if teams_data and "data" in teams_data:
        active_teams = [
            {
                "fullName": team.get("fullName", "Unknown Team"),
                "triCode": team.get("triCode", "N/A"),  # Use triCode for abbreviation
            }
            for team in teams_data["data"]
            if team.get("triCode") not in (None, "N/A")  # Filter valid triCodes
        ]
        return active_teams
    return []

def get_team_roster(team_code):
    """Retrieve the current roster for a specific team."""
    endpoint = f"roster/{team_code}/current"
    return fetch_data(NHL_WEB_API_BASE_URL, endpoint)

# Streamlit App
st.title("NHL Teams and Rosters")

# Fetch all teams
teams = get_active_teams()
if teams:
    for team in teams:
        team_name = team.get("fullName", "Unknown Team")
        team_code = team.get("triCode", "N/A")

        # Fetch team roster and only display if the roster exists
        if team_code != "N/A":
            roster = get_team_roster(team_code)
            if roster and "players" in roster:
                st.header(f"{team_name} ({team_code})")
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
                # Skip teams without rosters
                continue
else:
    st.write("No active teams available to display.")
