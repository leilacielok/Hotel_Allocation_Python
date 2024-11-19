import numpy as np
import random
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict


def random_allocation(guests_dict, hotels_dict):
    
    # 1: shuffle the list of guest IDs for randoma allocation (Numpy)
    # 2: Dictionary to store allocation and satisfaction details
    guest_ids = list(guests_dict.keys())
    np.random.shuffle(guest_ids)
    allocation = {}    
    guest_satisfaction = {}
    
    # 3: Allocate each guest to a room as long as there are available rooms
    for guest_id in guest_ids:
        guest_id_str = str(guest_id) # ensure it is a string
        available_hotels = [hotel_id for hotel_id, hotel_data in hotels_dict.items()
                            if hotel_data['available_rooms'] > 0] # get the list of hotels with available rooms
        if not available_hotels:
            print("No more rooms available.")
            break 
    
        hotel_id = random.choice(available_hotels) # Select a random hotel from the available hotels list 
        guest_discount = guests_dict[guest_id]['discount'] # Get the guest's discount and hotel's final room price
        room_price = hotels_dict[hotel_id]['price']
        revenue = round(room_price * (1 - guest_discount), 2)
        preferences = guests_dict[guest_id]['preferences']  # Guest's list of preferred hotels
        
        # Satisfaction score
        satisfaction_score = (
            round((len(preferences) - preferences.index(hotel_id)) / len(preferences), 2)
            if hotel_id in preferences else 0 # default score for hotels outside the preference list
        ) 
        
        hotels_dict[hotel_id]['available_rooms'] -= 1 # update the number of available rooms in the hotel allocated
        
        # Store the allocation
        if hotel_id not in allocation: # 'new' hotel in the allocation dictionary
            allocation[hotel_id] = {
                'occupied_rooms': 1, # one room occupied at the first allocation
                'available_rooms': hotels_dict[hotel_id]['available_rooms'],
                'discount_applied': guest_discount,
                'revenue': revenue,
                'number_of_guests_accommodated': 1,
                'guests': [guest_id_str],
            }

        else: # If the hotel is already in allocation
            allocation[hotel_id]['occupied_rooms'] += 1  # Increment the number of occupied rooms
            allocation[hotel_id]['available_rooms'] = hotels_dict[hotel_id]['available_rooms']
            allocation[hotel_id]['revenue'] += revenue # add to the total revenue    
            allocation[hotel_id]['number_of_guests_accommodated'] += 1            
            allocation[hotel_id]['guests'].append(guest_id_str)  # Add the guest to the guest list
    
        # track satisfaction for the guest
        guest_satisfaction[guest_id_str] = satisfaction_score

    # Hotel status
    random_allocation_report = {}
    for hotel_id, data in hotels_dict.items():
        if hotel_id in allocation:
            details = allocation[hotel_id]
            random_allocation_report[hotel_id] = {
                'occupied_rooms': details['occupied_rooms'],
                'available_rooms': details['available_rooms'],
                'discount_applied': details['discount_applied'],
                'revenue': details['revenue'],  
                'number_of_guests_accommodated': details['number_of_guests_accommodated'],
                'guests': details['guests'],
            }
    else:
        # Initialize with default values for hotels with no allocation
        random_allocation_report[hotel_id] = {
            'occupied_rooms': 0,
            'available_rooms': data['available_rooms'],
            'discount_applied': None,
            'revenue': 0,  # Default revenue
            'number_of_guests_accommodated': 0,
            'guests': [],
        }
    
    # Overall statistics 
    total_guests = len(guest_satisfaction)
    total_revenues = sum(details['revenue'] for details in allocation.values()) # default value of 0 if revenue missing (no guests assigned to a hotel)
    occupied_hotels_count = sum(1 for details in allocation.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0
    total_satisfaction_score = sum(guest_satisfaction.values())
    average_satisfaction_score = round(total_satisfaction_score / total_guests, 2) if total_guests > 0 else 0
        
    #allocation['average_satisfaction'] = average_satisfaction_score # add the value to the allocation
    
    return {
        'allocation': allocation,
        'random_allocation_report': random_allocation_report,
        'occupied_hotels_count': occupied_hotels_count,
        'remaining_rooms': {hotel_id: hotels_dict[hotel_id]['available_rooms'] for hotel_id in hotels_dict},
        'average_revenue': average_revenue,
        'guest_satisfaction': guest_satisfaction,
        'average_satisfaction_score': average_satisfaction_score,
        'total_guests_count': total_guests
    }    


# Call the random_allocation function
random_allocation_result = random_allocation(guests_dict, hotels_dict)

# Function to print the report
def print_random_allocation_report(random_allocation_result):
    # Access random_allocation_report from the random_allocation_result dictionary
    if 'random_allocation_report' in random_allocation_result:
        print("Hotel Allocation Report:")
        for hotel, details in random_allocation_result['random_allocation_report'].items():
            print(f"'{hotel}': {{")
            print(f"    'occupied_rooms': {details['occupied_rooms']},")
            print(f"    'available_rooms': {details['available_rooms']},")
            print(f"    'number_of_guests_accommodated': {details['number_of_guests_accommodated']},")
            print(f"    'final_revenue': {details['revenue']:.2f},")
            print(f"    'guests': {details['guests']}")
            print("}")
        
        # Overall statistics
        print("\nOverall Statistics:")
        print(f"Total number of guests assigned: {random_allocation_result['total_guests_count']}")
        print(f"Overall average degree of satisfaction: {random_allocation_result['average_satisfaction_score']:.2f}")
        print(f"Total number of hotels occupied: {random_allocation_result['occupied_hotels_count']}")
        print(f"Overall average revenue per hotel: {random_allocation_result['average_revenue']:.2f}")
        
        # Guest satisfaction scores
     #   print("\nGuest Satisfaction Scores:")
     #   for guest_id, satisfaction in random_allocation_result['guest_satisfaction'].items():
     #       print(f"    '{guest_id}': {satisfaction:.2f}")
   
        
# Call the function to print the report
print_random_allocation_report(random_allocation_result)