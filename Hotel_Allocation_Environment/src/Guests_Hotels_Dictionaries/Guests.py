from src.Data_loading import load_data

# Load data
hotels_df, guests_df, preferences_df = load_data()

# Sort preferences DataFrame by guest and priority for easier handling 
preferences_df = preferences_df.sort_values(by=['guest', 'priority'])

# Create a guest object
def create_guest(guest_id, discount, preferences): 
    """
    Creates a guest dictionary with discount and preferences.

    Parameters:
    guest_id (str): Unique ID of the guest.
    discount (float): Discount applicable to the guest.
    preferences (list): List of hotel preferences in priority order.

    Returns:
    dict: A dictionary representing the guest's data.
    """
    return {'discount': discount, 'preferences': preferences}

def create_guests_dict(guests_df, preferences_df):
    """
    Creates a dictionary of guests, with each guest having a discount and hotel preferences.

    Parameters:
    guests_df (DataFrame): DataFrame containing guest information.
    preferences_df (DataFrame): DataFrame containing guest preferences for hotels.

    Returns:
    dict: A dictionary where each guest ID maps to a guest data dictionary with 'discount' and 'preferences'.
    """

    # Initialize an empty dictionary for guests' data
    guests_dict = {} 

    # Group preferences by guest 
    grouped_preferences = preferences_df.groupby('guest')['hotel'].apply(list)

    # Iterate over each row in the guests dataframe and build the guest dictionary 
    for _, row in guests_df.iterrows():  
        guest_id = row['guest']
        discount = row['discount']    
    
        # Filter the DataFrame for the current guest and get hotels in priority order
        hotels_priority = grouped_preferences.get(guest_id, [])  # Get the list of hotels in priority order
    
        # Add guest info to the dictionary
        guests_dict[guest_id] = create_guest(guest_id, discount, hotels_priority)

    return guests_dict

guests_dict_original = create_guests_dict(guests_df, preferences_df)