import streamlit as st
import requests

# NHL API Base URL
NHL_API_BASE_URL = "https://statsapi.web.nhl.com/api/v1/"

# Helper Functions
def fetch_teams():
    """Retrieve all NHL teams."""
    response = requests.get(f"{NHL_API_BASE_URL}teams")
    if response.status_code == 200:
        return response.json().get("teams", [])
    else:
        st.error("Failed to fetch teams.")
        return []

def fetch_team_stats(team_id):
    """Retrieve statistics for a specific team."""
    response = requests.get(f"{NHL_API_BASE_URL}teams/{team_id}/stats")
    if response.status_code == 200:
        return response.json().get("stats", [])
    else:
        st.error("Failed to fetch team stats.")
        return []

def fetch_team_roster(team_id):
    """Retrieve the roster for a specific team."""
    response = requests.get(f"{NHL_API_BASE_URL}teams/{team_id}/roster")
    if response.status_code == 200:
        return response.json().get("roster", [])
    else:
        st.error("Failed to fetch team roster.")
        return []

def fetch_player_stats(player_id):
    """Retrieve statistics for a specific player."""
    response = requests.get(f"{NHL_API_BASE_URL}people/{player_id}/stats?stats=statsSingleSeason")
    if response.status_code == 200:
        stats = response.json().get("stats", [])
        if stats:
            return stats[0].get("splits", [])
    else:
        st.error("Failed to fetch player stats.")
        return []

def fetch_team_injuries(team_id):
    """Retrieve injury reports for a specific team."""
    response = requests.get(f"{NHL_API_BASE_URL}teams/{team_id}?expand=team.roster,team.injuries")
    if response.status_code == 200:
        teams = response.json().get("teams", [])
        if teams:
            return teams[0].get("injuries", [])
    else:
        st.error("Failed to fetch team injuries.")
        return []

# Streamlit App Interface
st.title("NHL Teams & Player Statistics")

# Fetch and display teams
teams = fetch_teams()
team_names = [team["name"] for team in teams]
selected_team = st.selectbox("Select a Team", team_names)

if selected_team:
    team_id = next((team["id"] for team in teams if team["name"] == selected_team), None)
    
    if team_id:
        # Display Team Stats
        st.header(f"{selected_team} - Team Statistics")
        team_stats = fetch_team_stats(team_id)
        if team_stats:
            for stat in team_stats:
                st.subheader(stat["type"]["displayName"])
                for key, value in stat["splits"][0]["stat"].items():
                    st.write(f"{key.replace('_', ' ').title()}: {value}")

        # Display Team Injuries
        st.header(f"{selected_team} - Injury Report")
        injuries = fetch_team_injuries(team_id)
        if injuries:
            for injury in injuries:
                st.write(f"{injury['player']['fullName']}: {injury['description']}")
        else:
            st.write("No current injuries reported.")

        # Display Team Roster
        st.header(f"{selected_team} - Roster")
        roster = fetch_team_roster(team_id)
        player_names = [player["person"]["fullName"] for player in roster]
        selected_player = st.selectbox("Select a Player", player_names)

        if selected_player:
            player_id = next((player["person"]["id"] for player in roster if player["person"]["fullName"] == selected_player), None)
            
            if player_id:
                # Display Player Stats
                st.header(f"{selected_player} - Player Statistics")
                player_stats = fetch_player_stats(player_id)
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
        st.error("Team ID not found.")
