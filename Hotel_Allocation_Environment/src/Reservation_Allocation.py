import numpy as np
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

def reservation_allocation(guests_dict, hotels_dict):
    allocation = {} # store the allocation
    
    # Iterate over guests in order of reservation (over ids): get preferences and discount
    for guest_id, guest_data in sorted(guests_dict.items()):
        preferences = guest_data['preferences']
        discount = guest_data['discount']
    
        # Allocation based on preferences
        for hotel in preferences:
            if hotels_dict.get(hotel, {}).get("available_rooms", 0) > 0: # Available rooms: allocate the guest
                allocation[guest_id] = {
                    'hotel': hotel,
                    'price': hotels_dict[hotel]["price"] * (1 - discount / 100),
                }
                hotels_dict[hotel]['available_rooms'] -= 1
                break
            else: # If no available rooms:
                allocation[guest_id] = {"hotel": None, "price": None}
    return allocation

reservation_allocation_result = reservation_allocation(guests_dict, hotels_dict)

print(reservation_allocation_result)