import numpy as np
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original

def reservation_allocation(guests_dict_original, hotels_dict_original):
    """
    ## Parameters: 
     - Dictionary containing guests information: guest_id, discount, preferences list.
     - Dictionary containing hotels information: hotel_id, available_rooms, price.
    ## Returns a dictionary:
     - Allocation: for each hotel, number of rooms occupied, rooms available, total revenue, list of guests allocated.
     - Unassigned guests (count and list).
     - Allocation report: 0 for non-occupied hotels.
     - Overall statistics: count of assigned guests, avg satisfaction, couhnt of occupied hotels, avg revenue.
    """   
    # Make copies of the dictionaries to prevent modifying the originals
    guests_dict = guests_dict_original.copy()  
    hotels_dict = {k: v.copy() for k, v in hotels_dict_original.items()}  
    allocation = {} 

    # Initialize hotel status
    hotel_status = { 
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
    
    # Calculate total number of guests assigned
    total_assigned_guests = len(allocation)  
    
    # Total and overall average revenue
    total_revenues = sum(details['final_revenue'] for details in reservation_allocation_report.values())
    occupied_hotels_count = sum(1 for details in reservation_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0 # don't divide by 0
    
    # Avg satisfaction score
    average_satisfaction_score = round(total_satisfaction / len(guests_dict), 2) # I include unassigned guest to penalize the final score

    statistics = {
        'assigned_guests_count': total_assigned_guests,
        'average_satisfaction_score': average_satisfaction_score,
        'occupied_hotels_count': occupied_hotels_count,
        'average_revenue': average_revenue
    }
    
    return{
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'assigned_guests_count': total_assigned_guests,
        'reservation_allocation_report': reservation_allocation_report,
        'statistics': statistics,
    } 

# Store the function
reservation_allocation_result = reservation_allocation(guests_dict_original, hotels_dict_original)


# Needed to pass the report to the main file
def printed_reservation_allocation_report(reservation_allocation_result):
    allocation_report = reservation_allocation_result.get('reservation_allocation_report', None)
   
    # Generate a string report or any formatted output here
    report = f"Allocation Report:\n{allocation_report}"
    
    return report

