import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import pandas as pd

# NHL API Base URL
NHL_API_BASE_URL = "https://api-web.nhle.com/v1/"

# Headers (if required by the API)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Helper Functions
def fetch_data(endpoint, params=None):
    """Fetch data from the NHL API with error handling."""
    url = f"{NHL_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except ConnectionError:
        st.error("Failed to connect to the NHL API. Please check your connection.")
    except Timeout:
        st.error("The request to the NHL API timed out. Please try again later.")
    except RequestException as e:
        st.error(f"Unexpected error occurred: {e}")
    return None

def search_players_by_name(name):
    """Search for players by name."""
    endpoint = f"player/search/{name}"  # Update this endpoint based on actual API structure
    return fetch_data(endpoint)

def get_player_info(player_id):
    """Retrieve detailed information for a specific player."""
    endpoint = f"player/{player_id}/landing"
    return fetch_data(endpoint)

def display_player_info(player_info):
    """Format and display player information."""
    if not player_info:
        st.write("No player information available.")
        return

    st.image(player_info["headshot"], width=150, caption=f"{player_info['firstName']['default']} {player_info['lastName']['default']}")
    st.image(player_info["teamLogo"], width=100, caption=player_info["fullTeamName"]["default"])
    st.write(f"**Position:** {player_info['position']}")
    st.write(f"**Sweater Number:** {player_info['sweaterNumber']}")
    st.write(f"**Height:** {player_info['heightInInches']} in / {player_info['heightInCentimeters']} cm")
    st.write(f"**Weight:** {player_info['weightInPounds']} lbs / {player_info['weightInKilograms']} kg")
    st.write(f"**Birth Date:** {player_info['birthDate']}")
    st.write(f"**Birth Place:** {player_info['birthCity']['default']}, {player_info['birthStateProvince']['default']} ({player_info['birthCountry']})")
    st.write(f"**Shoots/Catches:** {player_info['shootsCatches']}")
    st.write("**Draft Details:**")
    st.write(f"- Year: {player_info['draftDetails']['year']}")
    st.write(f"- Team: {player_info['draftDetails']['teamAbbrev']}")
    st.write(f"- Round: {player_info['draftDetails']['round']}")
    st.write(f"- Pick: {player_info['draftDetails']['overallPick']}")
    st.markdown(f"**Career Highlights:**")
    career = player_info["careerTotals"]["regularSeason"]
    st.write(f"- Games Played: {career['gamesPlayed']}")
    st.write(f"- Goals: {career['goals']}")
    st.write(f"- Assists: {career['assists']}")
    st.write(f"- Points: {career['points']}")
    st.write(f"- Plus/Minus: {career['plusMinus']}")

    st.subheader("Last 5 Games")
    last5 = player_info["last5Games"]
    if last5:
        games_df = pd.DataFrame(last5)
        games_df = games_df.rename(columns={
            "gameDate": "Game Date",
            "teamAbbrev": "Team",
            "opponentAbbrev": "Opponent",
            "goals": "Goals",
            "assists": "Assists",
            "points": "Points",
            "toi": "Time on Ice",
        })
        st.dataframe(games_df[["Game Date", "Team", "Opponent", "Goals", "Assists", "Points", "Time on Ice"]])
    else:
        st.write("No recent games available.")

# Streamlit App Interface
st.title("NHL Player Lookup")
st.write("Search for NHL players by name and view detailed statistics.")

# Player Search Section
player_name = st.text_input("Enter Player Name")
if st.button("Search Player"):
    players = search_players_by_name(player_name)
    if players and "players" in players:
        player_list = players["players"]
        player_options = {f"{p['firstName']['default']} {p['lastName']['default']}": p["id"] for p in player_list}
        selected_player = st.selectbox("Select a Player", list(player_options.keys()))
        player_id = player_options[selected_player]
        player_info = get_player_info(player_id)
        display_player_info(player_info)
    else:
        st.write("No players found with that name.")

