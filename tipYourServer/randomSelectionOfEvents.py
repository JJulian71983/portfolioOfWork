# My first Python project. Backend of a game I created to play with a friend that was a server. There are various random events to increase a servers tip. I wouldn't play this with someone you don't know.
import random as r


def bargame(mode):
    game_mode = mode
    random = round(r.random(), 2)
    dollar_amount = round((random * 5), 0)
    jackpot = 20
    fifty_percent = {"You win": dollar_amount}
    thirty_percent = {"Rub your belly and pat your head successfully for 15 seconds": 6, "Stand on one foot for 45 seconds for": 8, "Moonwalk like Michael and you'll be rewarded with": 8, "Share a fact about yourself that I didn't previously know for": 5,
                      "Name three State capitals you've not previously named for": 5, "Talk with an accent for": 6, "Play never have I ever for": 7, "Give a sincere compliment to a coworker for": 5, "Pull your best dance moves for": 9,
                      "Pick someone else\'s nose...LOL, just kidding, win for the hell of it": 5, "Tell me your favorite Disney character and why for": 5}
    ten_percent = {"Acknowledge that you're the best server in the joint and win a jackpot of": 10, "JACKPOT! YOU WON": jackpot, "Sing a song for 10 seconds and win": jackpot}
    one_percent = str(jackpot * 2)
    if game_mode == 1:
        if random >= 0.50:
            s_key = r.choice(list(fifty_percent.keys()))
            s_value = fifty_percent.get(s_key)
            print(s_key + " $" + str(s_value) + "!")
        elif 0.50 > random >= 0.20:
            s_key = r.choice(list(thirty_percent.keys()))
            s_value = thirty_percent.get(s_key)
            print(s_key + " $" + str(s_value) + "!")
        elif 0.20 > random >= 0.10:
            s_key = r.choice(list(ten_percent.keys()))
            s_value = ten_percent.get(s_key)
            print(s_key + " $" + str(s_value) + "!")
        elif 0.10 > random >= 0.02:
            print("You win a replay.")
        elif 0.02 > random >= 0.01:
            print("Double Jackpot of $" + one_percent)
        else:
            print("Better luck next time.")
    else:
        print("Error - Check game mode.")

bargame(1)
