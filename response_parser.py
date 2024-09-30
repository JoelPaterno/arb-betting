from oddsapi import get_events
#parseing the json into objects, functions for finding useful information can be found in the Events Class
class Event:
    def __init__(self, id: str, sport_key: str, sport_title: str, commence_time: str, home_team: str, away_team: str, bookmakers: list):
        self.id = id
        self.sport_key = sport_key
        self.sport_title = sport_title
        self.commence_time = commence_time
        self.home_team = home_team
        self.away_team = away_team
        self.bookmakers = bookmakers

        self.best_home_odds = None
        self.best_away_odds = None
        self.best_home_bookmaker = None
        self.best_away_bookmaker = None
        self.away_lay = None
        self.home_lay = None
    def __repr__(self):
        return f"Event({self.id}, {self.sport_key}, {self.sport_title}, {self.commence_time}, {self.home_team}, {self.away_team}, {self.bookmakers})\n\n"
    def find_best_odds(self):
        for bookmaker in self.bookmakers:
            for market in bookmaker.markets:
                if market.key == "h2h":
                    home_outcome = market.outcomes[0]  # Assuming outcomes[0] is always home team
                    away_outcome = market.outcomes[1]  # Assuming outcomes[1] is always away team
                    
                    # Check and store best home team odds
                    if self.best_home_odds is None or home_outcome.price > self.best_home_odds:
                        self.best_home_odds = home_outcome.price
                        self.best_home_bookmaker = bookmaker.title
                    
                    # Check and store best away team odds
                    if self.best_away_odds is None or away_outcome.price > self.best_away_odds:
                        self.best_away_odds = away_outcome.price
                        self.best_away_bookmaker = bookmaker.title
                if market.key == "h2h_lay":
                    if self.home_lay is None:
                        self.home_lay = market.outcomes[0].price
                    if self.away_lay is None:
                        self.away_lay = market.outcomes[1].price

    def display_best_odds(self):
        """Displays the best odds for home and away teams."""
        print(f"\nBest Home Odds: {self.best_home_odds} for {self.home_team} (Bookmaker: {self.best_home_bookmaker}) (Betfair Lay : {self.home_lay})")
        print(f"Best Away Odds: {self.best_away_odds} for {self.away_team} (Bookmaker: {self.best_away_bookmaker}) (Betfair Lay : {self.away_lay})")
class Bookmaker:
    def __init__(self, key: str, title: str, last_update: str, markets: list):
        self.key = key
        self.title = title
        self.last_update = last_update
        self.markets = markets
    def __repr__(self):
        return f"Bookmaker({self.key}, {self.title}, {self.last_update}, {self.markets})\n"
    
class Market: 
    def __init__(self, key: str, last_update: str, outcomes: list):
        self.key = key
        self.last_update = last_update
        self.outcomes = outcomes
    def __repr__(self):
        return f"Market({self.key}, {self.last_update}, {self.outcomes})\n"

class Outcome:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    def __repr__(self):
        return f"Outcome({self.name}, {self.price})\n"
#functions to build the objects
def create_events(event_json: dict):
    return Event(event_json["id"], event_json["sport_key"], event_json["sport_title"], event_json["commence_time"], event_json["home_team"], event_json["away_team"], create_bookmakers(event_json["bookmakers"]))
def create_bookmakers(bookmaker_json: dict):
    return [Bookmaker(bookmaker["key"], bookmaker["title"], bookmaker["last_update"], create_markets(bookmaker["markets"])) for bookmaker in bookmaker_json]
def create_markets(market_json: dict):
    return [Market(market["key"], market["last_update"], create_outcomes(market["outcomes"])) for market in market_json]
def create_outcomes(outcome_json: dict):
    return [Outcome(outcome["name"], outcome["price"]) for outcome in outcome_json]
#this will parse the json sports events into python objects
sports = ["basketball_nba"]

response = get_events(sports)

nba_response = response[0]

nba_events = [create_events(event) for event in nba_response]

for event in nba_events:
    event.find_best_odds()
    event.display_best_odds()


    


