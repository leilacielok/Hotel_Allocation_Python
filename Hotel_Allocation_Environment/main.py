import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
plt.switch_backend('Agg')

# External objects and functions
from src.Guests_Hotels_Dictionaries.Guests import guests_dict_original
from src.Guests_Hotels_Dictionaries.Hotels import hotels_dict_original
from src.Hotel_Manager_class import HotelManager
from src.Data_Visualization.run_all_visualization import plot_execution_times, statistics_comparison

# Main program: Streamlit App
if __name__ == "__main__":
    st.title("Hotel Guest Allocation System")
    st.markdown("""
            ### About the Application
            Welcome to the **Hotel Guest Allocation System**!
            
            This application allows you to allocate customers to hotels based on four different methods: 
            - **Random**: assigns guests randomly to hotels; 
            - **Reservation**: assign guests based on order of reservation;
            - **Price**: from the cheapest hotel to the most expensive one; 
            - **Availability**: from the most roomy hotel, down to the hotel with fewer rooms.
            
            The last three methods take into account also the personal preferences of each customer, and allocate them accordingly.
            Each customer occupies exactly one room, and each stay lasts only one night. The total revenue per hotel is given by the unit price of the room discounted by the fraction of the discount to which the corresponding customer is entitled.
            Some data visualization is there to help you to better understand the different allocation methods, and to compare them.
            
            _Use the sidebar to view the allocation returned from the method you'd like to explore, or run all methods for comparison!_  
            """)
    # Create an instance of the HotelManager class: it can access all allocation methods
    manager = HotelManager(guests_dict_original, hotels_dict_original) 
    
    # Sidebar options (dropdown menu from which the user can choose what allocation method to use)
    # Store the selection in allocation_method
    st.sidebar.title("Choose Allocation Method")
    allocation_method = st.sidebar.selectbox("Select Method", 
                                             ["Random", "Reservation", "Price", "Availability", "Run All"])
    
    if st.sidebar.button("Run Allocation"):
        if allocation_method == "Run All":
            manager.run_all_methods() # function from Hotel_Manager class to run all methods
            st.write("All methods executed. Check the visualizations below.")

            # Display the statistics in a table format: create a DataFrame for statistics
            statistics_df = pd.DataFrame.from_dict(manager.statistics, orient='index') # manager.statistics is a dictionary: the keys become row indexes (the methods)
            times_series = pd.Series(manager.times, name="execution_time") # series that stores executions times for methods
            statistics_df["execution_time"] = times_series # add also the execution times to the dataframe
            
            # Display the statistics as a table
            st.subheader("Statistics Summary")
            st.table(statistics_df) # display the dataframe as a table

            # Display execution time and statistics plots
            st.subheader("Execution Times Across Allocation Methods")
            st.pyplot(plot_execution_times(manager.times)) # manager.times is the input to the plot_execution_times function
            
            st.subheader("Statistics Comparison Across Allocation Methods")
            st.pyplot(statistics_comparison(list(manager.statistics.values())))
            
        else:
            # Map method to the corresponding function of the manager object.
            # Selecting the option 'Random' refers to the run_random_allocation method of manager.
            method_mapping = {
                "Random": manager.run_random_allocation,
                "Reservation": manager.run_reservation_allocation,
                "Price": manager.run_price_allocation,
                "Availability": manager.run_availability_allocation
            }
            if allocation_method in method_mapping: # additional check
                result = method_mapping[allocation_method]() # store result of the corresponding function
                
                # Allocation report
                st.subheader(f"{allocation_method} Allocation Report")
                allocation_report = result.get('allocation_report', None) # extracts the allocation_report of the selected method
                st.dataframe(allocation_report)  # Directly display the DataFrame.
                
                # Overall statistics
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
                    st.write("No visualizations available for this method.") # additional check
                    
                    
        
