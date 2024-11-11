class guests:
    def __init__(self, guest_id, discount, preferences):
        self.guest_id = guest_id
        self.discount = discount
        self.preference_order = preferences

    def get_discounted_price(self, price):
        return price * (1 - self.discount)


from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

guests_dict = {}

for i, row in guests_df.iterrows():
    guest_id = row['guest']
    discount = row['discount']
    preference_order = preferences_df[preferences_df['guest'] == guest_id]  #filtering the preferences dataframe for the guest
    
    preferences = {}
    for idx, pref_row in preference_order.iterrows():
        priority = pref_row['priority']
        hotel = pref_row['hotel']
        preferences[priority] = hotel
        
    guests_dict[guest_id] = guests(guest_id, discount, preferences)  # Store the preferences in the 'guests' dictionary

# Check
for guest_id, guest_obj in guests_dict.items():
    print(f"Guest ID: {guest_id}")
    print(f"Discount: {guest_obj.discount}")
    print(f"Preferences: {guest_obj.preference_order}")
    print()
