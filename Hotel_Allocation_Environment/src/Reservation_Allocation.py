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
            if hotels_dict.get(hotel, {}).get("available_rooms", 0) > 0: # Available rooms: allocate the guest. If not, it skips to the next hotel in the preference list.
                allocation[guest_id] = {
                    'hotel': hotel,
                    'price': hotels_dict[hotel]["price"] * (1 - discount / 100),
                    'discount': discount,
                }
                hotels_dict[hotel]['available_rooms'] -= 1
                break
            else: # If no available rooms:
                allocation[guest_id] = {"hotel": None, "price": None, "discount": None}
    return allocation

reservation_allocation_result = reservation_allocation(guests_dict, hotels_dict)
print(reservation_allocation_result)

# Check if everything works properly

# Function: check which and how many guests were not assigned 
def reservation_check_unassigned_guests(guests_dict, reservation_allocation_result):
    # Hotel value is None --> unassigned guests
    unassigned_guests = [
        guest_id for guest_id, allocation in reservation_allocation_result.items() 
        if allocation["hotel"] is None
    ]
    # count the total number of unassigned guests
    num_unassigned = len(unassigned_guests)
    
    # Output results
    if unassigned_guests:
        print("Unassigned guests:", unassigned_guests)
        print("Number of unassigned guests:", num_unassigned)
    else:
        print("All guests have been successfully assigned.")
    
    return unassigned_guests, num_unassigned  # Return the list and the total number of unassigned guests.

# Call the function
num_unassigned, unassigned_guests = reservation_check_unassigned_guests(guests_dict, reservation_allocation_result)

# Hotel status
from src.RandomAllocation import guest_ids

hotel_status = {
    hotel_id: {
        'rooms_occupied': 0,
        'guests_accommodated': 0,
        'revenue': 0,
        'remaining_rooms': hotels_dict[hotel_id]['available_rooms'] 
        }
    for hotel_id in hotels_dict.keys()}

allocated_hotels = [
    info['hotel'] for guest_id, info in reservation_allocation_result.items()
]
final_prices = [
    info['price'] if info['price'] is not None else 0
    for guest_id, info in reservation_allocation_result.items()
]

# Initialize total satisfaction
total_satisfaction = 0 # Needed for the average
customer_satisfaction = {}

# Update hotel status and calculate satisfaction
for guest_id, allocation_info in reservation_allocation_result.items():
    allocated_hotel = allocation_info['hotel']
    final_price = allocation_info['price']
    
    if allocated_hotel:  # Check if the guest was actually allocated to a room in the hotel 
        #update status 
        if hotel_status[allocated_hotel]['remaining_rooms'] > 0: # Update hotel status
            hotel_status[allocated_hotel]['rooms_occupied'] += 1
            hotel_status[allocated_hotel]['guests_accommodated'] += 1
            hotel_status[allocated_hotel]['revenue'] += final_price
            hotel_status[allocated_hotel]['remaining_rooms'] -= 1

        # Calculate satisfaction score
        preferences = guests_dict[guest_id]['preferences']  # get preferences of the guest
        if allocated_hotel in preferences:
            satisfaction_score = (1 - preferences.index(allocated_hotel) / len(preferences)) * 100
        else:
            satisfaction_score = 0 # the hotel is not in the guest's preferences
            
        # Store satisfaction score
        customer_satisfaction[guest_id] = satisfaction_score
        total_satisfaction += satisfaction_score
        
    else: # unassigned guests (no available rooms)
        customer_satisfaction[guest_id] = 0 

# Average satisfaction
average_satisfaction = total_satisfaction / len(guests_dict) if len(guests_dict) > 0 else 0

# Count total hotels occupied
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
print("\nCustomer Satisfaction (Per Guest):")
for guest_id, score in customer_satisfaction.items():
    print(f"Guest {guest_id}: Satisfaction = {score:.2f}%")
print(f"Average Customer Satisfaction: {average_satisfaction:.2f}%")