import pandas as pd
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original

def availability_allocation(guests_dict_original, hotels_dict_original):
    
    # Make copies of the dictionaries to prevent modifying the originals
    guests_dict = guests_dict_original.copy()  # Copy the guest dictionary
    hotels_dict = {k: v.copy() for k, v in hotels_dict_original.items()}  # Deep copy of the hotels dictionary
    
    # 1: Sort hotels by available rooms in descending order
    hotels_df = pd.DataFrame(hotels_dict).T  # Transpose to flip the dictionary
    sorted_hotels = hotels_df.sort_values(by='available_rooms', ascending=False).index  # Sort by available rooms
    
    # Store statistics
    allocation = {}
    hotel_occupancy = {hotel_id: {'occupied_rooms': 0, 'guests': []} for hotel_id in hotels_dict}
    guest_revenues = {}  # Revenue per guest
    guest_satisfaction = {}  # Satisfaction score for each guest
    
    # Step 2: Process guests in ID order (reservation order)
    for guest_id, guest_info in sorted(guests_dict.items()): # sort guests by their ids: reservation order
        preferences = guest_info['preferences'] # Retrieve the preferences for each guest
        discount = guest_info.get('discount', 0) # Retrieve discount rate for each guest
        allocated = False
        
        for hotel_id in sorted_hotels:
            # Check if the hotel encountered in order of availability is in preferences
            if hotel_id in preferences and hotels_dict[hotel_id]['available_rooms'] > 0:
                # Allocate room
                allocation[guest_id] = hotel_id
                hotels_dict[hotel_id]['available_rooms'] -= 1
                hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                hotel_occupancy[hotel_id]['guests'].append(guest_id)  # Track guests allocated to this hotel
                
                # Revenue of the hotel for this guest
                discounted_price = hotels_dict[hotel_id]['price'] * (1 - discount)
                guest_revenues[guest_id] = discounted_price  # Store revenue per guest
                
                # Satisfaction score
                guest_satisfaction[guest_id] = round((len(preferences) - preferences.index(hotel_id)) / len(preferences), 2)  # Higher score for better match

                allocated = True
                break  # Stop and move to the next guest once allocated
        
        # If no hotel in preferences has available rooms, allocate based on availability order
        if not allocated:
            for hotel_id in sorted_hotels:
                if hotels_dict[hotel_id]['available_rooms'] > 0:
                    # Allocate the guest to the hotel with the most available rooms
                    allocation[guest_id] = hotel_id
                    hotels_dict[hotel_id]['available_rooms'] -= 1
                    hotel_occupancy[hotel_id]['occupied_rooms'] += 1
                    hotel_occupancy[hotel_id]['guests'].append(guest_id)
                    guest_satisfaction[guest_id] = 0.1  # Penalty for being allocated outside preferences

                    allocated = True
                    break
                
        if not allocated:
            guest_satisfaction[guest_id] = 0  # No allocation = 0 satisfaction
            guest_revenues[guest_id] = 0

    # Stats for unassigned guests
    unassigned_count = len([guest_id for guest_id in guests_dict if guest_id not in allocation])  # Count unassigned guests
    unassigned_guests = [guest_id for guest_id in guests_dict if guest_id not in allocation]  # List unassigned guest ids

    # Hotel report
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
    
    total_assigned_guests = len(allocation)  # Number of guests assigned to hotels

    # Now compute total and average revenue
    total_revenues = sum(details['final_revenue'] for details in availability_allocation_report.values())
    occupied_hotels_count = sum(1 for details in availability_allocation_report.values() if details['number_of_guests_accommodated'] > 0)
    average_revenue = round(total_revenues / occupied_hotels_count, 2) if occupied_hotels_count > 0 else 0  # Avoid division by zero
    
    # Satisfaction score
    total_satisfaction_score = sum(guest_satisfaction.values())
    average_satisfaction_score = round(total_satisfaction_score / len(guests_dict), 2)  # Include unassigned guests to penalize the score

    # Return results for allocation, guests, and hotels
    return {
        'allocation': allocation,
        'unassigned_guests': unassigned_guests,
        'unassigned_count': unassigned_count,
        'assigned_guests_count': total_assigned_guests,
        'occupied_hotels_count': occupied_hotels_count,
        'remaining_rooms': {hotel_id: hotels_dict[hotel_id]['available_rooms'] for hotel_id in hotels_dict},
        'availability_allocation_report': availability_allocation_report,
        'average_revenue': average_revenue,
        'guest_satisfaction': guest_satisfaction,
        'average_satisfaction_score': average_satisfaction_score
    }

# Test the function
availability_allocation_result = availability_allocation(guests_dict_original, hotels_dict_original)

def printed_availability_allocation_report(availability_allocation_result):
    # Print Unassigned Guests 
    print("\nUnassigned Guests:")
    print(f"  {availability_allocation_result['unassigned_count']} guests were not assigned to any hotel.")
    print(f"  Unassigned Guests List: {availability_allocation_result['unassigned_guests']}")
    
    # Print guests' satisfaction scores
    print("\nCustomer Satisfaction Scores:")
    for guest_id, satisfaction_score in availability_allocation_result['guest_satisfaction'].items():
        print(f"  Guest {guest_id}: Satisfaction Score = {satisfaction_score}")

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
    print(f"Total number of guests assigned: {availability_allocation_result['assigned_guests_count']}")
    print(f"Overall average degree of satisfaction: {availability_allocation_result['average_satisfaction_score']}")
    print(f"Total number of hotels occupied: {availability_allocation_result['occupied_hotels_count']}")
    print(f"Overall average revenue per hotel: {availability_allocation_result['average_revenue']:.2f}")

printed_availability_allocation_report(availability_allocation_result)