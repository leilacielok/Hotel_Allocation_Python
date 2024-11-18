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
    sorted_hotels = hotels_df.sort_values(by='price').index
    
    # Store statistics
    allocation = {}
    hotel_occupancy = {hotel_id: {'occupied_rooms': 0, 'guests': []} for hotel_id in hotels_dict}
    
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
                    hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                    hotel_occupancy[hotel_id]['guests'].append(guest_id) # Track which guests were allocated to this hotel
                    allocated = True
                    break  # Stop and move to the next guest once allocated
        
        if not allocated:
            print(f"No allocation for {guest_id}")
    
    unassigned_count = len([guest_id for guest_id in guests_dict if guest_id not in allocation]) #count how many guests were not assigned
    occupied_hotels_count = sum(1 for hotel_id in hotel_occupancy if hotel_occupancy[hotel_id]['occupied_rooms'] > 0)

    # Results
    unassigned_guests = [guest_id for guest_id in guests_dict if guest_id not in allocation]
    remaining_rooms = {hotel_id: hotels_dict[hotel_id]['available_rooms'] for hotel_id in hotels_dict}
    occupied_rooms_per_hotel = {hotel_id: hotel_occupancy[hotel_id]['occupied_rooms'] for hotel_id in hotels_dict}
    guests_per_hotel = {hotel_id: hotel_occupancy[hotel_id]['guests'] for hotel_id in hotels_dict}
    
    # Return all the results
    return {
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'occupied_hotels_count': occupied_hotels_count,
        'remaining_rooms': remaining_rooms,
        'occupied_rooms_per_hotel': occupied_rooms_per_hotel,
        'guests_per_hotel': guests_per_hotel
    }

price_allocation_result = price_allocation(guests_dict, hotels_dict)
print("\nAllocation Results:")
print(price_allocation_result['allocation'])

print(f"\nNumber of unassigned guests: {price_allocation_result['unassigned_count']}")
print(f"Unassigned guests: {price_allocation_result['unassigned_guests']}")

print(f"\nNumber of occupied hotels: {price_allocation_result['occupied_hotels_count']}")

print("\nRemaining rooms in each hotel:")
for hotel, remaining in price_allocation_result['remaining_rooms'].items():
    print(f"{hotel}: {remaining} rooms left")

print("\nOccupied rooms in each hotel:")
for hotel, occupied in price_allocation_result['occupied_rooms_per_hotel'].items():
    print(f"{hotel}: {occupied} rooms occupied")
    
print("\nGuests in each hotel:")
for hotel, guests in price_allocation_result['guests_in_each_hotel'].items():
    print(f"{hotel}: {len(guests)} guests assigned")
