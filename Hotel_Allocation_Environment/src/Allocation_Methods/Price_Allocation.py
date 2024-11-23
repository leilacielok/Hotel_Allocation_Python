import pandas as pd
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Data_Visualization.random_visualization import (
    plot_revenue_distribution,
    plot_guest_satisfaction_distribution,
    plot_guests_per_hotel,
)

"""
Concept:
- Assign the guest to a hotel from their preferences, in order of price (since sorted_hotels is sorted by price).
  Guests are processed in the natural order of their IDs, so in order of reservation.
- If no preferred hotels are available, I decided to assign the guest to the cheapest available hotel.
Satisfaction Score:
- If the guest is allocated to a preferred hotel, their satisfaction is based on the index of the hotel in their preferences list.
- If the guest is allocated to a non-preferred hotel, a penalty of 0.1 is applied.
- If the guest is not allocated to any hotel, their satisfaction score is 0.
"""

def price_allocation(guests_dict_original, hotels_dict_original):
    """
    ## Parameters: 
     - Dictionary containing guests information: guest_id, discount, preferences list.
     - Dictionary containing hotels information: hotel_id, available_rooms, price.
    ## Returns:
     - Allocation report (dictionary): for each hotel, number of rooms occupied, rooms available, total revenue, list of guests allocated.
     - Unassigned guests (count and list).
     - Overall statistics (dictionary): count of assigned guests, avg satisfaction, couhnt of occupied hotels, avg revenue.
    """   
    # Make copies of the dictionaries to prevent modifying the originals
    guests_dict = guests_dict_original.copy()  # Copy the guest dictionary
    hotels_dict = {k: v.copy() for k, v in hotels_dict_original.items()}  # Deep copy of the hotels dictionary
    
    # 1: sort hotels by price using pandas
    hotels_df = pd.DataFrame(hotels_dict).T  # Transpose to flip the dictionary
    sorted_hotels = hotels_df.sort_values(by='price').index
    
    # Store statistics
    allocation = {}
    hotel_occupancy = {hotel_id: {'occupied_rooms': 0, 'guests': []} for hotel_id in hotels_dict}
    guest_revenues = {} # revenue per guest
    guest_satisfaction = {}  # satisfaction score for each guest
    
    # Step 2: Process guests in ID order
    for guest_id, guest_info in sorted(guests_dict.items()): # sort guests by their ids: reservation order
        preferences = guest_info['preferences'] # retrieve the preferences for each guest
        discount = guest_info.get('discount', 0) # retrieve discount rate for each guest
        allocated = False
        
        for hotel_id in sorted_hotels:
            #Check that the hotel encountered in order of price is in preferences
            if hotel_id in preferences and hotels_dict[hotel_id]['available_rooms'] > 0:
                # Allocate room
                allocation[guest_id] = hotel_id
                hotels_dict[hotel_id]['available_rooms'] -= 1
                hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                hotel_occupancy[hotel_id]['guests'].append(guest_id) # Track which guests were allocated to this hotel
                    
                # Revenue of the hotel for this guest
                discounted_price = hotels_dict[hotel_id]['price'] * (1 - discount)
                guest_revenues[guest_id] = discounted_price # store revenue per guest
                    
                # Satisfaction score
                guest_satisfaction[guest_id] = round((len(preferences) - preferences.index(hotel_id)) / len(preferences), 2)  # Higher score for better match

                allocated = True
                break  # Stop and move to the next guest once allocated
        
        # If no hotel in preferences has available rooms, I allocate based on price
        if not allocated:
            for hotel_id in sorted_hotels:
                if hotels_dict[hotel_id]['available_rooms'] > 0:
                    # Allocate the guest to the cheapest available hotel
                    allocation[guest_id] = hotel_id
                    hotels_dict[hotel_id]['available_rooms'] -= 1
                    hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                    hotel_occupancy[hotel_id]['guests'].append(guest_id)
                    guest_satisfaction[guest_id] = 0.1 # Penalty for being allocated to a hotel outside the preferences

                    allocated = True
                    break
                
        if not allocated:
            guest_satisfaction[guest_id] = 0  # No allocation = 0 satisfaction
            guest_revenues[guest_id] = 0

    # Stats for unassigned guests
    unassigned_count = len([guest_id for guest_id in guests_dict if guest_id not in allocation]) #count how many guests were not assigned
    unassigned_guests = [guest_id for guest_id in guests_dict if guest_id not in allocation] # list to order the ids of unassigned guests (one can see them also from the print)

    # Hotel report
    price_allocation_report = {}

    for hotel_id, data in hotels_dict.items():
        occupied_rooms = hotel_occupancy[hotel_id]['occupied_rooms']
        guests = hotel_occupancy[hotel_id]['guests']
        final_revenue = sum(guest_revenues.get(guest_id, 0) for guest_id in guests)
        
        price_allocation_report[hotel_id] = {
            'rooms_occupied': occupied_rooms,
            'rooms_available': data['available_rooms'],
            'number_of_guests_accommodated': len(guests),
            'revenue': round(final_revenue, 2),
            'guests': guests
        } 
    
    total_assigned_guests = len(allocation)  # Number of guests assigned to hotels

    # Now I have all the details I need to compute total and average revenue
    # Total and overall average revenue
    total_revenues = sum(details['revenue'] for details in price_allocation_report.values())
    occupied_hotels_count = sum(1 for details in price_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0 # don't divide by 0
    
    # Satisfaction score
    total_satisfaction_score = sum(guest_satisfaction.values())
    average_satisfaction_score = round(total_satisfaction_score / len(guests_dict), 2) # I include unassigned guest to penalize the final score

    statistics = {
        'assigned_guests_count': total_assigned_guests,
        'average_satisfaction_score': average_satisfaction_score,
        'occupied_hotels_count': occupied_hotels_count,
        'average_revenue': average_revenue
    }
    
    # Generate visualizations
    fig1 = plot_revenue_distribution(price_allocation_report)
    fig2 = plot_guest_satisfaction_distribution(guest_satisfaction)
    fig3 = plot_guests_per_hotel(price_allocation_report)
    
    # return the results for allocation, guests and hotels.
    return{
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'allocation_report': price_allocation_report,
        'statistics': statistics,
        'plots': [fig1, fig2, fig3]
    }    
    
price_allocation_result = price_allocation(guests_dict_original, hotels_dict_original)


## Needed to pass the report to the main file
def printed_price_allocation_report(price_allocation_result):
    # Directly return the allocation_report dictionary instead of creating a string
    allocation_report = price_allocation_result.get('allocation_report', None)
    return allocation_report  # Just return the allocation report (as a dictionary)


