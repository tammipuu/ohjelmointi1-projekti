import time
import random

player_money = 500
player_range_km = 500
screen_name = input("Enter your name: ")

# EU airport list example for the game
eu_airports = [
    "Split Airport, Split",
    "Munich Airport, Munich",
    "Dublin Airport, Dublin",
    "Malpensa Airport, Milan",
    "Valencia Airport, Valencia",
    "Côte d'Azur Airport, Cannes",
    "Edinburgh Airport, Edinburgh",
    "Lisbon Portela Airport, Lisbon"
    "Nice Côte d'Azur Airport, Nice",
    "Düsseldorf Airport, Düsseldorf",
    "Luxembourg Airport, Luxembourg",
    "Riga International Airport, Riga",
    "Tenerife South Airport, Tenerife",
    "Helsinki-Vantaa Airport, Helsinki",
    "Barcelona-El Prat Airport, Barcelona",
    "Athens International Airport, Athens",
    "Málaga-Costa del Sol Airport, Malaga",
    "Prague Václav Havel Airport, Prague",
    "Stockholm Arlanda Airport, Stockholm",
    "Kraków John Paul II International Airport, Krakow"
    "Budapest Ferenc Liszt International Airport, Budapest",
]
random.shuffle(eu_airports)


def introduction():
    global screen_name
    print(f"                               !Welcome, {screen_name}, to Time Travel Adventure!          ")
    time.sleep(1.5)
    print("Year 1919, the world was engulfed in chaos. There was no safe haven, and the roads were fraught with peril.")
    time.sleep(1.5)
    print(
        "As you wake up in this turbulent time, the world around you is a battlefield, a place of uncertainty and the lives of countless people are in grave danger")
    time.sleep(1.5)
    print(
        "The deafening sounds of artillery and gunfire echo in the distance. You initially think it's a dream, but reality soon sets in.")
    time.sleep(1.5)
    print("Beside you lies an unconscious soldiers, severely injured and in immediate need of medical attention.")
    time.sleep(1.5)
    print("As you sit up, you discover a mysterious letter and a map tucked away in your pocket. ")
    time.sleep(1.5)
    print("With trembling hands, you open the letter, its words explaining your incredible situation: ")


def part_1():
    global screen_name
    print("\nPart 1: The Letter")
    time.sleep(1.5)
    print(f"Greetings {screen_name}, the chosen Gurdian!")

    time.sleep(1.5)
    print("In a world on the brink of destruction, the fate of humanity rests in your hands as the chosen Gurdian.")
    time.sleep(1.5)
    print("You have always yearned for an adventurous life, and now you stand amid history's most turbulent moments.")
    time.sleep(1.5)
    print("However, after sleeping for thousands of years, you have finally been awakened to fulfill your destiny.")
    time.sleep(1.5)
    print("As the chosen Gurdian, you are called upon whenever the world faces its darkest hours.")
    time.sleep(1.5)
    print("Armed with unique abilities, you embark on a high-stakes journey through time and space.")
    time.sleep(1.5)
    print("Keep in mind that all your unique abilities have yet to awaken; you must complete the given mission first")
    time.sleep(1.5)
    print("The fate of this war hangs in the balance, but be cautious—your choices matter, and a misstep could trap you \nin this timeline forever, endangering not only your own existence but the soldier's life as well.!")
    time.sleep(1.5)
    print("Your mission is clear: safely bring the soldier to back home, ensuring the vital information he possesses reaches the right hands. ")


