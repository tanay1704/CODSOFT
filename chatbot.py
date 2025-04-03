import random
import re
from datetime import datetime

class HotelBookingBot:
    """A rule-based chatbot that helps users book a hotel room based on predefined intents."""

    # Predefined responses for negative answers and exit commands
    negative_responses = ("no", "nope", "nah", "naw", "not interested", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

    # Predefined random questions for greeting the user
    random_greetings = (
        "Welcome to our hotel! How can I assist you with your booking today?",
        "Hello! Looking for a room? I can help you book one!",
        "Hi there! Want to make a reservation? I can help you with that!"
    )

    # Predefined room types
    available_rooms = {
        "Single": 3500,  # 3500 INR per night
        "Double": 5500,  # 5500 INR per night
        "Suite": 10000   # 10000 INR per night
    }

    def __init__(self):
        """Initialize the bot and define regex patterns to match user inputs."""
        self.booking_details = {}
    
    def greet(self):
        """Start the conversation with a random greeting."""
        print(random.choice(self.random_greetings))
        self.name = input("Can I have your name, please?\n")
        
        # Ask if the user wants to proceed with the booking
        willing_to_book = input(f"Hi {self.name}, would you like to proceed with booking a room?\n")
        
        if self.make_exit(willing_to_book):  # Check if user wants to exit
            return
        
        if willing_to_book.lower() in self.negative_responses:
            print("No problem! Have a great day!")
            return
        
        # Start gathering booking details
        self.ask_room_type()

    def make_exit(self, reply):
        """Check if the user wants to exit the conversation."""
        if reply.lower() in self.exit_commands:
            print("Goodbye! Have a great day!")
            return True
        return False

    def ask_room_type(self):
        """Ask the user for their preferred room type."""
        while True:
            print("Great! What type of room would you prefer?")
            print("Available options: Single, Double, Suite")
            room_type = input("Please enter the room type:\n")
            
            # Validate room type
            if room_type.capitalize() in self.available_rooms:
                self.booking_details['room_type'] = room_type.capitalize()
                self.ask_check_in_date()
                break
            else:
                print("Sorry, that room type is not available. Please choose from the available options.")

    def ask_check_in_date(self):
        """Ask the user for their check-in date."""
        while True:
            check_in_date = input("When would you like to check in? (Please provide in format YYYY-MM-DD)\n")
            
            if not self.is_valid_date(check_in_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            
            self.booking_details['check_in'] = check_in_date
            self.ask_check_out_date()
            break

    def ask_check_out_date(self):
        """Ask the user for their check-out date."""
        while True:
            check_out_date = input("When would you like to check out? (Please provide in format YYYY-MM-DD)\n")
            
            if not self.is_valid_date(check_out_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            
            # Check if check-out is after check-in
            check_in_date = self.booking_details['check_in']
            if datetime.strptime(check_out_date, "%Y-%m-%d") <= datetime.strptime(check_in_date, "%Y-%m-%d"):
                print("Error: Check-out date must be after check-in date.")
                continue
            
            self.booking_details['check_out'] = check_out_date
            self.ask_number_of_guests()
            break

    def ask_number_of_guests(self):
        """Ask the user for the number of guests."""
        while True:
            try:
                num_guests = int(input("How many guests will be staying?\n"))
                if num_guests <= 0:
                    print("Please enter a valid number of guests.")
                    continue
                self.booking_details['num_guests'] = num_guests
                self.show_room_price()
                break
            except ValueError:
                print("Please enter a valid number of guests.")

    def show_room_price(self):
        """Calculate and show the price of the booking based on room type and number of nights."""
        room_type = self.booking_details['room_type']
        check_in = self.booking_details['check_in']
        check_out = self.booking_details['check_out']
        
        # Simple calculation: number of nights = difference between check-in and check-out dates
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        num_nights = (check_out_date - check_in_date).days
        
        if num_nights <= 0:
            print("Error: Check-out date must be after check-in date.")
            self.ask_check_out_date()
            return
        
        room_price_per_night = self.available_rooms[room_type]
        total_price = room_price_per_night * num_nights
        
        print(f"Your total cost for {num_nights} night(s) in a {room_type} room will be ₹{total_price}.")
        self.confirm_booking(total_price)

    def confirm_booking(self, total_price):
        """Ask the user to confirm the booking."""
        confirm = input(f"Do you want to confirm the booking for ₹{total_price}? (yes/no)\n")
        
        if confirm.lower() == "yes":
            print("Your booking has been confirmed! Thank you for choosing us.")
        else:
            print("Booking canceled. If you need help with anything else, feel free to ask.")

    def is_valid_date(self, date_string):
        """Check if the date is in the correct format."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def no_match_intent(self):
        """Return a response when the bot cannot match the user's input to any intent."""
        responses = [
            "I didn't quite understand that. Can you please clarify?",
            "Could you rephrase that for me? I'm not sure what you mean.",
            "Sorry, I didn't get that. Could you try again?"
        ]
        return random.choice(responses)

# Start the chatbot
if __name__ == "__main__":
    bot = HotelBookingBot()
    bot.greet()
