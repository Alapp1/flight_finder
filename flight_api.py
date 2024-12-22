#!/usr/bin/env python3
from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os
import isodate
from datetime import datetime

# Load Amadeus API credentials
load_dotenv()

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

# Initialize Amadeus client
amadeus = Client(client_id=AMADEUS_API_KEY, client_secret=AMADEUS_API_SECRET)

# Utility functions for formatting
def format_duration(iso_duration):
    """Convert ISO 8601 duration (e.g., PT12H10M) to human-readable format."""
    parsed_duration = isodate.parse_duration(iso_duration)
    total_seconds = int(parsed_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours} hours, {minutes} minutes"

def format_datetime(iso_datetime):
    """Convert ISO 8601 datetime (e.g., 2024-12-25T16:45:00) to a readable format."""
    parsed_datetime = datetime.fromisoformat(iso_datetime)
    return parsed_datetime.strftime("%A, %B %d, %Y at %I:%M %p")

def display_flights(flights):
    """Display flight data in a human-readable format."""
    for i, flight in enumerate(flights, start=1):
        price = flight["price"]["grandTotal"]
        currency = flight["price"]["currency"]
        itineraries = flight["itineraries"]

        print(f"Flight {i}: Price: {price} {currency}")
        for itinerary in itineraries:
            duration = format_duration(itinerary["duration"])
            print(f"  Total Duration: {duration}")
            for segment in itinerary["segments"]:
                departure = segment["departure"]
                arrival = segment["arrival"]
                print(
                    f"    {departure['iataCode']} ({format_datetime(departure['at'])}) -> "
                    f"{arrival['iataCode']} ({format_datetime(arrival['at'])}), "
                    f"Carrier: {segment['carrierCode']}, "
                    f"Segment Duration: {format_duration(segment['duration'])}"
                )
        print("-" * 150)

# Main flight search function
def find_cheapest_flights(origin, destination, rough_departure_date, rough_return_date, date_range):
    """
    Finds the cheapest flights within a given date range.
    """
    try:
        # Make the API call to search for flights
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=rough_departure_date,
            returnDate=rough_return_date,
            adults=1,
            currencyCode="USD",
            max=5  # Get the top 5 cheapest flights
        )

        # Parse and display results
        if response.data:
            print(f"Found {len(response.data)} flights:")
            display_flights(response.data)  # Use the new formatting function
            return response.data
        else:
            print("No flights found.")
            return None

    except ResponseError as error:
        print(f"An error occurred: {error}")
        return None

# Main program
def main():
    print("Welcome to the Flight Finder!")
    origin = input("Enter the departure city code (e.g., NYC): ").strip()
    destination = input("Enter the arrival city code (e.g., MAD): ").strip()
    rough_departure_date = input("Enter the approximate departure date (YYYY-MM-DD): ").strip()
    rough_return_date = input("Enter the approximate return date (YYYY-MM-DD): ").strip()
    date_range = int(input("Enter the range of days to search around the dates (e.g., 3): ").strip())

    print(f"Searching for the cheapest flights from {origin} to {destination}...")
    flights = find_cheapest_flights(origin, destination, rough_departure_date, rough_return_date, date_range)

    if flights:
        print("\nDone! Cheapest flights are displayed above.")
    else:
        print("No flights found within the specified date range.")

if __name__ == "__main__":
    main()

