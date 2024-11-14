import random
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

# Function for random allocation of customers to hotels
def random_allocation(guests_dict, hotels_dict):
    # List of available hotel-room pairs (hotel ID, room number)
    left_rooms = []
    for hotel_id, hotel_data in hotels_dict.items():
        left_rooms.extend([(hotel_id, room_num + 1) for room_num in range(hotel_data['available_rooms'])])  #list of tuples: hotel id + rooms

    # Shuffle guest list to ensure random assignment order
    guest_ids = list(guests_dict.keys())
    random.shuffle(guest_ids)
    
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

# Result of the allocation (calling the function)
allocation_result = random_allocation(guests_dict, hotels_dict)

# Print allocation result
for guest_id, details in allocation_result.items():
    print(f"Guest {guest_id}: Assigned to {details['hotel_id']}, Room {details['room_number']}; "
          f"Discount: {details['discount_applied']*100}%, Price Paid: ${details['price_paid']:.2f}")
    

# I have the result, now I just need something to check the result: check 