import requests
from dotenv import load_dotenv
import os

load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

apiKey = ODDS_API_KEY
regions = "au"
markets =  "h2h"

def get_available_sports() -> list: 
    sports = requests.get(f"https://api.the-odds-api.com//v4/sports?apiKey={apiKey}")
    sports_json = sports.json()
    return sports_json

#this function will call the api and return the odds for the listed sports
def get_events(sports: list) -> list:
    responses = []
    # The API endpoint
    for sport in sports:
        url = f"https://api.the-odds-api.com//v4/sports//{sport}//odds//?apiKey={apiKey}&regions={regions}&markets={markets}"
        # A GET request to the API
        response = requests.get(url)

        responses.append(response.json())

    with open("responses.txt", "w") as f:
        f.write(str(responses))
    return responses

