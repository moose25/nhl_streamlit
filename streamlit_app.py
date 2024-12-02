import streamlit as st
import requests

# NHL API Endpoint
NHL_API_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/"

# Helper Functions
def get_teams():
    """Fetch all NHL teams."""
    response = requests.get(f"{NHL_API_ENDPOINT}teams")
    if response.status_code == 200:
        return response.json()["teams"]
    return []

def get_team_details(team_id):
    """Fetch team details, including stats and injuries."""
    response = requests.get(f"{NHL_API_ENDPOINT}teams/{team_id}?expand=team.stats")
    if response.status_code == 200:
        team = response.json()["teams"][0]
        return team
    return {}

def get_team_roster(team_id):
    """Fetch the roster of a team."""
    response = requests.get(f"{NHL_API_ENDPOINT}teams/{team_id}/roster")
    if response.status_code == 200:
        return response.json()["roster"]
    return []

def get_player_stats(player_id):
    """Fetch stats for a specific player."""
    response = requests.get(f"{NHL_API_ENDPOINT}people/{player_id}/stats?stats=statsSingleSeason")
    if response.status_code == 200:
        stats_data = response.json()
        if stats_data.get("stats"):
            return stats_data["stats"][0]["splits"]
    return []

# Streamlit App
st.title("NHL Teams & Player Stats")
st.write("Explore NHL teams, view their rosters, team stats, and player stats.")

# Fetch NHL teams
teams = get_teams()
team_names = [team["name"] for team in teams]

# Dropdown to select a team
selected_team = st.selectbox("Select a Team", team_names)
if selected_team:
    # Get team ID and details
    team_id = next(team["id"] for team in teams if team["name"] == selected_team)
    team_details = get_team_details(team_id)
    roster = get_team_roster(team_id)

    # Display Team Stats
    st.header(f"{selected_team} - Team Stats")
    if "teamStats" in team_details:
        for stats in team_details["teamStats"]:
            st.subheader(f"Stats for {stats['type']['displayName']}")
            for key, value in stats["splits"][0]["stat"].items():
                st.write(f"{key}: {value}")
    else:
        st.write("No stats available for this team.")

    # Display Roster
    st.subheader("Roster")
    player_names = [player["person"]["fullName"] for player in roster]
    selected_player = st.selectbox("Select a Player", player_names)

    # Display Player Stats
    if selected_player:
        player_id = next(player["person"]["id"] for player in roster if player["person"]["fullName"] == selected_player)
        player_stats = get_player_stats(player_id)

        st.header(f"{selected_player} - Player Stats")
        if player_stats:
            for stat in player_stats:
                st.subheader(f"Season: {stat['season']}")
                for key, value in stat["stat"].items():
                    st.write(f"{key}: {value}")
        else:
            st.write("No stats available for this player.")
