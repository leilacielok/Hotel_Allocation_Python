import numpy as np
import random
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

guest_ids = np.array(list(guests_dict.keys()))

# Function for random allocation of customers to hotels
def random_allocation(guests_dict, hotels_dict):
    # List of available hotel-room pairs (hotel ID, room number)
    left_rooms = []
    for hotel_id, hotel_data in hotels_dict.items():
        left_rooms.extend([(hotel_id, room_num + 1) for room_num in range(hotel_data['available_rooms'])])  #list of tuples: hotel id + rooms

    # Numpy to shuffle guest list to ensure random assignment order
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
def random_check_unassigned_guests(guests_dict, random_allocation_result):
    unassigned_guests = set(guests_dict.keys()) - set(random_allocation_result.keys()) #By converting to sets, I can use subtraction to identify unassigned guests
    if unassigned_guests:
        print("Unassigned guests:", list(unassigned_guests))
    else:
        print("All guests have been successfully assigned.")

random_check_assignment = random_check_unassigned_guests(guests_dict, random_allocation_result)

# Initialize rooms occupied, guests accommodated, revenues and remaining rooms (dictionary)
hotel_status = {
    hotel_id: {
        'rooms_occupied': 0,
        'guests_accommodated': 0,
        'revenue': 0,
        'remaining_rooms': hotels_dict[hotel_id]['available_rooms'] 
        }
    for hotel_id in hotels_dict.keys()}

# Extract data to use Numpy
room_prices = np.array([hotels_dict[info['hotel_id']]['price'] for guest_id, info in random_allocation_result.items()])
discounts = np.array([info['discount_applied'] for guest_id, info in random_allocation_result.items()])
allocated_hotels = np.array([info['hotel_id'] for guest_id, info in random_allocation_result.items()])

# Vectorized calculation of final prices
final_prices = room_prices * (1 - discounts)

# Initialize customer satisfaction
total_satisfaction = 0

# Update hotel status
for guest_id, (final_price, allocated_hotel) in enumerate(zip(final_prices, allocated_hotels)):
    hotel_status[allocated_hotel]['rooms_occupied'] += 1 # Add one occupied room for each allocation
    hotel_status[allocated_hotel]['guests_accommodated'] += 1 # Add 1 guest for each allocation
    hotel_status[allocated_hotel]['revenue'] += final_price # add price discounted as revenue
    hotel_status[allocated_hotel]['remaining_rooms'] -= 1 # Subtract one available room for each allocation

    # Guest satisfaction: if the hotel is in the preference, calculate the score, otherwise score = 0
    preferences = guests_dict[guest_ids[guest_id]]['preferences']
    if allocated_hotel in preferences:
        satisfaction_score = ((len(preferences)) - preferences.index(allocated_hotel)) / len(preferences) * 100
    else:
        satisfaction_score = 0
    total_satisfaction += satisfaction_score

# Average satisfaction: aggregate the scores and calculate average
average_satisfaction = total_satisfaction / len(guest_ids) if len(guest_ids) > 0 else 0

# How many hotels were occupied? (At least one room occupied)
total_occupied_hotels = sum(1 for status in hotel_status.values() if status['rooms_occupied'] > 0)


# Print updated status
print("\nHotel Status:")
for hotel_id, status in hotel_status.items():
    print(
        f"{hotel_id}: Remaining Rooms = {status['remaining_rooms']}, "
        f"Rooms Occupied = {status['rooms_occupied']}, "
        f"Revenue = ${status['revenue']:.2f}, "
        f"Guests Accommodated = {status['guests_accommodated']}"
    )

print(f"\nTotal Hotels Occupied: {total_occupied_hotels}")
print(f"Average Customer Satisfaction: {average_satisfaction:.2f}%")