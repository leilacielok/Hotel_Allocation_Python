import numpy as np
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

def reservation_allocation(guests_dict, hotels_dict):
    allocation = {} # store the allocation

    hotel_status = { # initialize Hotel status
        hotel_id: {
            'rooms_occupied': 0,
            'remaining_rooms': hotels_dict[hotel_id]['available_rooms'],
            'guests_accommodated': 0,
            'revenue': 0,
            }
        for hotel_id in hotels_dict.keys()
    }
    
    customer_satisfaction = {} # individual satisfaction scores
    total_satisfaction = 0 # initialize total satisfaction to calculate average
    unassigned_guests = [] # list with unassigned guests
    
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
                
                # Update hotel status and dictionary on available rooms
                hotels_dict[hotel]['available_rooms'] -= 1
                hotel_status[hotel]['rooms_occupied'] += 1
                hotel_status[hotel]['remaining_rooms'] -= 1
                hotel_status[hotel]['guests_accommodated'] += 1
                hotel_status[hotel]['revenue'] += allocation[guest_id]['price']
                                
                # Calculate guest satisfaction
                satisfaction_score = round((len(preferences) - preferences.index(hotel)) / len(preferences), 2)  # Higher score for better match
                customer_satisfaction[guest_id] = satisfaction_score
                total_satisfaction += satisfaction_score
                
                allocated = True
                break
            
        if not allocated: # If no available rooms in preferred hotel: mark as unassigned guest
            customer_satisfaction[guest_id] = 0
            unassigned_guests.append(guest_id)

    
    # Unassigned guests count
    unassigned_count = len(unassigned_guests) #count how many guests were not assigned
    
    # Hotel report
    reservation_allocation_report = {}

    for hotel_id, data in hotels_dict.items():
        guests = [guest_id for guest_id, allocation_info in allocation.items() if allocation_info['hotel'] == hotel_id]
        final_revenue = sum(allocation[guest_id]['price'] for guest_id in guests)
        
        reservation_allocation_report[hotel_id] = {
            'rooms_occupied': hotel_status[hotel_id]['rooms_occupied'],
            'rooms_available': data['available_rooms'],
            'number_of_guests_accommodated': len(guests),
            'final_revenue': round(final_revenue, 2),
            'guests': guests
        } 
    
    # Now I have all the details I need to compute total and average revenue
    # Total and overall average revenue
    total_revenues = sum(details['final_revenue'] for details in reservation_allocation_report.values())
    occupied_hotels_count = sum(1 for details in reservation_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0 # don't divide by 0
    
    # Satisfaction score
    average_satisfaction_score = round(total_satisfaction / len(guests_dict), 2) # I include unassigned guest to penalize the final score

#   return the results for allocation, guests and hotels.
    return{
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'occupied_hotels_count': occupied_hotels_count,
        'remaining_rooms': {hotel_id: hotels_dict[hotel_id]['available_rooms'] for hotel_id in hotels_dict},
        'reservation_allocation_report': reservation_allocation_report,
        'average_revenue': average_revenue,
        'guest_satisfaction': customer_satisfaction,
        'average_satisfaction_score': average_satisfaction_score
    } 

reservation_allocation_result = reservation_allocation(guests_dict, hotels_dict)


def printed_reservation_allocation_report(reservation_allocation_result):
    # Print Unassigned Guests
    print("\nUnassigned Guests:")
    print(f"  {reservation_allocation_result['unassigned_count']} guests were not assigned to any hotel.")
    print(f"  Unassigned Guests List: {reservation_allocation_result['unassigned_guests']}")
    
    # Print guests' satisfaction scores
    print("\nCustomer Satisfaction Scores:")
    for guest_id, satisfaction_score in reservation_allocation_result['guest_satisfaction'].items():
        print(f"  Guest {guest_id}: Satisfaction Score = {satisfaction_score}")
        
    # Print details for each hotel: Remaining Rooms, Occupied Rooms, and Revenue
    print("\nHotel Room Allocation and Revenue:")
    for hotel_id, report in reservation_allocation_result['reservation_allocation_report'].items():
        print(f"\n{hotel_id}:")
        print(f"  Remaining Rooms: {report['rooms_available']}")
        print(f"  Occupied Rooms: {report['rooms_occupied']}")
        print(f"  Revenue: {report['final_revenue']}")
        print(f"  Assigned Guests: {report['guests']}")  # Printing the list of assigned guests

    # Print the overall statistics
    print("\nOverall Statistics:")
    print(f"\nOverall Average Revenue: {reservation_allocation_result['average_revenue']}")
    print(f"Average Satisfaction Score: {reservation_allocation_result['average_satisfaction_score']}")
    print(f"\nNumber of Occupied Hotels: {reservation_allocation_result['occupied_hotels_count']}")

printed_reservation_allocation_report(reservation_allocation_result)