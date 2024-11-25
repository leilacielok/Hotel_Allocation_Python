import pandas as pd
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Data_Visualization.individual_visualization import (
    plot_revenue_distribution,
    plot_guest_satisfaction_distribution,
    plot_guests_per_hotel,
    group_hotels_by_rooms,
    plot_revenue_by_room_category
)

def availability_allocation(guests_dict_original, hotels_dict_original):
    """
    ## Parameters: 
     - Dictionary containing guests information: guest_id, discount, preferences list.
     - Dictionary containing hotels information: hotel_id, available_rooms, price.
    ## Returns:
     - Allocation report (dictionary): for each hotel, number of rooms occupied, rooms available, total revenue, list of guests allocated.
     - Unassigned guests (count and list).
     - Overall statistics (dictionary): count of assigned guests, avg satisfaction, couhnt of occupied hotels, avg revenue.
    """
    # Make copies of the dictionaries to prevent the function from modifying the originals
    guests_dict = guests_dict_original.copy()  # Copy the guest dictionary
    hotels_dict = {k: v.copy() for k, v in hotels_dict_original.items()}  # Deep copy of the hotels dictionary
    
    # Sort hotels by available rooms in descending order (starting from most roomy)
    hotels_df = pd.DataFrame(hotels_dict).T  
    sorted_hotels = hotels_df.sort_values(by='available_rooms', ascending=False).index  
    
    # Store statistics: result of the allocation, initialize hotel occupancy, revenue per guest, satisfaction score per guest.
    allocation = {}
    hotel_occupancy = {hotel_id: {'occupied_rooms': 0, 'guests': []} for hotel_id in hotels_dict}
    guest_revenues = {}  
    guest_satisfaction = {}  
    
    # Process guests in ID order (reservation order): sort by guest_id, retrieve preferences list and discount rate.
    for guest_id, guest_info in sorted(guests_dict.items()): 
        preferences = guest_info['preferences'] 
        discount = guest_info.get('discount', 0) 
        allocated = False
        
        # Considering sorted hotels in order of price, allocate each guest to a preferred hotel with available rooms
        # If a match is found, the room is allocated, hotel stats are updated, and guest satisfaction is calculated.
        for hotel_id in sorted_hotels:
            if hotel_id in preferences and hotels_dict[hotel_id]['available_rooms'] > 0:
                
                allocation[guest_id] = hotel_id
                hotels_dict[hotel_id]['available_rooms'] -= 1
                hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                hotel_occupancy[hotel_id]['guests'].append(guest_id)  # Track guests allocated to this hotel
                
                # Revenue of the hotel for this guest
                discounted_price = hotels_dict[hotel_id]['price'] * (1 - discount)
                guest_revenues[guest_id] = discounted_price  # Store revenue per guest
                
                guest_satisfaction[guest_id] = round((len(preferences) - preferences.index(hotel_id)) / len(preferences), 2)  # Higher score for better match

                allocated = True
                break  # Stop and move to the next guest once allocated
   
        # If no hotel in preferences has available rooms, allocate based on availability order.
        # In this case, guests' satisfaction scores suffer a penalty for being allocated outside preferences.
        if not allocated:
            for hotel_id in sorted_hotels:
                if hotels_dict[hotel_id]['available_rooms'] > 0:
                    # Allocate the guest to the hotel with the most available rooms
                    allocation[guest_id] = hotel_id
                    hotels_dict[hotel_id]['available_rooms'] -= 1
                    hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                    hotel_occupancy[hotel_id]['guests'].append(guest_id)
                    guest_satisfaction[guest_id] = 0.1

                    allocated = True
                    break
        
        # Guests not allocated any room receive a satisfaction score of 0       
        if not allocated:
            guest_satisfaction[guest_id] = 0  
            guest_revenues[guest_id] = 0

    # Stats for assigned unassigned guests: count and list.
    unassigned_count = len([guest_id for guest_id in guests_dict if guest_id not in allocation]) 
    unassigned_guests = [guest_id for guest_id in guests_dict if guest_id not in allocation]  
    total_assigned_guests = len(allocation)  

    # Stats for hotel report (calculated for each hotel after the allocation process)
    availability_allocation_report = {}

    for hotel_id, data in hotels_dict.items():
        occupied_rooms = hotel_occupancy[hotel_id]['occupied_rooms']
        guests = hotel_occupancy[hotel_id]['guests']
        final_revenue = sum(guest_revenues.get(guest_id, 0) for guest_id in guests)
        
        availability_allocation_report[hotel_id] = {
            'rooms_occupied': occupied_rooms,
            'rooms_available': data['available_rooms'],
            'number_of_guests_accommodated': len(guests),
            'revenue': round(final_revenue, 2),
            'guests': guests
        }
    
    # Total and average revenue of the allocation method
    total_revenues = sum(details['revenue'] for details in availability_allocation_report.values())
    occupied_hotels_count = sum(1 for details in availability_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0  # Avoid division by zero
    
    # Satisfaction score
    total_satisfaction_score = sum(guest_satisfaction.values())
    average_satisfaction_score = round(total_satisfaction_score / len(guests_dict), 2)  # Include unassigned guests to penalize the score

    statistics = {
        'assigned_guests_count': total_assigned_guests,
        'average_satisfaction_score': average_satisfaction_score,
        'occupied_hotels_count': occupied_hotels_count,
        'average_revenue': average_revenue
    }
    
    df_grouped = group_hotels_by_rooms(availability_allocation_report, hotels_dict_original)

    # Generate visualizations
    fig1 = plot_revenue_distribution(availability_allocation_report)
    fig2 = plot_guest_satisfaction_distribution(guest_satisfaction)
    fig3 = plot_guests_per_hotel(availability_allocation_report)
    fig4 = plot_revenue_by_room_category(df_grouped)
    
    # Return results for allocation, guests, and hotels
    return {
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'allocation_report': availability_allocation_report,
        'statistics': statistics,
        'plots': [fig1, fig2, fig3, fig4]
    }
    
# Store the function
availability_allocation_result = availability_allocation(guests_dict_original, hotels_dict_original)

# Needed to pass the report to the main file
def printed_availability_allocation_report(availability_allocation_result):
    # Get the allocation report directly from the result
    allocation_report = availability_allocation_result.get('allocation_report', None)
    
    # Instead of converting it to a string, just return the dictionary
    return allocation_report  # Return the allocation report as a dictionary, not a string


