import textwrap

story = '''Year 1975, near the end of the Vietnam War, you wake up on an unfamiliar island in a different timeline, utterly perplexed. 

You initially think it's a dream, but reality soon sets in. You discover a mysterious letter and a map tucked away in your pocket. Beside you an unconscious soldier in immediate need of medical attention. To your surprise, this person seems oddly familiar.

As you open the letter, its words explain your incredible situation: " Greetings, intrepid traveler. You have traveled from the year 2030 and have been selected for a daring mission. You've always wished to meet your grandfather, a brave Cold War soldier, who's now severely injured. 

Your mission: safely bring your grandfather back home to the USA, as he holds critical information for the U.S. government. Yet, be cautious- your choices, matters, and a misstep could trap you here forever, endangering your grandfather's life."  

With the letter as your guide, you set off your journey, armed with a map and essential supplies. Setting off from Vietnam Airport, you encounter yet another letter just before your departure: " Welcome your mission begins here!"  

Your first challenge emerges as a dire warning from the plane's controls: your fuel levels are dangerously low, insufficient to reach your goal destination. Your decision? Attempting your luck by answering the first question posed at the airport. Fortune smiles on you, granting you a valuable reward.

You must continue your journey now, but you must be cautious with future challenges, as wrong answers can cost you dearly. Gathering money at each airport, until you reach your destination.

When you finally arrive at your destination and complete your mission successfully, you finally reunite with your grandfather once he regains consciousness. Your grandfather sends you back home and you wake up. It was a dream after all! 

'''

# Set column width to 80 characters
wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
# Wrap text
word_list = wrapper.wrap(text=story)


def getStory():
    return word_list
