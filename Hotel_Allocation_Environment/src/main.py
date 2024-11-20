import numpy as np
import pandas as pd
import random
from copy import deepcopy

# External functions
from src.Allocation_Methods.Reservation_Allocation import reservation_allocation, printed_reservation_allocation_report
from src.Allocation_Methods.Price_Allocation import price_allocation, printed_price_allocation_report
from src.Allocation_Methods.Random_Allocation import random_allocation, print_random_allocation_report
from src.Classes_and_Dictionaries.Guests import guests_dict_original
from src.Classes_and_Dictionaries.Hotels import hotels_dict_original

# Hotel Manager class
class HotelManager:
    def __init__(self, guests_dict_original, hotels_dict_original):
        self.guests_dict = guests_dict_original # copy the dictionaries, so that I do not modify the original ones
        self.hotels_dict = deepcopy(hotels_dict_original)
        self.price_allocation_result = None  # To store price allocation result
        self.reservation_allocation_result = None  # To store reservation allocation result
        self.random_allocation_result = None  # To store random allocation result
        
    def reset_hotels(self):
        self.hotels_dict = deepcopy(hotels_dict_original)
    
    def run_random_allocation(self):
        self.random_allocation_result = random_allocation(self.guests_dict, self.hotels_dict)
        random_allocation_report = print_random_allocation_report(self.random_allocation_result)
        return random_allocation_report

    def run_reservation_allocation(self):
        self.reservation_allocation_result = reservation_allocation(self.guests_dict, self.hotels_dict)
        reservation_allocation_report = printed_reservation_allocation_report(self.reservation_allocation_result)
        return reservation_allocation_report
    
    def run_price_allocation(self):
        self.price_allocation_result = price_allocation(self.guests_dict, self.hotels_dict)
        price_allocation_report = printed_price_allocation_report(self.price_allocation_result)
        return price_allocation_report
    
    
    
# Main program: create instance for hotel manager    
if __name__ == "__main__":
    manager = HotelManager(guests_dict_original, hotels_dict_original)

    # Run allocation methods
    print("Running Reservation Allocation...")
    manager.reset_hotels()
    reservation_result = manager.run_reservation_allocation()
    print(reservation_result)

    print("\nRunning Price Allocation...")
    manager.reset_hotels()
    price_result = manager.run_price_allocation()
    print(price_result)

    print("\nRunning Random Allocation...")
    manager.reset_hotels()
    random_result = manager.run_random_allocation()
    print(random_result)
    



        
    