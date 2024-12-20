# Hotels Allocation Project
The datasets used contain the following information:
* hotels.xlsx: number of vacant rooms and unit cost of each room for 400 hotels;
* guests.xlsx: discount fraction for 4000 potential customers;
* preferences.xlsx: order of hotel preference for each customer

The program must calculate the allocation of customers at hotels, considering the number of available rooms, the fact that each customer occupies exactly one room, and that each stay lasts only one night. The price paid by the customer is the unit price of the room discounted by the fraction of the discount to which the customer is entitled.

The program must implement four different allocation strategies:
* random: customers are randomly distributed to the rooms until the seats or customers are exhausted;
* customer preference: customers are served in order of reservation (the customer number indicates the order) and are allocated to the hotel based on their preference, until the seats or customers are exhausted;
* price: the places in the hotel are distributed in order of price, starting with the cheapest hotel and following in order of reservation and preference until the places or customers are exhausted;
* availability: places in hotels are distributed in order of room availability, starting with the most roomy hotel and subordinately in order of reservation and preference until places or clients are exhausted.

Finally, the program must present and display a report of the result obtained, showing for each strategy the number of customers accommodated, the number of rooms occupied, the number of different hotels occupied, the total volume of business (total earnings of each hotel), and the degree of customer satisfaction (calculated according to the location of the hotel assigned to them with respect to their preferences).
