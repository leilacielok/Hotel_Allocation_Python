class hotels:
    def __init__(self, hotel_id, available_rooms, price):
        self.hotel_id = hotel_id
        self.rooms = available_rooms
        self.price = price

from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

hotels_dict = {}

for i, row in hotels_df.iterrows():
    hotel_id = row['hotel']
    available_rooms = row['rooms']
    price = row['price']

# Print guest_dict to check its contents
for hotel_id, hotel_obj in hotels_dict.items():
    print(f"Hotel ID: {hotel_id}")
    print(f"Number of rooms available: {hotel_obj.available_rooms}")
    print()  # Print a newline for readability
