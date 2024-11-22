import pandas as pd
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original

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
            'final_revenue': round(final_revenue, 2),
            'guests': guests
        }
    
    # Total and average revenue of the allocation method
    total_revenues = sum(details['final_revenue'] for details in availability_allocation_report.values())
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
    
    # Return results for allocation, guests, and hotels
    return {
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'availability_allocation_report': availability_allocation_report,
        'statistics': statistics,
    }

# Store the function
availability_allocation_result = availability_allocation(guests_dict_original, hotels_dict_original)

def printed_availability_allocation_report(availability_allocation_result):
    # Print Unassigned Guests 
    print("\nUnassigned Guests:")
    print(f"  {availability_allocation_result['unassigned_count']} guests were not assigned to any hotel.")
    print(f"  Unassigned Guests List: {availability_allocation_result['unassigned_guests']}")
    
    # Print details for each hotel: Remaining Rooms, Occupied Rooms, and Revenue
    print("\nHotel Room Allocation and Revenue:")
    for hotel_id, report in availability_allocation_result['availability_allocation_report'].items():
        print(f"\n{hotel_id}:")
        print(f"  Remaining Rooms: {report['rooms_available']}")
        print(f"  Occupied Rooms: {report['rooms_occupied']}")
        print(f"  Revenue: {report['final_revenue']}")
        print(f"  Assigned Guests: {report['guests']}")  # Printing the list of assigned guests

    # Print the overall statistics
    print("\nOverall Statistics:")
    print(f"Total number of guests assigned: {availability_allocation_result['statistics']['assigned_guests_count']}")
    print(f"Overall average degree of satisfaction: {availability_allocation_result['statistics']['average_satisfaction_score']:.2f}")
    print(f"Total number of hotels occupied: {availability_allocation_result['statistics']['occupied_hotels_count']}")
    print(f"Overall average revenue per hotel: {availability_allocation_result['statistics']['average_revenue']:.2f}")

# Store printed output (improved readability)
printed_availability_allocation_report(availability_allocation_result)