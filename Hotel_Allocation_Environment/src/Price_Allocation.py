# First, Hotels are sorted by price, ensuring cheaper options are considered first.
# Guests are processed in the natural order of their IDs, so in order of reservation.
# Preference Matching: For each guest, I iterate through their preferences to find the first available room in their order of priorities.
# Once a room is allocated I can move to the next guest.

import pandas as pd
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

def price_allocation(guests_dict, hotels_dict):
    
    # 1: sort hotels by price using pandas
    hotels_df = pd.DataFrame(hotels_dict).T  # Transpose to flip the dictionary
    sorted_hotels = hotels_df.sort_values(by='price')
    allocation = {}
    
    # Step 2: Process guests in ID order
    for guest_id, guest_info in sorted(guests_dict.items()): # sort guests by their ids: reservation order
        preferences = guest_info['preferences'] # retrieve the preferences for each guest
        allocated = False
        
        for hotel_id in sorted_hotels:
            #Check that the hotel encountered in order of price is in preferences
            if hotel_id in preferences:
                # Check if hotel has available rooms
                if hotels_dict[hotel_id]['available_rooms'] > 0:
                    # Allocate room
                    allocation[guest_id] = hotel_id
                    hotels_dict[hotel_id]['available_rooms'] -= 1
                    allocated = True
                    break  # Stop and move to the next guest once allocated
        if not allocated:
            print(f"No allocation for {guest_id}")
    
    return allocation

price_allocation_result = price_allocation(guests_dict, hotels_dict)
print(price_allocation_result)

# Print the allocation
print("Room Allocations:")
for guest, hotel in allocation.items():
    print(f"{guest}: {hotel}")

# Print remaining rooms in hotels
print("\nRemaining Hotel Rooms:")
for hotel, details in hotels_dict.items():
    print(f"{hotel}: {details['available_rooms']} rooms left")