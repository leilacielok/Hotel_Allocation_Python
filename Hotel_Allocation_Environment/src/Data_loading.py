import pandas as pd

def load_data():
    hotels_df = pd.read_excel("C:/Users/Leila/Downloads/hotels.xlsx")
    guests_df = pd.read_excel("C:/Users/Leila/Downloads/guests.xlsx")
    preferences_df = pd.read_excel("C:/Users/Leila/Downloads/preferences.xlsx")
    return hotels_df, guests_df, preferences_df

print(load_data())
