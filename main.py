import story
import random
from geopy import distance
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='root',
    password='kirjoitasalasana',
    autocommit=True
)


# FUNCTIONS

import textwrap

story = ("Year 1975, near the end of the Vietnam War,\nyou wake up on an unfamiliar island in a different timeline, utterly perplexed.\n"
         "You initially think it's a dream, but reality soon sets in. You discover a mysterious letter and a map tucked away in your pocket.\n Beside you an unconscious soldier in immediate need of medical attention. To your surprise, this person seems oddly familiar.)\n"
         "As you open the letter, its words explain your incredible situation:\n  Greetings, intrepid traveler. You have traveled from the year 2030 and have been selected for a daring mission. You've always wished to meet your grandfather, a brave Cold War soldier, who's now severely injured. "
         "Your mission: safely bring your grandfather back home to the USA, as he holds critical information for the U.S. government.\n Yet, be cautious- your choices, matters, and a misstep could trap you here forever, endangering your grandfather's life."
         "With the letter as your guide, you set off your journey, armed with a map and essential supplies.\n Setting off from Vietnam Airport, you encounter yet another letter just before your departure: "
         "Welcome your mission begins here! Your first challenge emerges as a dire warning from the plane's controls: your fuel levels are dangerously low, insufficient to reach your goal destination. \n Your decision? Attempting your luck by answering the first question posed at the airport. Fortune smiles on you, granting you a valuable reward.\n"
         "You must continue your journey now, but you must be cautious with future challenges, as wrong answers can cost you dearly. Gathering money at each airport, until you reach your destination."
         "When you finally arrive at your destination and complete your mission successfully, you finally reunite with your grandfather once he regains consciousness. \n Your grandfather sends you back home and you wake up. It was a dream after all! ")



# select 30 airports for the game
def get_airports():
    sql = "SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE iso_country IN ('BD', 'IN', 'NP', 'CN', 'PH', 'MY', 'ID', 'FJ', 'CL', 'AR', 'BR', 'CR', 'JM', 'MX') AND type = 'large_airport' order by rand() limit 20;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
#tällä haetaan aloituskenttiä Vietnamista, mutta palautetaan vain yksi
def get_start_airport():
    sql = "SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE iso_country IN ('VN') AND type = 'large_airport' limit 5;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    #vaihtakaa numeroa vaihtaaksenne kenttää, jota voitte käyttää aloituksena
    return result[1]
#tällä haetaan kenttiä USA:sta, mutta palautetaan vain yksi niistä
def get_finish_airport():
    sql = "SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE iso_country IN ('US') AND type = 'large_airport' limit 5;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    #vaihdelkaa numeroa vaihtaaksenne kenttää, jota käytetään loppukenttän, jonne
    #halutaan päästä
    return result[1]

# get all goals
def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
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

    g_ports = a_ports[:].copy()
    #random.shuffle(g_ports)

    for i, goal_id in enumerate(goal_list):
        sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (g_id, g_ports[i]['ident'], goal_id))

    return g_id


# get airport info
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


