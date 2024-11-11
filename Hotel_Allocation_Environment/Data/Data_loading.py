import pandas as pd

guests_path = "C:/Users/Leila/OneDrive/Desktop/Progetti/guests_dataset.xlsx"
guests_df = pd.read_excel(guests_path)
print(guests_df.head())

hotels_path = "C:/Users/Leila/OneDrive/Desktop/Progetti/hotels_dataset.xlsx"
hotels_df = pd.read_excel(hotels_path)
print(hotels_df.head())

preferences_path = "C:/Users/Leila/OneDrive/Desktop/Progetti/preferences_dataset.xlsx"
preferences_df = pd.read_excel(preferences_path)
print(preferences_df.head())