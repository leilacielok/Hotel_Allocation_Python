import pandas as pd

def load_data():
    hotels = pd.read_excel("C:/Users/Leila/Downloads/hotels.xlsx")
    guests = pd.read_excel("C:/Users/Leila/Downloads/guests.xlsx")
    preferences = pd.read_excel("C:/Users/Leila/Downloads/preferences.xlsx")
    return hotels, guests, preferences

print(load_data())
