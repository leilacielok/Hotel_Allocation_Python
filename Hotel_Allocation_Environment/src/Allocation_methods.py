# Random Allocation Result
from src.RandomAllocation import random_allocation_result

# Print allocation result
for guest_id, details in random_allocation_result.items():
    print(f"Guest {guest_id}: Assigned to {details['hotel_id']}, Room {details['room_number']}; "
          f"Discount: {details['discount_applied']*100}%, Price Paid: ${details['price_paid']:.2f}")