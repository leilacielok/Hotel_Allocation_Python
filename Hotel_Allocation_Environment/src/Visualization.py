import matplotlib.pyplot as plt
import time

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

    plt.figure(figsize=(8, 6))
    plt.bar(methods, times, color='skyblue')
    plt.xlabel('Allocation Methods')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Comparison of Execution Times for Allocation Methods')
    plt.show()

# Function to compare allocation results: line chart comparing allocation results across different methods.
def plot_allocation_comparison(results_dict, hotels_dict):
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
    plt.show()
    
## Heatmap for allocation density
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Create DataFrame for heatmap

