import requests
from dotenv import load_dotenv
import os
import telebot

load_dotenv()

ODDS_API_KEY = os.getenv("ODDS_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

apiKey = ODDS_API_KEY
regions = "au"
markets =  "h2h"


sports = requests.get(f"https://api.the-odds-api.com//v4/sports?apiKey={apiKey}")
sports_json = sports.json()
for sport in sports_json:
    print(sport["key"])

sport = input("Enter sport key: ")
# The API endpoint
url = f"https://api.the-odds-api.com//v4/sports//{sport}//odds//?apiKey={apiKey}&regions={regions}&markets={markets}"

# A GET request to the API
response = requests.get(url)

responses = response.json()

with open("responses.txt", "w") as f:
    f.write(str(responses))

for response in responses:
    print("\n\n")
    best_home_company = ""
    best_away_company = ""
    best_draw_company = ""
    best_home = 1
    best_away = 1
    best_draw = 1
    draw = False
    print("Home Team: " + response["home_team"])
    print("Away Team: " + response["away_team"])
    for bookmaker in response["bookmakers"]:
        print("Bookmaker: " + bookmaker["title"]) 
        for line in bookmaker["markets"]:
            n = len(line["outcomes"])
            if line['key'] == "h2h":
                if line["outcomes"][0]["price"] > best_home:
                    best_home_company = bookmaker["title"]
                    best_home = line["outcomes"][0]["price"]
                elif line["outcomes"][1]["price"] > best_away:
                    best_away_company = bookmaker["title"]
                    best_away = line["outcomes"][1]["price"]
                elif len(line["outcomes"]) == 3 and line["outcomes"][2]["price"] > best_draw:
                    draw = True
                    best_draw_company = bookmaker["title"]
                    best_draw = line["outcomes"][2]["price"]
                for i in range(n):
                    print(line["outcomes"][i]["name"] + " " + str(line["outcomes"][i]["price"]))
    
    print("\nBest Home: " + str(best_home) + " " + response["home_team"] + " To Win (" + best_home_company + ")")
    print("Best Away: " + str(best_away) + " " + response["away_team"] + " To Win (" + best_away_company + ")")
    print("\n")

    prob_home = (1/best_home) * 100
    prob_away = (1/best_away) * 100
    if draw:
        prob_draw = (1/best_draw) * 100
    print("Home probability: " + str(prob_home))
    print("Away probability: " + str(prob_away)) 
    if draw:   
        print("Draw probability: " + str(prob_draw))
    print("\nCombined Market Margin: " + str(prob_home + prob_away) + "\n")

    combined = prob_home + prob_away
    arbitrage = False
    overall_stake = 10000
    if combined < 100:
        arbitrage = True 
    if arbitrage:
        print("Arbitrage: YES\n\n")
        stakeA =  (overall_stake * prob_home) / combined
        stakeB =  (overall_stake * prob_away) / combined
        print("Overall Stake: " + str(overall_stake))
        print("Stake Home: " + str(stakeA))
        print("Stake Away: " + str(stakeB))
        print("Home win profit: +" + str( (stakeA * best_home) - overall_stake))
        print("Away win: +" + str((stakeB * best_away) - overall_stake))
    else:
        print("Arbitrage: NO\n\n")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['markets'])
def sign_handler(message):
    bot.reply_to(message)

#bot.infinity_polling()