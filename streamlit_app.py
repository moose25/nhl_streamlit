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
    """Fetch data from the NHL API with enhanced error handling."""
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

def get_teams():
    """Fetch all NHL teams."""
    return fetch_data("teams")

def get_skater_stats_leaders(season, game_type, category=None, limit=5):
    """Retrieve skater stats leaders for a specific season and game type."""
    endpoint = f"skater-stats-leaders/{season}/{game_type}"
    params = {'categories': category, 'limit': limit}
    return fetch_data(endpoint, params)

def format_player_stats(players):
    """Format player stats into a table."""
    if not players:
        st.write("No player data available.")
        return

    player_data = []
    for player in players:
        player_data.append({
            "Player": f"{player['firstName']['default']} {player['lastName']['default']}",
            "Team": player['teamName']['default'],
            "Position": player['position'],
            "Goals": player['value'],
            "Number": player['sweaterNumber'],
            "Headshot": f"![]({player['headshot']})",
            "Team Logo": f"![]({player['teamLogo']})",
        })

    # Create a DataFrame and display it as Markdown
    df = pd.DataFrame(player_data)
    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

# Streamlit App Interface
st.title("NHL Stats Explorer")
st.write("Explore NHL teams, view their rosters, team stats, and player stats.")

# Teams Section
st.header("NHL Teams")
teams = get_teams()
if teams:
    for team in teams:
        st.subheader(team["name"])
        st.image(team["logo"], width=100)

# Player Stats Leaders Section
st.header("Player Stats Leaders")
season = st.text_input("Enter Season (YYYYYYYY format)", value="20222023")
game_type = st.selectbox("Select Game Type", options=[2, 3], format_func=lambda x: "Regular Season" if x == 2 else "Playoffs")
category = st.text_input("Enter Category (optional)", value="goals")
limit = st.number_input("Number of Results", min_value=1, max_value=50, value=5)

if st.button("Get Player Stats Leaders"):
    stats_leaders = get_skater_stats_leaders(season, game_type, category, limit)
    if stats_leaders and category in stats_leaders:
        format_player_stats(stats_leaders[category])
    else:
        st.write("No data found for the selected criteria.")

# Player Information
st.header("Player Information")
player_id = st.text_input("Enter Player ID", value="8478402")
if st.button("Get Player Info"):
    player_info = fetch_data(f"player/{player_id}/landing")
    if player_info:
        st.json(player_info)

# Player Game Log
st.header("Player Game Log")
if st.button("Get Player Game Log"):
    game_log = fetch_data(f"player/{player_id}/game-log/{season}/{game_type}")
    if game_log:
        st.json(game_log)
