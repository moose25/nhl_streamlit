import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# NHL API Base URL
NHL_API_BASE_URL = "https://statsapi.web.nhl.com/api/v1/"

def fetch_data(endpoint):
    """Fetch data from the NHL API with enhanced error handling."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        st.write(f"Attempting to fetch data from: {url}")  # Debug log
        response = requests.get(url, timeout=10, verify=False)  # Disable SSL temporarily
        st.write(f"Response Status: {response.status_code}")  # Debug log
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        st.error("Failed to connect to the NHL API. Please check your connection.")
    except Timeout:
        st.error("The request to the NHL API timed out. Please try again later.")
    except RequestException as e:
        st.error(f"Unexpected error occurred: {e}")
    return None


def get_teams():
    """Retrieve all NHL teams."""
    data = fetch_data("teams")
    if data and "teams" in data:
        return data["teams"]
    return []

def get_team_stats(team_id):
    """Retrieve statistics for a specific team."""
    data = fetch_data(f"teams/{team_id}/stats")
    if data and "stats" in data:
        return data["stats"]
    return []

def get_team_roster(team_id):
    """Retrieve the roster for a specific team."""
    data = fetch_data(f"teams/{team_id}/roster")
    if data and "roster" in data:
        return data["roster"]
    return []

def get_player_stats(player_id):
    """Retrieve statistics for a specific player."""
    data = fetch_data(f"people/{player_id}/stats?stats=statsSingleSeason")
    if data and "stats" in data and data["stats"]:
        return data["stats"][0].get("splits", [])
    return []

# Streamlit App Interface
st.title("NHL Teams & Player Stats")
st.write("Explore NHL teams, view their rosters, team stats, and player stats.")

# Fetch NHL teams
teams = get_teams()
if teams:
    team_names = [team["name"] for team in teams]

    # Dropdown to select a team
    selected_team = st.selectbox("Select a Team", team_names)
    if selected_team:
        # Get team ID and details
        team_id = next((team["id"] for team in teams if team["name"] == selected_team), None)

        if team_id:
            # Display Team Stats
            st.header(f"{selected_team} - Team Statistics")
            team_stats = get_team_stats(team_id)
            if team_stats:
                for stat in team_stats:
                    st.subheader(stat["type"]["displayName"])
                    for key, value in stat["splits"][0]["stat"].items():
                        st.write(f"{key.replace('_', ' ').title()}: {value}")
            else:
                st.write("No stats available for this team.")

            # Display Team Roster
            st.header(f"{selected_team} - Roster")
            roster = get_team_roster(team_id)
            if roster:
                player_names = [player["person"]["fullName"] for player in roster]
                selected_player = st.selectbox("Select a Player", player_names)

                if selected_player:
                    player_id = next((player["person"]["id"] for player in roster if player["person"]["fullName"] == selected_player), None)
                    
                    if player_id:
                        # Display Player Stats
                        st.header(f"{selected_player} - Player Statistics")
                        player_stats = get_player_stats(player_id)
                        if player_stats:
                            for stat in player_stats:
                                st.subheader(f"Season: {stat['season']}")
                                for key, value in stat["stat"].items():
                                    st.write(f"{key.replace('_', ' ').title()}: {value}")
                        else:
                            st.write("No statistics available for this player.")
                    else:
                        st.error("Player ID not found.")
            else:
                st.write("No roster available for this team.")
        else:
            st.error("Team ID not found.")
else:
    st.error("Failed to fetch NHL teams. Please try again later.")
