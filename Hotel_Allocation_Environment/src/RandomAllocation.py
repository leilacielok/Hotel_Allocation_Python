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
random_allocation_result = random_allocation(guests_dict, hotels_dict)

# Print allocation result
for guest_id, details in random_allocation_result.items():
    print(f"Guest {guest_id}: Assigned to {details['hotel_id']}, Room {details['room_number']}; "
          f"Discount: {details['discount_applied']*100}%, Price Paid: ${details['price_paid']:.2f}")
    

# I have the result, now I just need something to check the result:
# whether every guest was assigned how many hotels remain, how many rooms for each hotel, total revenue of each hotel.

# Initialize remaining rooms and revenue for each hotel
def initialize_hotel_status(hotels_dict):
    return {
        hotel_id: {'remaining_rooms': hotel_info['available_rooms'], 'revenue': 0}
        for hotel_id, hotel_info in hotels_dict.items()
    } #For each hotel_id in the dictionary, an entry is created in hotel_status

hotel_status = initialize_hotel_status(hotels_dict)

print(hotel_status)
for hotel_id, status in hotel_status.items():
    print(hotel_id, status)
    

# Have all guests been assigned?
def random_check_all_guests_assigned(guests_dict, random_allocation_result):
    unassigned_guests = [guest for guest in guests_dict if guest not in random_allocation_result]
    if unassigned_guests:
        print("Unassigned guests:", unassigned_guests)
    else:
        print("All guests have been successfully assigned.")

# Calculate the remaining rooms and final revenue for each hotel
def random_hotel_status(hotels_dict, random_allocation_result, guests_dict, hotel_status):
    for guest_id, guest_info in random_allocation_result.items():
        hotel_id = guest_info['hotel_id'] # To access the allocated hotel from the allocation result. 
        
        # Check if the hotel is in the hotel status dictionary
        if hotel_id in hotel_status:
            
            #Lower the room count
            if hotel_status[hotel_id]['remaining_rooms'] > 0:
                hotel_status[hotel_id]['remaining_rooms'] -=1
            
                # Calculate final price for the guest after discount
                room_price = hotels_dict[hotel_id]['price']
                discount = guests_dict[guest_id]['discount']
                revenue = room_price * (1 - discount)
                
                # Update revenue and available rooms
                hotel_status[hotel_id]['revenue'] += revenue
            
            else:
                print(f"No rooms available for {hotel_id}: {guest_id} was not allocated.")
        
        else:
            print(f"Invalid hotel ID: {hotel_id}, {guest_id}")
            

# Check, update and print the status 
random_hotel_status(hotels_dict, random_allocation_result, guests_dict, hotel_status)  
print("Updated Hotel Status:")
for hotel_id, status in hotel_status.items():
    print(f"{hotel_id}: Remaining Rooms = {status['remaining_rooms']}, Revenue = ${status['revenue']:.2f}")

 # Output the status for each hotel
    #for hotel_id, status in hotel_status.items():
     #   print(f"Hotel {hotel_id}:")
      #  print(f"  Remaining rooms: {status['remaining_rooms']}")
       # print(f"  Final revenue: ${status['revenue']:.2f}")

# Final check
#random_check_all_guests_assigned(guests_dict, random_allocation_result)
#random_hotel_status(hotels_dict, random_allocation_result, guests_dict)