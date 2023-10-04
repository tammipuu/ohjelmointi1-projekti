import random
import story
# import sqlconfig
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    database='flight_game',
    user='root',
    password='salasana',
    autocommit=True
)


# FUNCTIONS

# select 30 airports for the game
def get_airports():
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
            FROM airport
            WHERE country IN ('VN', 'BD', 'IN', 'NP', 'CN', 'PH', 'MY', 'ID', 'FJ', 'CL', 'AR', 'BR', 'CR', 'JM', 'MX', 'US')
            AND type='large_airport'
            ORDER by RAND();"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


# get all goals
def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


# create new game
def create_game(start_money, p_range, cur_airport, p_name, a_ports):
    sql = "INSERT INTO game (money, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_money, p_range, cur_airport, p_name))
    g_id = cursor.lastrowid

    # add goals / loot boxes
    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    # exclude starting airport
    g_ports = a_ports[1:].copy()
    random.shuffle(g_ports)

    for i, goal_id in enumerate(goal_list):
        sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (g_id, g_ports[i]['ident'], goal_id))

    cursor.close()
    return g_id


# get airport info
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    cursor.close()
    return result


# check if airport has a goal
def check_goal(g_id, cur_airport):
    sql = f'''SELECT ports.id, goal, goal.id as goal_id, name, money 
    FROM ports 
    JOIN goal ON goal.id = ports.goal 
    WHERE game = %s 
    AND airport = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    cursor.close()
    return result


# calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


# get airports in range
def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range


# set loot box opened

# update location
def update_location(icao, p_range, u_money, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_money, g_id))
    cursor.close()


# Kysymykset ja vastaukset tallennetaan listaan

questions = [
    country_questions = 
    'Vietnam': { 'question': 'When did the Cold War start?"',
        'choices': ["A) 1914", "B) 1945", "C) 1950"],
        'correct_awnser':'B'
    },
    'Bangladesh': "question": "What was the primary ideological conflict of the Cold War?",
        "options": ["A) Capitalism vs. Imperialism", "B) Democracy vs. Monarchy", "C) Communism vs. Capitalism"],
        "correct_answer": "C"
    },
    'India': {"question": "What was the Warsaw Pact, and why was it formed?",
        "options": ["A) A military alliance of Eastern Bloc countries in response to NATO", "B) An economic alliance for trade purposes", "C) For fun"],
        "correct_answer": "A"
    },
    'Nepal': {"question": "Which event is marked as the beginning of the Cold War?",
        "options": ["A) The Korean war", "B) The dropping of atomic bombs on Hiroshima and Nagasaki.", "C) The Yalta conference"],
        "correct_answer": "B"    
    },
    'China': {"question": "What was the primary goal of the United Nations (UN) during the Cold War?",
        "options": ["A) Promotes economic competition between major powers", "B) To prevent the spread of nuclear weapons", "C) Maintaining international peace and security"],
        "correct_answer": "C"
    },
    'Philippines': {"question": "Which country served as the primary battleground for the proxy war between the United States and the Soviet Union during the Cold War?",
        "options": ["A) Korea", "B) Vietnam", "C) Cuba"],
        "correct_answer": "B"
    },
    'Malaysia': {"question": "Who were the major leaders of the United States and the Soviet Union during the Cold War?",
        "options": ["A) Ronald Reagan and Mikhail Gorbachev", "B) Donald Trump", "C) Vladimir Putin"],
        "correct_answer": "A"
    },
    'Indonesia': { "question": "What term is often used to describe the competition between the United States and the Soviet Union to achieve advancements in space exploration during the Cold War?",
        "options": ["A) Proxy war", "B) Space Race", "C) Nuclear Arms Race"],
        "correct_answer": "B"    
    },
    'Fiji': { "question": "What term is often used to describe the competition between the United States and the Soviet Union to achieve advancements in space exploration during the Cold War?",
        "options": ["A) Proxy war", "B) Space Race", "C) Nuclear Arms Race"],
        "correct_answer": "B"   
    },
    'Chile': { "question": "When did the war end?",
        "options": ["A) 1991", "B) 1992", "C) 1988"],
        "correct_answer": "A"
    },
    'Argentina': { "question": "Your fuel reserves are dangerously low. What’s your next move?",
        "options": {"A": "Prepare for a courageous landing.", "B": "Start panicking", "C": "Keep soaring through the skies."
        "correct_answer": "A",
    },
    'Brazil': { "question": "In this thrilling adventure, you notice that there is a fire on the aircraft’s wings. What’s your next move?",
        "options": { "A": "Put more fuel to the fire", "B": "Put water to calm the fire", "C": "Use Fire Extinguishers"
        "correct_answer": "C",
       '
    },
    'Costa rica': { "question": "Oh No! The weather is taking a turn for the worse and your fuel reserves are dangerously low. What’s your next move?",
        "options": {"A": "Grab a snack to refuel yourself.", "B": "Execute an emergency landing.", "C": "Harness the power of wind and ride along the storm."
        },
        "correct_answer": "B",'
    },
    'Jamaica': {"question": "As you gear up your journey, what items are you bringing along to reach your destination?",
        "options": {"A": "A laptop","B": "Vital supplies: Food, Map & Fuel","C": "Someone’s grandmother"
        },
        "correct_answer": "B",
    },
    'Mexico': {"question": "Looks like, on your adventurous journey, you encounter an unexpected fellow traveler who needs your aid. What do you do in the following situation?",
        "options": { "A": "Attack him and rob him.", "B": "Make a hasty escape","C": "Offer him assistance"   
         "correct_answer": "C",
    },
    'USA': { "question": "Rate this game (1-5):",
        "options": { "1": "1", "2": "2","3": "3","4": "4","5": "5"
        },



# Alustetaan pelaajan polttoaine
fuel_reserves = 10


def ask_question(question_data):
    print(question_data("question"))
    for option in question_data("options"):
        print(option)

    player_answer = input("Anna vastaus (A/B/C): ").upper()

    if player_answer == question_data("correct_answer"):
        print("Oikein! Saat 2x enemmän polttoainetta.")
        return True
    else:
        print("Väärin! Menetät polttoainetta.")
        return False

for question in questions:
    if ask_question(question):
        if question != questions[-1]:
            fuel_reserves *= 2
    else:
        fuel_reserves -= 1


# game starts
# ask to show the story
storyDialog = input('Do you want to read the background story? (Y/N): ')
if storyDialog == 'Y':
    # print wrapped string line by line
    for line in story.getStory():
        print(line)

# GAME SETTINGS
print('When you are ready to start, ')
player = input('type player name: ')
# boolean for game over and win
game_over = False
win = False

# start fuel = 1000
fuel = 1000
# start range in km = 2000
player_range = 2000

# score = 0
score = 0

# boolean for diamond found
diamond_found = False

# all airports
all_airports = get_airports()
# start_airport ident
start_airport = all_airports[0]['ident']

# current airport
current_airport = start_airport

# game id
game_id = create_game(money, player_range, start_airport, player, all_airports)

# GAME LOOP
while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show game status
    print(f'''You are at {airport['name']}.''')
    print(f'''You have {money:.0f}$ and {player_range:.0f}km of range.''')
    # pause
    input('\033[32mPress Enter to continue...\033[0m')
    # if airport has goal ask if player wants to open it
    # check goal type and add/subtract money accordingly
    goal = check_goal(game_id, current_airport)
    if goal:
        question = input(
            f'''Do you want to open lootbox for {"100$ or " if money > 100 else ""}{"50km range" if player_range > 50 else ""}? M = money, R = range, enter to skip: ''')
        if not question == '':
            if question == 'M':
                money -= 100
            elif question == 'R':
                player_range -= 50
            if goal['money'] > 0:
                money += goal['money']
                print(f'''Congratulations! You found {goal['name']}. That is worth {goal['money']}$.''')
                print(f'''You have now {money:.0f}$''')
            elif goal['money'] == 0:
                win = True
                print(f'''Congratulations! You found the diamond. Now go to start.''')
            else:
                money = 0
                print(f'''Oh no! You have been robbed. You lost all your money''')

    # pause
    input("\033[32mPress Enter to continue...\033[0m")

    # ask to buy fuel/range
    if money > 0:
        question2 = input('Do you want to by fuel? 1$ = 2km of range. Enter amount or press enter. ')
        if not question2 == '':
            question2 = float(question2)
            if question2 > money:
                print(f'''You don't have enough money.''')
            else:
                player_range += question2 * 2
                money -= question2
                print(f'''You have now {money:.0f}$ and {player_range:.0f}km of range''')
        # pause
        input("\033[32mPress Enter to continue...\033[0m")

    # if no range, game over
    # show airports in range. if none, game over
    airports = airports_in_range(current_airport, all_airports, player_range)
    print(f'''\033[34mThere are {len(airports)} airports in range: \033[0m''')
    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    else:
        print(f'''Airports: ''')
        for airport in airports:
            ap_distance = calculate_distance(current_airport, airport['ident'])
            print(f'''{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
        # ask for destination
        dest = input('Enter destination icao: ')
        selected_distance = calculate_distance(current_airport, dest)
        player_range -= selected_distance
        update_location(dest, player_range, money, game_id)
        current_airport = dest
        if player_range < 0:
            game_over = True
    # if diamond is found and player is at start, game is won
    if win and current_airport == start_airport:
        print(f'''You won! You have {money}$ and {player_range}km of range left.''')
        game_over = True


# if game is over loop stops
# show game result
print(f'''{'You won!' if win else 'You lost!'}''')
print(f'''You have {money:.0f}$''')
print(f'''Your range is {player_range:.0f}km''')