# check if airport has a goal
def check_goal(g_id, cur_airport):
    sql = f'''SELECT ports.id, goal, question, answer, wrong_answer, wrong_answer2
    FROM ports
    JOIN goal ON goal.id = ports.goal
    WHERE ports.game = %s
    AND ports.airport = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
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
        #ile, lisätty tänne 'and a_port['ident'] not in visited:', koska
        #jo vierailtuihin kenttiin ei? voida matkustaa
        if dist <= p_range and not dist == 0 and a_port['ident'] not in visited:
            in_range.append(a_port)
    return in_range


# set loot box opened

# update location
def update_location(icao, p_range, u_money, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_money, g_id))




#ilen koodi

def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def get_answer():
    user = 0
    # kysytään
    while user == 0:
        user = input('Enter you answer here: ').upper()
        if is_int(user):
            user = int(user)
            if 0 < user > 3:
                user = 0
    return user
#ilen koodi loppuu

# game starts
# ask to show the story
# storyDialog = input('Do you want to read the background story? (Y/N): ')
# if storyDialog == 'Y':
#     # print wrapped string line by line
#     for line in story.getStory():
#         print(line)

# GAME SETTINGS
print('When you are ready to start, ')
print(story)
player = input('type player name: ')
# boolean for game over and win
game_over = False
win = False

# start money = 1000
money = 1000                    #tarvitseeko tätä
# start range in km = 2000
player_range = 14000            ##muokatkaa tätä

# score = 0
score = 0               #miten lasketaan?

# boolean for diamond found
questions = 0
right_answers = 0
wrong_answers = 0
travel = 0

# all airports
all_airports = get_airports()
# start_airport ident. Haetaan satunnainen vietnamilainen kenttä aloituskentäksi
start_airport = get_start_airport()['ident'] #all_airports[0]['ident']

#Haetaan satunnainen amerikkalainen kenttä loppukentäksi
finish_airport = get_finish_airport()

# current airport
current_airport = start_airport

# game id
game_id = create_game(money, player_range, start_airport, player, all_airports)

#ilen koodi
#asetetaan kaikkien kenttien ICAO-koodit listaan
airport_icaos = []
for info in all_airports:
    airport_icaos.append(info['ident'])
#tänne kenttien ICAO-koodit, joilla on käyty
visited = []
game_won = False
reward_range = 4000 #tämä on oikeasta vastauksesta annettava voitto-range,
#ilen koodi loppuu

# GAME LOOP
while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)

    # show game status
    print(f'''You are at {airport['name']}.''')
    print(f"You have traveled to {travel} airports.")
    print(f'''You have answered to {questions} questions.\n
    Right answers: {right_answers}, Wrong answers: {wrong_answers}.
    You have {money:.0f}$ and {player_range:.0f}km of range.''')
    # pause
    # if airport has goal ask if player wants to open it
    # check goal type and add/subtract money accordingly

    goal = check_goal(game_id, current_airport)

    if goal:

        print(f'Theres a question in this airport!')
        print('If you answer correctly you will be awarded 500$ and 500km of range!')
        print('If you answer incorrectly you will lose 500km of range!')
        print(f"{goal['question']} (Answer 1, 2 or 3)")

        #ilen koodi, luodaan lista vastauksista

        answers = [goal['answer'], goal['wrong_answer'], goal['wrong_answer2']]
        #sekoitetaan vastaukset
        random.shuffle(answers)
        ##asetetaan jokaisen vastauksen eteen järjestysnumero, jonka käyttäjä näkee
        #ja jonka käyttäjä kirjoittaa kun valitsee vastausta
        answer_lines = answers.copy()
        answer_id = -1
        for i, answer in enumerate(answer_lines):
            # jos vastaus on oikea, niin otetaan sen järjestysnumero listassa muistiin
            # myöhempää tarkistusta varten
            if answer == goal['answer']:
                answer_id = i
            # lisätään näytettävien vastausten eteen sen järjestysnumero ja
            # asetetaan sen answer_lines-listaan, joka näytetään pelaajalle
            answer_lines[i] = f"{i + 1}. {answer_lines[i]}"
            print(answer_lines[i])
        # haetaan pelaajan vastausnumero
        user = get_answer()
        #ilen koodi loppuu

        #tarkistetaan oliko vastaus oikea
        if str(user) == str(answer_id + 1):
            print(f'Your answer was correct! As a reward you get 500$ and {reward_range} km of range!')
            money += 500        #tarvitseeko tätä?
            player_range += reward_range #muokatkaa tätä
            questions = 1
            right_answers += 1
        else:
            print(f'Your answer was incorrect! As a penalty, you lose 500km of range')
            player_range -= 500 #muokatkaa tätä?
            wrong_answers += 1
            questions += 1

    if wrong_answers >= 3:
        game_over = True
        print(f"You lost the game! You gave the wrong answer for three times. Better luck next time!")

    # get current airport info
    airport = get_airport_info(current_airport)

    # show game status
    #print(f'''You are at {airport['name']}.''')
    input('\033[32mPress Enter to continue...\033[0m')
    print(f"You have traveled to {travel} airports.")
    print(f'''You have answered to {questions} questions.\n
    Right answers: {right_answers}, Wrong answers: {wrong_answers}.
    You have {money:.0f}$ and {player_range:.0f}km of range.''')
    # if no range, game over

    # show airports in range. if none, game over
    airports = airports_in_range(current_airport, all_airports, player_range)
    print(f'''\033[34mThere are {len(airports)} airports in range: \033[0m''')
    if len(airports) == 0:
        print('You are out of range.')
        print('You lost the game as you are not able to travel to any other airport. Better luck next time!')
        game_over = True
    else:
        print(f'''Airports: ''')
        #ilen koodi, tarkastetaan onko USA-kenttä pelaajan etäisyydellä
        ap_distance = calculate_distance(current_airport, finish_airport['ident'])
        if ap_distance < player_range:
            print("You won, you have range to fly to USA")
            game_won = True
            game_over = True
            #mitä tapahtuu kuin voitto tulee
        #ilen koodi loppuu
        else:
            for airport in airports:
                if airport['ident'] not in visited:
                    ap_distance = calculate_distance(current_airport, airport['ident'])
                    print(f'''Country: {airport['iso_country']}, {airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
            # ask for destination
            dest = input('Enter destination icao: ').upper()
            #toista kunnes pelaaja antaa etäisyydellä olevan kentän ICAO:n
            while dest not in airport_icaos:
                dest = input('Enter destination icao: ').upper()
            #lisätään kenttä jonne matkustetaan vierailtujen kenttien listaan
            visited.append(dest)

            selected_distance = calculate_distance(current_airport, dest)
            player_range -= selected_distance
            update_location(dest, player_range, money, game_id)
            current_airport = dest
            travel += 1


    #if current_airport == #Laittakaa tähän USA lentokenttä mihin tämä peli loppuu!:
        #print(f'''You won! You managed to navigate back to USA! You have {money}$ and {player_range}km of range left.''')
        #game_over = True


# if game is over loop stops
# show game result

#tehkää täällä jotain kun peli  voitettu
if game_won:
    print("You are in USA now")
