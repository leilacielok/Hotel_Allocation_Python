# First, Hotels are sorted by price, ensuring cheaper options are considered first.
# Guests are processed in the natural order of their IDs, so in order of reservation.
# Preference Matching: For each guest, I iterate through their preferences to find the first available room in their order of priorities.
# Once a room is allocated I can move to the next guest.

import pandas as pd
from src.Classes_and_Dictionaries.Guests import guests_dict
from src.Classes_and_Dictionaries.Hotels import hotels_dict

def price_allocation(guests_dict, hotels_dict):
    
    # 1: sort hotels by price using pandas
    hotels_df = pd.DataFrame(hotels_dict).T  # Transpose to flip the dictionary
    sorted_hotels = hotels_df.sort_values(by='price').index
    
    # Store statistics
    allocation = {}
    hotel_occupancy = {hotel_id: {'occupied_rooms': 0, 'guests': []} for hotel_id in hotels_dict}
    guest_revenues = {} # revenue per guest
    
    # Step 2: Process guests in ID order
    for guest_id, guest_info in sorted(guests_dict.items()): # sort guests by their ids: reservation order
        preferences = guest_info['preferences'] # retrieve the preferences for each guest
        discount = guest_info.get('discount', 0) # retrieve discount rate for each guest
        allocated = False
        
        for hotel_id in sorted_hotels:
            #Check that the hotel encountered in order of price is in preferences
            if hotel_id in preferences:
                # Check if hotel has available rooms
                if hotels_dict[hotel_id]['available_rooms'] > 0:
                    # Allocate room
                    allocation[guest_id] = hotel_id
                    hotels_dict[hotel_id]['available_rooms'] -= 1
                    hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                    hotel_occupancy[hotel_id]['guests'].append(guest_id) # Track which guests were allocated to this hotel
                    
                    # Revenue of the hotel for this guest
                    discounted_price = hotels_dict[hotel_id]['price'] * (1 - discount)
                    guest_revenues[guest_id] = discounted_price # store revenue per guest
                    
                    allocated = True
                    break  # Stop and move to the next guest once allocated
        
        if not allocated:
            print(f"No allocation for {guest_id}")
    
    # Stats for unassigned guests
    unassigned_count = len([guest_id for guest_id in guests_dict if guest_id not in allocation]) #count how many guests were not assigned
    unassigned_guests = [guest_id for guest_id in guests_dict if guest_id not in allocation] # list to order the ids of unassigned guests (one can see them also from the print)

    # Hotel report
    price_allocation_report = {}

    for hotel_id, data in hotels_dict.items():
        occupied_rooms = hotel_occupancy[hotel_id]['occupied_rooms']
        guests = hotel_occupancy[hotel_id]['guests']
        final_revenue = sum(guest_revenues[guest_id] for guest_id in guests)
        
        price_allocation_report[hotel_id] = {
            'rooms_occupied': occupied_rooms,
            'rooms_available': data['available_rooms'],
            'number_of_guests_accommodated': len(guests),
            'final_revenue': round(final_revenue, 2),
            'guests': guests
        } 
    
    # Now I have all the details I need to compute total and average revenue
    # Total and overall average revenue
    total_revenues = sum(details['final_revenue'] for details in price_allocation_report.values())
    occupied_hotels_count = sum(1 for details in price_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0 # don't divide by 0
    
    # return the results for allocation, guests and hotels.
    return{
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'occupied_hotels_count': occupied_hotels_count,
        'remaining_rooms': {hotel_id: hotels_dict[hotel_id]['available_rooms'] for hotel_id in hotels_dict},
        'price_allocation_report': price_allocation_report,
        'average_revenue': average_revenue
    }    
    
price_allocation_result = price_allocation(guests_dict, hotels_dict)

def printed_price_allocation_report(price_allocation_report):   
    print("\nPrice Allocation Report:")
    for hotel_id, report in price_allocation_result['price_allocation_report'].items():
        print(f"\n{hotel_id}:")
        for key, value in report.items():
            print(f"  {key.replace('_', ' ').capitalize()}: {value}")

# printed_price_allocation_report(price_allocation_result['price_allocation_report'])