def part_2():
    global player_money, player_range_km, airport_current_location
    print("\nPart 2: The Mission\n")
    time.sleep(2)

    choice = input("Choose your vehicle for this adventurous journey: (1) The Mega Plane (2)The Heroic Aircraf: ")

    if choice == "1" or choice == "2":
        print("Excellent choice, adventurer! Let's begin!\n")
        player_money = 500
        player_range_km = 500
        player_fuel = 1000
        airport_current_location = random.choice(eu_airports)
        print(f"You are about to start your adventure at {airport_current_location} with 500$, and a range of {player_range_km} kilometers. ")
    else:
        print("Invalid choice. Please choose option (1) or option (2) to continue the game.\n")
        return


    print("With a deep breath, you ponder your next move. ")
    time.sleep(1.5)
    print("You realize that the key to success in this mission lies in your ability to gather money at each airport to continue your journey and play wisely.")
    time.sleep(1.5)
    print("As you navigate through various challenges at different airports, you learn to adapt and make crucial decisions that shape your journey")
    time.sleep(1.5)
    print("You uncover secrets, alliances, and hidden agendas within the government, and you start to question the true nature of your missions.")
    time.sleep(1.5)
    print("Do not fear- It is only going to get more intense!\n ")
    time.sleep(3)


    choice1 = input("Do you want to continue playing? (1) Continue (2) Quit ")
    if choice1 == "2":
        print("Thankyou for playing!")
        return

    print("Countdown to save humanity begins now!\n")



    choice2 = input("Mysterious letter as your guide, you set off on your journey, armed with the map and essential supplies,a critical warning \nflashes across your vehicle's control panel – your fuel levels are critically low, insufficient to reach your ultimate destination.\nWhat will you do? (1) Prepare for a courageous landing at the nearest airport. (2) Keep soaring through the skies: ")

    if choice2 == "1":
        print("You have made the right call adventurer! In dire situations, landing is often the safest option.\n")
        player_money += 500
        player_range_km += 600
        airport_current_location = random.choice(eu_airports)
        print(f"Fortune smiles on you! You have successfully landed at the {airport_current_location},\nand as a reward, you receive a valuable cache of rewards.Your journey continues!\n")


    elif choice2 == "2":
        print("Oh No! the plane's fate is sealed as it is speeding toward an unfortunate end...")
        print("Your plane crashes, and your adventure begins anew. ")
        player_money = 0
        player_range_km = 0
        return


    else:
        print("Invalid choice.")


    print(f"You now posses {player_money} and range of {player_range_km} kilometers!\n")
    time.sleep(1.5)

    choice3 = input("Danger!Danger! There is sudden fire on the aircraft’s wings. Act quickly!\n(1) Put more fuel to the fire (2) Initiate an emergency landing at the nearest airport: ")

    if choice3 == "2":
        print("You have made the right call adventurer! In dire situations, landing is often the safest option")
        player_money += 500
        player_range_km += 600
        airport_current_location = random.choice(eu_airports)
        print(f"You have successfully landed at the {airport_current_location},and as a reward, you receive a valuable cache of rewards.Your journey continues!\n")

    elif choice3 == "1":
        print("Oh No! Oh No! The situation worsens and the plane crashes....")
        player_money = 0
        player_range_km = 0
        return

    else:
        print("Invalid choice.")


    print(f"You now posses {player_money} and range of {player_range_km} kilometers!\n")
    time.sleep(2)

    choice4 = input("You encounter a group of people at an airport, offering to share their findings. Will you join their adventure?,\n(1) Decline their offer. (2) Join them: ")

    if choice4 == "1":
        print(" By not joining them, you avoid potential danger, stay commit to your crucial mission. ")
        player_money += 600
        player_range_km += 700
        airport_current_location = random.choice(eu_airports)
        print(f" You have successfully landed at the {airport_current_location},\nand as a reward, you receive a valuable cache of rewards.\n")


    elif choice4 == "2":
        print("Tragedy strikes! You have been robbed and the plane has been stolen, putting the soldiers' lives at risk to the end!")
        print("Unfortunately you have failed your mission, you are stuck in this timeline forever.")
        player_money = 0
        player_range_km = 0
        return


    else:
        print("Invalid choice.")


    print(f"You now posses {player_money} and range of {player_range_km} kilometers!\n")


    choice5 = input("The weather is taking a turn for the worse. What’s your next move?\n(1) Excuete an emergency landing at a safe airport. (2)Harness the power of wind and ride along the storm: ")

    if choice5 == "1":
        print("Amazing! It is wise to avoid treacherous weather and make an emergency landing.\n ")
        player_money += 999
        player_range_km += 2000
        airport_current_location = random.choice(eu_airports)


    elif choice5 == "2":
        print("The relentless force of the storm has damaged your aircraft beyond repair. You can't fly anymore!")
        player_money = 0
        player_range_km = 0
        return


    else:
        print("Invalid choice")


    print(f"You now posses {player_money} and range of {player_range_km} kilometers!\n")
    time.sleep(3)


    choice6 = input("You are running out of time and the war is getting out of hand.\nAs you continue your journey from last airport, you encounter a mysterious man.\nHe utters, trust me and hand over the soldier, I know him, I can safely take him home.\nWhat do you do? (1) Fly as fast as you can (2) Hand over the solider: ")

    if choice6 == "1":
        print("Amazing! You have avoided the biggest challenge ever! Now the final map of your destination will\n be handed over to you.\n ")
        player_money += 1000
        player_range_km += 20000
        airport_current_location = random.choice(eu_airports)


    elif choice6 == "2":
        print("Suddenly darkness takes over the world. You understand that you have been deceived.")
        player_money = 0
        player_range_km = 0
        return


    else:
        print("Invalid choice.")

    print(f"You now posses {player_money} and range of {player_range_km} kilometers!\n")


    print("Finally, after several missions filled with twists and turns, you successfully deliver the injured soldier \n and the critical information to the government, which ultimately plays a pivotal role in bringing the war to an end. ")
    time.sleep(1.5)
    print("You are given the opportunity to return home, but it's clear that your journey isn't over.")
    time.sleep(1.5)
    print("As you walk away from the battlefield of 1919, you wonder what the future holds for a time traveler like \nyourself and the mysterious person that sent you on these extraordinary adventures.")

def end():
    print(f"Thankyou for playing, {screen_name}")





if __name__ == "__main__":
    introduction()
    part_1()
    part_2()
    end()