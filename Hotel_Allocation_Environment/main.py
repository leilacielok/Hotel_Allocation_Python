import streamlit as st
from copy import deepcopy
import matplotlib.pyplot as plt
import time
import pandas as pd
plt.switch_backend('Agg')

# External functions
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Allocation_Methods.Price_Allocation import price_allocation, printed_price_allocation_report
from src.Allocation_Methods.Random_Allocation import random_allocation, print_random_allocation_report
from src.Allocation_Methods.Availability_Allocation import availability_allocation, printed_availability_allocation_report
from src.Allocation_Methods.Reservation_Allocation import reservation_allocation, printed_reservation_allocation_report
from src.Visualization import plot_execution_times, statistics_comparison

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
        return pd.DataFrame(rows)
            
    # Unified method to run all allocations (needed for data visualization)
    def run_allocations(self, method_name, method, report_function):
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

    def run_all_methods(self):
        methods = {
            "Random": (random_allocation, print_random_allocation_report),
            "Reservation": (reservation_allocation, printed_reservation_allocation_report),
            "Price": (price_allocation, printed_price_allocation_report),
            "Availability": (availability_allocation, printed_availability_allocation_report)
        }

        for method_name, (method, report_function) in methods.items():
            print(f"\nRunning {method_name} Allocation...")
            self.reset_hotels()
            print(self.run_allocations(method_name, method, report_function))

    
# Main program: Streamlit App
if __name__ == "__main__":
    st.title("Hotel Guests Allocation System")
    manager = HotelManager(guests_dict_original, hotels_dict_original)
    
    # Sidebar options (the user can choose which allocation method to use)
    st.sidebar.title("Choose Allocation Method")
    allocation_method = st.sidebar.selectbox("Select Method", 
                                             ["Random", "Reservation", "Price", "Availability", "Run All"])
    
    if st.sidebar.button("Run Allocation"):
        if allocation_method == "Run All":
            manager.run_all_methods()
            st.write("All methods executed. Check the visualizations below.")

            # Display the statistics in a table format: create a DataFrame for statistics
            statistics_df = pd.DataFrame.from_dict(manager.statistics, orient='index')
            times_series = pd.Series(manager.times, name="execution_time")
            statistics_df["execution_time"] = times_series
            
            # Display the statistics as a table
            st.subheader("Statistics Summary")
            st.table(statistics_df)

            # Display execution time and statistics plots
            st.subheader("Execution Times Across Allocation Methods")
            st.pyplot(plot_execution_times(manager.times))
            
            st.subheader("Statistics Comparison Across Allocation Methods")
            st.pyplot(statistics_comparison(list(manager.statistics.values())))
            
        else:
            # Map method to function
            method_mapping = {
                "Random": manager.run_random_allocation,
                "Reservation": manager.run_reservation_allocation,
                "Price": manager.run_price_allocation,
                "Availability": manager.run_availability_allocation
            }
            if allocation_method in method_mapping:
                result = method_mapping[allocation_method]()
                st.subheader(f"{allocation_method} Allocation Report")
                
                allocation_report = result.get('allocation_report', None)
                
                st.dataframe(allocation_report)  # Directly display the DataFrame
                
                st.subheader(f"{allocation_method} Statistics")
                st.write(f"Assigned Guests Count: {result['statistics']['assigned_guests_count']}")
                st.write(f"Average Satisfaction Score: {result['statistics']['average_satisfaction_score']}")
                st.write(f"Occupied Hotels Count: {result['statistics']['occupied_hotels_count']}")
                st.write(f"Average Revenue: {result['statistics']['average_revenue']}")
                
                st.subheader(f"{allocation_method} Allocation Visualizations")
                plots = result.get('plots', [])
                if plots:
                    for fig in plots:
                        st.pyplot(fig)
                else:
                    st.write("No visualizations available for this method.")
                    
        
