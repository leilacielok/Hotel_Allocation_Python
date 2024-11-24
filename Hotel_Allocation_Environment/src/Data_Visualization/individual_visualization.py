import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

# Availability plot: group by room availability and see if the revenue changes
def group_hotels_by_rooms(availability_allocation_report):
    # Prepare data for grouping by available rooms
    available_rooms = []
    revenues = []
    hotel_labels = []

    for hotel_id, report in availability_allocation_report.items():
        available_rooms.append(report['rooms_available'])
        revenues.append(report['revenue'])
        hotel_labels.append(hotel_id)

    # Create a DataFrame
    df = pd.DataFrame({
        'Hotel': hotel_labels,
        'Available Rooms': available_rooms,
        'Revenue': revenues
    })

    # Define the room categories
    bins = [0, 5, 10, float('inf')]  # Define the bins for low, medium, and high availability
    labels = ['Low Availability', 'Medium Availability', 'High Availability']
    df['Room Category'] = pd.cut(df['Available Rooms'], bins=bins, labels=labels)

    return df

# Create the box plot
def plot_revenue_by_room_category(df):
    # Check the grouped DataFrame structure
    print("\nData for Plotting:")
    print(df)

    #  Create a figure and axis explicitly
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the box plot grouped by room category
    sns.boxplot(x='Room Category', y='Revenue', data=df, palette="Set2", ax=ax)
    
    # Add titles and labels
    ax.set_title('Revenue Distribution by Room Availability', fontsize=16)
    ax.set_xlabel('Room Availability Category', fontsize=12)
    ax.set_ylabel('Revenue', fontsize=12)
    
    return fig