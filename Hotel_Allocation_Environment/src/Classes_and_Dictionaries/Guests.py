from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

preferences_df = preferences_df.sort_values(by=['guest', 'priority']) # I want to insert the information in the priorities dataset into the guest dictionary

def create_guest(guest_id, discount, preferences):  # Function to create the object guest
    return {'discount': discount, 'preferences': preferences}


guests_dict = {} # initialize an empty dictionary

for i, row in guests_df.iterrows():  # iterate over each row in the dataframe
    guest_id = row['guest']
    discount = row['discount']    
    
    # Filter the DataFrame for the current guest and get hotels in priority order
    guest_preferences = preferences_df[preferences_df['guest'] == guest_id]
    hotels_priority = guest_preferences['hotel'].tolist()  # List of hotels in priority order
   
    guests_dict[guest_id] = create_guest(guest_id, discount, hotels_priority)


print(guests_dict)



