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
                    
        
