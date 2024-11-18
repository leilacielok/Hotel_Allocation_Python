import numpy as np
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

## Initial status of the hotels
def initial_hotel_status(hotels_dict):
    print("Initial Hotel Available Rooms:")
    for hotel_id, hotel_data in hotels_dict.items():
        print(f"Hotel {hotel_id}: Available Rooms = {hotel_data['available_rooms']}")
 
## Function to allocate guests   
def reservation_allocation(guests_dict, hotels_dict):
    allocation = {} # store the allocation
    
    # Iterate over guests in order of reservation (over ids): get preferences and discount
    for guest_id, guest_data in sorted(guests_dict.items()):
        preferences = guest_data['preferences']
        discount = guest_data['discount']
        allocated = False
        
        # Allocation based on preferences
        for hotel in preferences:
            available_rooms = hotels_dict.get(hotel, {}).get('available_rooms', 0)
            
            if available_rooms > 0: # Available rooms: allocate the guest. If not, it skips to the next hotel in the preference list.
                allocation[guest_id] = {
                    'hotel': hotel,
                    'price': hotels_dict[hotel]["price"] * (1 - discount / 100),
                    'discount': discount,
                }
                
                hotels_dict[hotel]['available_rooms'] -= 1 # Decrease available rooms in the hotels dictionary
                
                allocated = True
                break
            
        if not allocated: # If no available rooms:
            allocation[guest_id] = {"hotel": None, "price": None, "discount": None}
    
    return allocation


# Everything is working: I checked where guests were assigned, with their discounts, their satisfaction score, and checked the remaining rooms for each hotel 

# Function to identify guests who could not be assigned
def reservation_check_unassigned_guests(reservation_allocation_result):
    # Hotel value is None --> unassigned guests
    unassigned_guests = [
        guest_id for guest_id, allocation in reservation_allocation_result.items() 
        if allocation["hotel"] is None]
    num_unassigned = len(unassigned_guests) # count the total number of unassigned guests

    return unassigned_guests, num_unassigned


# Hotel status
def retrieve_hotel_status(hotels_dict, reservation_allocation_result):
    hotel_status = {
        hotel_id: {
            'rooms_occupied': 0,
            'guests_accommodated': 0,
            'revenue': 0,
            'remaining_rooms': hotels_dict[hotel_id]['available_rooms'] 
            }
        for hotel_id in hotels_dict.keys()}


    # Update hotel status and calculate satisfaction
    for guest_id, allocation_info in reservation_allocation_result.items():
        allocated_hotel = allocation_info['hotel']
        final_price = allocation_info['price']
    
        if allocated_hotel:  # Check if the guest was actually allocated to a room in the hotel 
            #update status 
            hotel_status[allocated_hotel]['rooms_occupied'] += 1
            hotel_status[allocated_hotel]['guests_accommodated'] += 1
            hotel_status[allocated_hotel]['revenue'] += final_price
            hotel_status[allocated_hotel]['remaining_rooms'] -= 1
    
    return hotel_status


## Calculate satisfaction score
def calculate_satisfaction(guests_dict, reservation_allocation_result):
    customer_satisfaction = {}
    total_satisfaction = 0
    assigned_count = 0  # Count of assigned guests
    
    for guest_id, allocation_info in reservation_allocation_result.items():
        allocated_hotel = allocation_info['hotel']
        preferences = guests_dict[guest_id]['preferences']  # get preferences of the guest
        satisfaction_score = 0  # Default to 0 for unassigned guests
        
        if allocated_hotel:
            assigned_count += 1
            if allocated_hotel in preferences:
                satisfaction_score = (1 - preferences.index(allocated_hotel) / len(preferences)) * 100
            else:
                satisfaction_score = 0 # the hotel is not in the guest's preferences

        customer_satisfaction[guest_id] = satisfaction_score # Store satisfaction score
        total_satisfaction += satisfaction_score
        
    average_satisfaction = total_satisfaction / len(guests_dict) # keep the total in the denominator to penalize for guests who could not be assigned
    return customer_satisfaction, average_satisfaction


## Final report on reservation order allocation
def generate_reservation_report(
    unassigned_guests, 
    hotel_status, 
    customer_satisfaction, 
    average_satisfaction, 
    verbose=True
):
    """Generates a consolidated report of the reservation process."""
    report = []
    
    if verbose:
        report.append("\n--- Unassigned Guests ---")
        if unassigned_guests:
            report.append(f"Unassigned guests: {unassigned_guests}")
            report.append(f"Number of unassigned guests: {len(unassigned_guests)}")
        else:
            report.append("All guests have been successfully assigned.")

        report.append("\n--- Hotel Status ---")
        for hotel_id, status in hotel_status.items():
            report.append(
                f"{hotel_id}: Remaining Rooms = {status['remaining_rooms']}, "
                f"Rooms Occupied = {status['rooms_occupied']}, "
                f"Revenue = ${status['revenue']:.2f}, "
                f"Guests Accommodated = {status['guests_accommodated']}"
            )
        
        report.append(f"\nTotal Hotels Occupied: {sum(1 for status in hotel_status.values() if status['rooms_occupied'] > 0)}")

        report.append("\n--- Customer Satisfaction ---")
        for guest_id, score in customer_satisfaction.items():
            report.append(f"Guest {guest_id}: Satisfaction = {score:.2f}%")
        report.append(f"\nAverage Customer Satisfaction: {average_satisfaction:.2f}%")
    else:
        report.append(f"Average Customer Satisfaction: {average_satisfaction:.2f}%")
        report.append(f"Total Unassigned Guests: {len(unassigned_guests)}")
        report.append(f"Total Hotels Occupied: {sum(1 for status in hotel_status.values() if status['rooms_occupied'] > 0)}")

    return "/n".join(report)
    
  
# Call the functions and gather them together in 'reservation_report' 
reservation_allocation_result = reservation_allocation(guests_dict, hotels_dict)

# Check unassigned guests
unassigned_guests, num_unassigned = reservation_check_unassigned_guests(reservation_allocation_result)

# Calculate hotel status
hotel_status = retrieve_hotel_status(hotels_dict, reservation_allocation_result)

# Calculate customer satisfaction
customer_satisfaction, average_satisfaction = calculate_satisfaction(guests_dict, reservation_allocation_result)

# Generate and print report
reservation_report = generate_reservation_report(unassigned_guests, hotel_status, customer_satisfaction, average_satisfaction, verbose=True)

print(reservation_report)


