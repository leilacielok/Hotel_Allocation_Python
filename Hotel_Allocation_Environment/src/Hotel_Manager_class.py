import time
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy


from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Allocation_Methods.Price_Allocation import price_allocation, printed_price_allocation_report
from src.Allocation_Methods.Random_Allocation import random_allocation, print_random_allocation_report
from src.Allocation_Methods.Availability_Allocation import availability_allocation, printed_availability_allocation_report
from src.Allocation_Methods.Reservation_Allocation import reservation_allocation, printed_reservation_allocation_report

# Hotel Manager class
class HotelManager:
    def __init__(self, guests_dict_original, hotels_dict_original):
        self.guests_dict = guests_dict_original # copy the dictionaries, so that I do not modify the original ones
        self.hotels_dict = deepcopy(hotels_dict_original)
        self.results = {} # store all allocations results by method
        self.times = {}
        self.statistics = {}
        
    def reset_hotels(self):
        self.hotels_dict = deepcopy(hotels_dict_original)
    
    def run_random_allocation(self):
        result = random_allocation(self.guests_dict, self.hotels_dict)
        self.statistics['Random'] = result['statistics']  
        self.results['Random'] = result
        # Process the allocation report into a DataFrame
        random_allocation_report_df = self.create_allocation_report_df(result.get('allocation_report', {}))
        
        return {
            'allocation_report': random_allocation_report_df,
            'statistics': result['statistics'],
            'plots': result.get('plots', [])
        }

    def run_reservation_allocation(self):
        result = reservation_allocation(self.guests_dict, self.hotels_dict)
        self.statistics['Reservation'] = result['statistics']  
        self.results['Reservation'] = result    
        reservation_allocation_report_df = self.create_allocation_report_df(result.get('allocation_report', {}))
        return {
            'allocation_report': reservation_allocation_report_df,
            'statistics': result['statistics'],
            'plots': result.get('plots', [])
        }
    
    def run_price_allocation(self):
        result = price_allocation(self.guests_dict, self.hotels_dict)
        self.statistics['Price'] = result['statistics'] 
        self.results['Price'] = result
        price_allocation_report_df = self.create_allocation_report_df(result.get('allocation_report', {}))
        return {
            'allocation_report': price_allocation_report_df,
            'statistics': result['statistics'],
            'plots': result.get('plots', [])
        }
    
    def run_availability_allocation(self):
        result = availability_allocation(self.guests_dict, self.hotels_dict)
        self.statistics['Availability'] = result['statistics'] 
        self.results['Availability'] = result
        availability_allocation_report_df = self.create_allocation_report_df(result.get('allocation_report', {}))
        return {
            'allocation_report': availability_allocation_report_df,
            'statistics': result['statistics'],
            'plots': result.get('plots', [])
        }
    
    def create_allocation_report_df(self, allocation_report):
        """
        This helper method processes the allocation report and returns a DataFrame
        with the necessary hotel data (rooms, revenue, guests, etc.)
        """
        rows = []
        for hotel, data in allocation_report.items():
            row = {
                'Hotel': hotel,
                'Rooms Occupied': data.get('rooms_occupied', 0),
                'Rooms Available': data.get('rooms_available', 0),
                'Number of Guests Accommodated': data.get('number_of_guests_accommodated', 0),
                'Revenue ($)': f"${data.get('revenue', 0):,.2f}",
                'Guests': ', '.join(data.get('guests', []))  # Join guest list into a single string
            }
            rows.append(row)
        return pd.DataFrame(rows) # Standardize every report into a structured dataframe
            
    def run_allocations(self, method_name, method, report_function):
        """Helper method: it runs a singel function and stores the results in the HotelManager instance (self.results, self.times, self.statistics).
        Parameters are the name of the allocation to execute, the allocation function and a function that formats the allocation results 
        (such as print_random_allocation_report).
        It is a generic function for all the individual methods."""
        start_time = time.time()
        result = method(self.guests_dict, self.hotels_dict)
        elapsed_time = time.time() - start_time
        
        self.results[method_name] = result
        self.times[method_name] = elapsed_time
        self.statistics[method_name] = result['statistics']
        
        report = report_function(result)
        return {
                'allocation_report': report,
                'statistics': result['statistics'],
                'plots': result.get('plots', []) # empty list if no plots exist
        }

    def run_all_methods(self): # no input (uses all four methods)
        """runs all allocation methods in sequence and display their results (for each method). 
        It relies on run_allocations to handle each method's execution."""
        methods = {
            "Random": (random_allocation, print_random_allocation_report),
            "Reservation": (reservation_allocation, printed_reservation_allocation_report),
            "Price": (price_allocation, printed_price_allocation_report),
            "Availability": (availability_allocation, printed_availability_allocation_report)
        }
        # calls run_allocation function for every method
        for method_name, (method, report_function) in methods.items(): # iterates over the dictionary running each method with run_allocations
            print(f"\nRunning {method_name} Allocation...")
            self.reset_hotels() # after each allocation resets hotels data to ensure independence
            print(self.run_allocations(method_name, method, report_function))
