from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

def create_hotels_dict(hotels_df):
    """
    Creates a dictionary of hotels with their available rooms and prices.
    
    Parameters:
    hotels_df (DataFrame): DataFrame containing hotel data (id, rooms, price).
    
    Returns:
    dict: A dictionary where keys are hotel IDs and values are dictionaries with 'available_rooms' and 'price'.
    """
    hotels_dict = {}
    for _, row in hotels_df.iterrows():
        hotel_id = row['hotel']
        hotel_data = {
            'available_rooms': row['rooms'], 
            'price': row['price']
        }
        hotels_dict[hotel_id] = hotel_data
    return hotels_dict

hotels_dict_original = create_hotels_dict(hotels_df)

