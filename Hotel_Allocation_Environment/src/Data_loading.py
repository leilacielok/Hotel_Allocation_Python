import pandas as pd

def load_data():
    hotels_df = pd.read_excel("C:/Users/Leila/Downloads/hotels.xlsx", index_col=0)
    guests_df = pd.read_excel("C:/Users/Leila/Downloads/guests.xlsx", index_col=0)
    preferences_df = pd.read_excel("C:/Users/Leila/Downloads/preferences.xlsx", index_col=0)
    preferences_df['guest'] = preferences_df['guest'].str.extract(r'(\d+)', expand=False).astype(int)

    return hotels_df, guests_df, preferences_df

hotels_df, guests_df, preferences_df = load_data()
