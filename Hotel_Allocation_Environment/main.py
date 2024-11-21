import numpy as np
import pandas as pd
import random
from copy import deepcopy
import matplotlib.pyplot as plt
import time

# External functions
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Allocation_Methods.Price_Allocation import price_allocation, printed_price_allocation_report
from src.Allocation_Methods.Random_Allocation import random_allocation, print_random_allocation_report
from src.Allocation_Methods.Availability_Allocation import availability_allocation, printed_availability_allocation_report
from src.Allocation_Methods.Reservation_Allocation import reservation_allocation, printed_reservation_allocation_report
from src.Visualization import plot_execution_times, plot_allocation_comparison

# Hotel Manager class
class HotelManager:
    def __init__(self, guests_dict_original, hotels_dict_original):
        self.guests_dict = guests_dict_original # copy the dictionaries, so that I do not modify the original ones
        self.hotels_dict = deepcopy(hotels_dict_original)
        self.results = {} # store all allocations results by method
        self.times = {}
        
    def reset_hotels(self):
        self.hotels_dict = deepcopy(hotels_dict_original)
    
    def run_random_allocation(self):
        self.results['Random'] = random_allocation(self.guests_dict, self.hotels_dict)
        random_allocation_report = print_random_allocation_report(self.results['Random'])
        return random_allocation_report

    def run_reservation_allocation(self):
        self.results['Reservation'] = reservation_allocation(self.guests_dict, self.hotels_dict)
        reservation_allocation_report = printed_reservation_allocation_report(self.results['Reservation'])
        return reservation_allocation_report
    
    def run_price_allocation(self):
        self.results['Price'] = price_allocation(self.guests_dict, self.hotels_dict)
        price_allocation_report = printed_price_allocation_report(self.results['Price'])
        return price_allocation_report
    
    def run_availability_allocation(self):
        self.results['Availability'] = availability_allocation(self.guests_dict, self.hotels_dict)
        availability_allocation_report = printed_availability_allocation_report(self.results['Availability'])
        return availability_allocation_report
    
    
      # Unified method to run all allocations (needed for data visualization)
    def run_allocations(self, method_name, method, report_function):
        start_time = time.time()
        result = method(self.guests_dict, self.hotels_dict)
        elapsed_time = time.time() - start_time
        
        self.results[method_name] = result
        self.times[method_name] = elapsed_time
        
        report = report_function(result)
        return report

    def run_all_methods(self):
        print("Running Reservation Allocation...")
        self.reset_hotels()
        print(self.run_allocations("Reservation", reservation_allocation, printed_reservation_allocation_report))

        print("\nRunning Price Allocation...")
        self.reset_hotels()
        print(self.run_allocations("Price", price_allocation, printed_price_allocation_report))

        print("\nRunning Random Allocation...")
        self.reset_hotels()
        print(self.run_allocations("Random", random_allocation, print_random_allocation_report))
        
        print("\nRunning Availability Allocation...")
        self.reset_hotels()
        print(self.run_allocations("Availability", availability_allocation, printed_availability_allocation_report))


    
# Main program
if __name__ == "__main__":
    manager = HotelManager(guests_dict_original, hotels_dict_original)
    
    # Run allocation methods
    print("Running Individual Allocations...")
    manager.reset_hotels()
    print(manager.run_reservation_allocation())
    manager.reset_hotels()
    print(manager.run_price_allocation())
    manager.reset_hotels()
    print(manager.run_random_allocation())
    manager.reset_hotels()
    print(manager.run_availability_allocation())

    # Run all methods and measure execution times
    print("\nRunning All Allocations for Visualization...")
    manager.run_all_methods()

    # Visualize results
    print("\nVisualizing Execution Times...")
    plot_execution_times(manager.times)

    print("\nVisualizing Allocation Comparison...")
    plot_allocation_comparison(manager.results, manager.hotels_dict)
    

 