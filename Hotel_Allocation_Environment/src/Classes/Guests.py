class guests:
    def __init__(self, guest_id, discount):
        self.guest_id = guest_id
        self.discount = discount

    def get_discounted_price(self, price):
        return price * (1 - self.discount)


from src.Data_loading import load_data
hotels_df, guests_df, preferences_df = load_data()

guests_dict = {}

for i, row in guests_df.iterrows():
    guest_id = row['guest']
    discount = row['discount']
    # Store the preferences in the 'guests' dictionary

# Print guest_dict to check its contents
for guest_id, guest_obj in guests_dict.items():
    print(f"Guest ID: {guest_id}")
    print(f"Discount: {guest_obj.discount}")
    print()  # Print a newline for readability
