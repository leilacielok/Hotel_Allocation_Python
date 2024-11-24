import matplotlib.pyplot as plt
import time
import numpy as np

# Function to measure execution time of a method: stores the results and time taken (dictionaries)
def measure_execution_time(method_name, method, results_dict, times_dict):
    start_time = time.time()
    result = method()
    elapsed_time = time.time() - start_time
    results_dict[method_name] = result # method names as keys and allocation results as values.
    times_dict[method_name] = elapsed_time # method names as keys and execution times as values.
    return result

# Function to plot execution times: bar chart of the execution times for allocation methods.
def plot_execution_times(times_dict):
    methods = list(times_dict.keys())
    times = list(times_dict.values())
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(methods, times, color='skyblue')
    ax.set_xlabel('Allocation Methods')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Comparison of Execution Times for Allocation Methods')

    return fig

# Function to compare allocation results: line chart comparing allocation results across different methods.
def time_comparison(results_dict, hotels_dict):
    hotels = list(hotels_dict.keys())
    allocation_counts = {method: [0] * len(hotels) for method in results_dict}

    for method, result in results_dict.items():
        for guest, hotel in result.items():
            hotel_index = hotels.index(hotel)
            allocation_counts[method][hotel_index] += 1

    # Plot
    plt.figure(figsize=(10, 6))
    for method, counts in allocation_counts.items():
        plt.plot(hotels, counts, label=method)

    plt.xlabel('Hotels')
    plt.ylabel('Number of Guests')
    plt.title('Allocation Comparison Across Methods')
    plt.legend()


## Compare statistics across the allocation methods: the parameter is the list of the statistics dictionaries of the 4 methods
# Keys are the guests count, the avg satisfaction, the hotels count, the avg revenue.
def statistics_comparison(statistics_dicts):
    allocation_methods = ['Random', 'Reservation', 'Price', 'Availability']  
    x = np.arange(len(allocation_methods))  # x axis labels (allocation methods)
    width = 0.5  # width of the bars for each statistic
    
    # Extract values for each statistic dynamically from the list of dictionaries
    assigned_guests_counts = [statistics_dict['assigned_guests_count'] for statistics_dict in statistics_dicts]
    avg_satisfaction_scores = [statistics_dict['average_satisfaction_score'] for statistics_dict in statistics_dicts]
    occupied_hotels_counts = [statistics_dict['occupied_hotels_count'] for statistics_dict in statistics_dicts]
    avg_revenues = [statistics_dict['average_revenue'] for statistics_dict in statistics_dicts]
        
    # Create subplots: 4 separate plots, one for each statistic
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 2 rows, 2 columns for 4 plots
    axs = axs.flatten()  # Flatten the 2D array of axes to 1D for easier indexing

    # Plot for Assigned Guests Count
    bars = axs[0].bar(x, assigned_guests_counts, width, color='b', label = 'Assigned Guests Count')
    axs[0].set_title('Assigned Guests Count by Allocation Method')
    axs[0].set_xlabel('Allocation Method')
    axs[0].set_ylabel('Assigned Guests Count')
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(allocation_methods)
    axs[0].legend()
    for bar, value in zip(bars, assigned_guests_counts):
        axs[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value}", ha='center', va='bottom')

    # Plot for Average Satisfaction Score
    bars = axs[1].bar(x, avg_satisfaction_scores, width, color='r', label='Avg Satisfaction Score')
    axs[1].set_title('Average Satisfaction Score by Allocation Method')
    axs[1].set_xlabel('Allocation Method')
    axs[1].set_ylabel('Average Satisfaction Score')
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(allocation_methods)
    axs[1].legend()
    for bar, value in zip(bars, avg_satisfaction_scores):
        axs[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha='center', va='bottom')
        
    # Plot for Occupied Hotels Count
    bars = axs[2].bar(x, occupied_hotels_counts, width, color='g', label='Occupied Hotels Count')
    axs[2].set_title('Occupied Hotels Count by Allocation Method')
    axs[2].set_xlabel('Allocation Method')
    axs[2].set_ylabel('Occupied Hotels Count')
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(allocation_methods)
    axs[2].legend()
    for bar, value in zip(bars, occupied_hotels_counts):
        axs[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value}", ha='center', va='bottom')

    # Plot for Average Revenue
    bars = axs[3].bar(x, avg_revenues, width, color='orange', label = 'Average Revenue')
    axs[3].set_title('Average Revenue by Allocation Method')
    axs[3].set_xlabel('Allocation Method')
    axs[3].set_ylabel('Average Revenue')
    axs[3].set_xticks(x)
    axs[3].set_xticklabels(allocation_methods)
    axs[3].legend()
    for bar, value in zip(bars, avg_revenues):
            axs[3].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha='center', va='bottom')

    # Adjust layout for a clean display
    fig.tight_layout()
    
    return fig

