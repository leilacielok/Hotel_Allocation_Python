import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Histogram to visualize the distribution of revenues across hotels
def plot_revenue_distribution(allocation_report):
    hotel_names = list(allocation_report.keys()) # extracts hotel IDs from the allocation report
    revenues = [allocation_report[hotel_name]['revenue'] for hotel_name in hotel_names] # list of revenue values per hotel
    
    # initialize matplotlib figure, use seaborn to create histogram (30 bars with kernel density estimate)
    fig, ax = plt.subplots(figsize=(10, 6)) 
    sns.histplot(revenues, bins=30, kde=True, color='green', edgecolor='black', ax=ax) 
    ax.set_title('Revenue Distribution Across Hotels')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('Number of Hotels')
    return fig # so I can use st.pyplot(fig) in streamlit

# Histogram to visualize the distribution of guest satisfaction across guests
def plot_guest_satisfaction_distribution(guest_satisfaction):
    satisfaction_scores = list(guest_satisfaction.values()) # stores scores per guest
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(satisfaction_scores, bins=30, kde=True, color='orange', edgecolor='black', ax=ax)
    ax.set_title('Guest Satisfaction Distribution')
    ax.set_xlabel('Satisfaction Score')
    ax.set_ylabel('Number of Guests')
    return fig

# Bar chart to visualize the distribution of guests per hotel
def plot_guests_per_hotel(allocation_report):
    # Get the number of guests per hotel
    hotel_guest_counts = [
        allocation_report[hotel_name]['number_of_guests_accommodated'] 
        for hotel_name in allocation_report
    ] # list of the number of guests accommodated per hotel
    
    # Count how many hotels have a specific number of guests.
    guest_count_distribution = Counter(hotel_guest_counts) # dictionary-like object (keys is number of guest, value is how many hotels have that number)
    sorted_guest_counts = sorted(guest_count_distribution.items()) # Sort by the number of guests (x-axis values)
    
    num_guests, num_hotels = zip(*sorted_guest_counts) # separates the sorted pairs of guests and hotels into two lists (hotel with 3 guests // 3 guests)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(num_guests, num_hotels, color='purple') #(x, y, purple bars)
    
    ax.set_xlabel('Number of Guests per Hotel')
    ax.set_ylabel('Number of Hotels')
    ax.set_title('Guests Distribution over Hotels')
    
    return fig
