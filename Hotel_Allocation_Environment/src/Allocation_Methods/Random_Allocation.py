import numpy as np
import random
import seaborn as sns
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Data_Visualization.random_visualization import (
    plot_occupancy_distribution, 
    plot_revenue_distribution,
    plot_guest_satisfaction_distribution,
    plot_guests_per_hotel,
)
                

def random_allocation(guests_dict_original, hotels_dict_original, verbose = False):
    """
    ## Parameters: 
     - Dictionary containing guests information: guest_id, discount, preferences list.
     - Dictionary containing hotels information: hotel_id, available_rooms, price.
     - verbose = False: I do not want line 36 to be printed in the main.py.
    ## Returns a dictionary:
     - Allocation: for each hotel, number of rooms occupied, rooms available, total revenue, number and list of guests allocated.
     - Allocation report: includes values of 0 in occupied rooms, revenue and guests for non-allocated hotels.
     - Overall statistics: count of assigned guests, avg satisfaction, couhnt of occupied hotels, avg revenue.
    """   
    # Make copies of the dictionaries to prevent modifying the originals
    guests_dict = guests_dict_original.copy()  
    hotels_dict = {k: v.copy() for k, v in hotels_dict_original.items()}  
    
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
            if verbose:
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
        
        # Store the allocation: if the hotel is 'new' to the allocation dictionary, start with 1 occupied room.
        if hotel_id not in allocation:
            allocation[hotel_id] = {
                'occupied_rooms': 1, 
                'available_rooms': hotels_dict[hotel_id]['available_rooms'],
                'discount_applied': guest_discount,
                'revenue': revenue,
                'number_of_guests_accommodated': 1,
                'guests': [guest_id_str],
            }

        else: # If the hotel is already in allocation: increment occupied rooms, revenue, and guests. Update number of available rooms.
            allocation[hotel_id]['occupied_rooms'] += 1 
            allocation[hotel_id]['available_rooms'] = hotels_dict[hotel_id]['available_rooms']
            allocation[hotel_id]['revenue'] += revenue    
            allocation[hotel_id]['number_of_guests_accommodated'] += 1            
            allocation[hotel_id]['guests'].append(guest_id_str) 
    
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
                'revenue': 0,  
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
    
    statistics = {
        'assigned_guests_count': total_guests,
        'average_satisfaction_score': average_satisfaction_score,
        'occupied_hotels_count': occupied_hotels_count,
        'average_revenue': average_revenue,
    }
    
    # Generate visualizations
    fig1 = plot_occupancy_distribution(allocation)
    print("Plot 1 generated:", fig1)
    fig2 = plot_revenue_distribution(allocation)
    print("Plot 2 generated:", fig2)
    fig3 = plot_guest_satisfaction_distribution(guest_satisfaction)
    print("Plot 3 generated:", fig3)
    fig4 = plot_guests_per_hotel(allocation)
    print("Plot 4 generated:", fig4)

    return {
        'allocation': allocation,
        'allocation_report': random_allocation_report,
        'statistics': statistics,
        'plots': [fig1, fig2, fig3, fig4]
}



# Store the random_allocation function
random_allocation_result = random_allocation(guests_dict_original, hotels_dict_original)

# Needed to pass the report to the main file
def print_random_allocation_report(random_allocation_result):
    # Assuming the result has a 'price_allocation_report' key that contains the report
    allocation_report = random_allocation_result.get('allocation_report', None)
    
    # Generate a string report
    report = f"Allocation Report:\n{allocation_report}"
    
    return report

