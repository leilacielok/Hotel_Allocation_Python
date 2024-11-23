import matplotlib.pyplot as plt
import seaborn as sns

# Random function visualization: Create a new figure for each plot to avoid reusing the same figure
def plot_occupancy_distribution(allocation):
    fig, ax = plt.subplots()
    hotel_ids = list(allocation.keys())
    num_guests = [allocation[hotel_id]['number_of_guests_accommodated'] for hotel_id in hotel_ids]
    
    ax.bar(hotel_ids, num_guests)
    ax.set_xlabel('Hotel')
    ax.set_ylabel('Number of Guests')
    ax.set_title('Occupancy Distribution')
    # Remove x-tick labels (make them empty)
    ax.set_xticklabels([])  # Empty list removes the label
    return fig

def plot_revenue_distribution(allocation):
    hotel_names = list(allocation.keys())
    revenues = [allocation[hotel_name]['revenue'] for hotel_name in hotel_names]
    
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

def plot_guests_per_hotel(allocation):
    hotel_names = list(allocation.keys())
    num_guests = [allocation[hotel_name]['number_of_guests_accommodated'] for hotel_name in hotel_names]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=hotel_names, y=num_guests, color='purple', ax=ax)
    ax.set_title('Number of Guests per Hotel')
    ax.set_xlabel('Hotels')
    ax.set_ylabel('Number of Guests')
    return fig
