import numpy as np
import random
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

# Function for random allocation of customers to hotels
def random_allocation(guests_dict, hotels_dict):
    # List of available hotel-room pairs (hotel ID, room number)
    left_rooms = []
    for hotel_id, hotel_data in hotels_dict.items():
        left_rooms.extend([(hotel_id, room_num + 1) for room_num in range(hotel_data['available_rooms'])])  #list of tuples: hotel id + rooms

    # Numpy to shuffle guest list to ensure random assignment order
    guest_ids = np.array(list(guests_dict.keys()))
    np.random.shuffle(guest_ids)
    
    # Dictionary to store allocation details
    allocation = {}

    # Allocate each guest to a room as long as there are available rooms
    for guest_id in guest_ids:
        if not left_rooms:
            print("No more rooms available.")
            break
        # Select a random room from the left rooms list    
        hotel_id, room_number = left_rooms.pop(random.randint(0, len(left_rooms) - 1))   #generates a random integer between 0 and the last valid index in the list (len(new_room_number) - 1).
       
        # Fetch the guest's discount and hotel's room price
        guest_discount = guests_dict[guest_id]['discount'] # discount of the guest
        room_price = hotels_dict[hotel_id]['price'] # room price
        # Final price of the room (discounted)
        final_price = room_price * (1 - guest_discount)
        
        # Store the allocation
        allocation[guest_id] = {
                'hotel_id': hotel_id,
                'room_number': room_number,
                'discount_applied': guest_discount,
                'price_paid': final_price
            }

    return allocation

    

# I have the result, now I just need something to check the result:
# whether every guest was assigned how many hotels remain, how many rooms for each hotel, total revenue of each hotel.


# Call the random_allocation function
random_allocation_result = random_allocation(guests_dict, hotels_dict)

# Check if all guests have been assigned: Set operations
def random_check_all_guests_assigned(guests_dict, random_allocation_result):
    unassigned_guests = set(guests_dict.keys()) - set(random_allocation_result.keys()) #By converting to sets, I can use subtraction to identify unassigned guests
    if unassigned_guests:
        print("Unassigned guests:", list(unassigned_guests))
    else:
        print("All guests have been successfully assigned.")

random_check_assignment = random_check_all_guests_assigned(guests_dict, random_allocation_result)

# Initialize remaining rooms and revenues
hotel_status = {hotel_id: {'remaining_rooms': hotels_dict[hotel_id]['available_rooms'], 'revenue': 0}
                for hotel_id in hotels_dict.keys()}

# Extract data for NumPy processing
room_prices = np.array([hotels_dict[info['hotel_id']]['price'] for guest_id, info in random_allocation_result.items()])
discounts = np.array([info['discount_applied'] for guest_id, info in random_allocation_result.items()])
# Vectorized calculation of final prices
final_prices = room_prices * (1 - discounts)

# Aggregate revenue for each hotel
hotel_revenues = {}
for guest_id, (final_price, details) in enumerate(zip(final_prices, random_allocation_result.values())):
    hotel_id = details['hotel_id']
    hotel_status[hotel_id]['revenue'] += final_price
    hotel_status[hotel_id]['remaining_rooms'] -= 1 # subtract 1 room for each allocation

# Print updated status
print("\nHotel Status:")
for hotel_id, status in hotel_status.items():
    print(f"{hotel_id}: Remaining Rooms: {status['remaining_rooms']}, Total Revenue: ${status['revenue']:.2f}")


