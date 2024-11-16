class hotels:
    def __init__(self, hotel_id, available_rooms, price):
        self.hotel_id = hotel_id
        self.available_rooms = available_rooms
        self.price = price

from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

hotels_dict = {}

for i, row in hotels_df.iterrows():
    hotel_id = row['hotel']
    hotel_data = {'available_rooms': row['rooms'], 'price': row['price']}
    hotels_dict[hotel_id] = hotel_data
 
if __name__ == "__main__":    
    print(hotels_dict)

