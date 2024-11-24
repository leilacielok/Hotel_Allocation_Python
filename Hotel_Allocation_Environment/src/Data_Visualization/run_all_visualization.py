import matplotlib.pyplot as plt
import time
import numpy as np

"""
Function to measure execution time of a method: stores the results and time taken (dictionaries)
Input: 
- method_name: name of the allocation method being timed;
- method: the actual function to execute;
- results_dict: dictionary to store the results of the methods. Method's name as key, result as value.
- times_dict: dictionary to store the time it took for each method to run. Method's name as key, time elapsed as value.
"""
def measure_execution_time(method_name, method, results_dict, times_dict):
    start_time = time.time() # captures current time (in seconds) <- before running the method
    result = method() # executes the method and store the result 
    elapsed_time = time.time() - start_time # captures current time and subtracts the start time
    results_dict[method_name] = result 
    times_dict[method_name] = elapsed_time # needed for the plot
    return result

# Function to plot execution times: bar chart of the execution times for allocation methods.
def plot_execution_times(times_dict):
    methods = list(times_dict.keys()) # separate keys (x axis) and values (y axis)
    times = list(times_dict.values())   
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(methods, times, color='skyblue')
    ax.set_xlabel('Allocation Methods')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Comparison of Execution Times for Allocation Methods')
    return fig


""" 
Compare statistics across the allocation methods: the parameter is the list of the statistics dictionaries of the 4 methods
Keys are the guests count, the avg satisfaction, the hotels count, the avg revenue."""
def statistics_comparison(statistics_dicts):
    allocation_methods = ['Random', 'Reservation', 'Price', 'Availability'] # Define the names of the methods
    x = np.arange(len(allocation_methods))  # x axis: bars for each method
    width = 0.5  # width of the bars 
    
    # Extract the values for each statistic dynamically from the list of dictionaries
    assigned_guests_counts = [statistics_dict['assigned_guests_count'] for statistics_dict in statistics_dicts]
    avg_satisfaction_scores = [statistics_dict['average_satisfaction_score'] for statistics_dict in statistics_dicts]
    occupied_hotels_counts = [statistics_dict['occupied_hotels_count'] for statistics_dict in statistics_dicts]
    avg_revenues = [statistics_dict['average_revenue'] for statistics_dict in statistics_dicts]
        
    # Create subplots: 4 separate plots, one for each statistic
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 2x2 grid of subplots
    axs = axs.flatten()  # Flatten the 2D array of axes to 1D for easier indexing

    # Bar chart for Assigned Guests Count
    bars = axs[0].bar(x, assigned_guests_counts, width, color='b', label = 'Assigned Guests Count')
    axs[0].set_title('Assigned Guests Count by Allocation Method')
    axs[0].set_xlabel('Allocation Method')
    axs[0].set_ylabel('Assigned Guests Count')
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(allocation_methods)
    axs[0].legend()
    for bar, value in zip(bars, assigned_guests_counts):
        axs[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value}", ha='center', va='bottom')

    # Bar chart for Average Satisfaction Score
    bars = axs[1].bar(x, avg_satisfaction_scores, width, color='r', label='Avg Satisfaction Score')
    axs[1].set_title('Average Satisfaction Score by Allocation Method')
    axs[1].set_xlabel('Allocation Method')
    axs[1].set_ylabel('Average Satisfaction Score')
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(allocation_methods)
    axs[1].legend()
    for bar, value in zip(bars, avg_satisfaction_scores):
        axs[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha='center', va='bottom')
        
    # Bar chart for Occupied Hotels Count
    bars = axs[2].bar(x, occupied_hotels_counts, width, color='g', label='Occupied Hotels Count')
    axs[2].set_title('Occupied Hotels Count by Allocation Method')
    axs[2].set_xlabel('Allocation Method')
    axs[2].set_ylabel('Occupied Hotels Count')
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(allocation_methods)
    axs[2].legend()
    for bar, value in zip(bars, occupied_hotels_counts):
        axs[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value}", ha='center', va='bottom')

    # Bar chart for Average Revenue
    bars = axs[3].bar(x, avg_revenues, width, color='orange', label = 'Average Revenue')
    axs[3].set_title('Average Revenue by Allocation Method')
    axs[3].set_xlabel('Allocation Method')
    axs[3].set_ylabel('Average Revenue')
    axs[3].set_xticks(x)
    axs[3].set_xticklabels(allocation_methods)
    axs[3].legend()
    for bar, value in zip(bars, avg_revenues):
            axs[3].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha='center', va='bottom')

    # Adjust layout for a clean display (no overlapping between the plots)
    fig.tight_layout()

    return fig

