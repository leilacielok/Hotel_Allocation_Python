import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Random function visualization: Create a new figure for each plot to avoid reusing the same figure
def plot_revenue_distribution(allocation_report):
    hotel_names = list(allocation_report.keys())
    revenues = [allocation_report[hotel_name]['revenue'] for hotel_name in hotel_names]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(revenues, bins=30, kde=True, color='green', edgecolor='black', ax=ax)
    ax.set_title('Revenue Distribution Across Hotels')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('Number of Hotels')
    return fig

def plot_guest_satisfaction_distribution(guest_satisfaction):
    satisfaction_scores = list(guest_satisfaction.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(satisfaction_scores, bins=30, kde=True, color='orange', edgecolor='black', ax=ax)
    ax.set_title('Guest Satisfaction Distribution')
    ax.set_xlabel('Satisfaction Score')
    ax.set_ylabel('Number of Guests')
    return fig

def plot_guests_per_hotel(allocation_report):
    # Get the number of guests per hotel
    hotel_guest_counts = [
        allocation_report[hotel_name]['number_of_guests_accommodated'] 
        for hotel_name in allocation_report
    ]
    
    # Count how many hotels have 1 guest, 2 guests, 3 guests, etc.
    guest_count_distribution = Counter(hotel_guest_counts)
    # Sort by the number of guests (x-axis values)
    sorted_guest_counts = sorted(guest_count_distribution.items())
    
    num_guests, num_hotels = zip(*sorted_guest_counts)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(num_guests, num_hotels, color='purple')
    
    ax.set_xlabel('Number of Guests per Hotel')
    ax.set_ylabel('Number of Hotels')
    ax.set_title('Guests Distribution over Hotels')
    
    return fig
