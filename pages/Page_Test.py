#import streamlit as st
import csv
import random
import re

#st.title(":material/glyphs:")
#st.write("Page pour tester du code")
#st.divider()

with open('data/CanadianPostalCodes202403.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    locations = list(reader)

postal_code = ["L9Y 1K4", "M4C 1S9", "G0J 1J0", "G5H 3P8","8hp 2up"]

def check_valid_postal_code(code):
    """Checks if a postal code is valid"""
    pattern = re.compile(r'^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$')
    return bool(pattern.match(code))

def get_random_location(locations):
    """Returns a random location from the list of locations"""
    return random.choice(locations)

def get_lat_long(code, locations):
    """Returns the latitude and longitude of a postal code"""
    for location in locations:
        if check_valid_postal_code(code) and code == location[0]:
            if len(location) >= 6:
                a = [location[4], location[5]]
                return a
            else:
                print(f"Error: The location data for postal code {code} does not have latitude and longitude information.")
                return None
for code in postal_code:
    if check_valid_postal_code(code):
        print(get_lat_long(code, locations))
    else:
        print(f"Invalid postal code: {code}")
