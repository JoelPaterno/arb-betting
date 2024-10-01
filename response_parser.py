from oddsapi import get_events, get_available_sports
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

        #Attributes to be set by class functions
        self.best_home_odds = None
        self.best_away_odds = None
        self.best_draw_odds = None
        self.best_home_bookmaker = None
        self.best_away_bookmaker = None
        self.best_draw_bokmaker = None
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
                    if len(market.outcomes) > 2:
                        draw_outcome = market.outcomes[2]  # Assuming outcomes[2] is always draw
                        if self.best_draw_odds is None or draw_outcome.price > self.best_draw_odds: 
                            self.best_draw_odds = draw_outcome.price
                            self.best_draw_bokmaker = bookmaker.title
                    # Check and store best home team odds
                    if self.best_home_odds is None or home_outcome.price > self.best_home_odds:
                        self.best_home_odds = home_outcome.price
                        self.best_home_bookmaker = bookmaker.title
                    # Check and store best away team odds
                    if self.best_away_odds is None or away_outcome.price > self.best_away_odds:
                        self.best_away_odds = away_outcome.price
                        self.best_away_bookmaker = bookmaker.title
                    # Check and store best draw odds
                    
                if market.key == "h2h_lay":
                    if self.home_lay is None:
                        self.home_lay = market.outcomes[0].price
                    if self.away_lay is None:
                        self.away_lay = market.outcomes[1].price
    def display_best_odds(self):
        """Displays the best odds for home and away teams."""
        print(f"\nBest Home Odds: {self.best_home_odds} for {self.home_team} (Bookmaker: {self.best_home_bookmaker})")
        print(f"Best Away Odds: {self.best_away_odds} for {self.away_team} (Bookmaker: {self.best_away_bookmaker})")
        print(f"Best Draw Odds: {self.best_draw_odds} (Bookmaker: {self.best_draw_bokmaker})")
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

class MatchedBettingCalculator:
    def __init__(self, event: Event, free_bet: float):
        self.event = event
        self.free_bet = free_bet
        self.commission = 0.05
        self.combined_prob = None
        self.home_odds = event.best_home_odds
        self.away_odds = event.best_away_odds
        self.draw_odds = event.best_draw_odds
        
        #attributes to be set by class functions
        try:
            self.home_prob = 1 / self.home_odds * 100
        except Exception as e:
            print("no home outcome")
        try:
            self.away_prob = 1 / self.away_odds * 100
        except Exception as e:
            print("no away outcome")
        try:
            self.draw_prob = 1 / self.draw_odds * 100
        except Exception as e:
            print("no draw outcome")
    def __repr__(self):
        return f"Matched Bet(Home: {self.home}, Free Bet: {self.free_bet}, Back Stake: {self.back_stake}, Lay Stake: {self.lay_stake}, Back Bet Odds: {self.back_bet_odds}, Lay Bet Odds: {self.lay_bet_odds})\n"

    def calc_combined_prob(self):
        if self.draw_odds is None:
            self.combined_prob = self.home_prob + self.away_prob
        else:
            self.combined_prob = self.home_prob + self.away_prob + self.draw_prob
    
    def display_combined_prob(self):
        if self.draw_odds is None:
            return print(f"Home Probability: {self.home_prob: 2f} -> Away Probability: {self.away_prob: 2f} -> Combined Probability: {self.combined_prob: 2f}")
        else:
            return print(f"Home Probability: {self.home_prob: 2f} -> Away Probability: {self.away_prob: 2f} -> Draw Probability: {self.draw_prob: 2f} -> Combined Probability: {self.combined_prob: 2f}")
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

sports_json = get_available_sports()
sports = [sport["key"] for sport in sports_json]
response = get_events(sports)

for sport_response in response:

    sport_events = [create_events(event) for event in sport_response]

    for event in sport_events:
        event.find_best_odds()
        
        calc = MatchedBettingCalculator(event, 100)
        calc.calc_combined_prob()
    
        if calc.combined_prob < 100 and calc.combined_prob > 20:
            event.display_best_odds()
            calc.display_combined_prob()
    
            


