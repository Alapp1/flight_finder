# Amadeus Flight Finder

This script uses the Amadeus Flight Offers Search API to fetch and display the cheapest flights programmatically. It provides a reliable and efficient way to find flight deals without relying on web scraping.

---

## Features

- **User Input**: Prompts for departure and arrival cities, along with a date range.
- **Cheapest Flights**: Retrieves the cheapest flights within the specified date range.
- **Human-Readable Output**: Displays prices, flight durations, departure/arrival times, and layover details in an easy-to-read format.
- **Flexible Dates**: Allows searching for flights within a range of days around the given dates.

---

## Requirements

1. **Amadeus API Key**:
   - Sign up at [Amadeus for Developers](https://developers.amadeus.com/).
   - Obtain an API key and secret for the Flight Offers Search API.

2. **Python 3.x**:
   - Ensure you have Python 3.6 or newer installed.

3. **Dependencies**:
   - Install the required Python libraries:
     ```bash
     pip install amadeus python-dotenv isodate
     ```

4. **Environment Variables**:
   - Create a `.env` file in the project directory and add your Amadeus API credentials:
     ```plaintext
     AMADEUS_API_KEY=your_api_key
     AMADEUS_API_SECRET=your_api_secret
     ```

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flight-finder.git
   cd flight-finder
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
3. Add Amadeus API credentials to the .env file
  ```bash
  AMADEUS_API_KEY=your_api_key
  AMADEUS_API_SECRET=your_api_secret
  ```

---

## Usage
1. Run the script:
   ```bash
   python amadeus_flight_finder.py
   ```
2. Follow the prompts:
  - **Enter the departure city code** (e.g., `JFK` for New York).  
  - **Enter the arrival city code** (e.g., `MAD` for Madrid).  
  - **Provide rough departure and return dates** (e.g., `2024-12-25` and `2025-01-10`).  
  - **Specify a range of days** around the given dates (e.g., `3` for ±3 days).

---

## Output

The script displays:

- **Price**: Total cost of the flight in USD.  
- **Flight Details**:  
  - Departure and arrival airport codes  
  - Human-readable departure and arrival times (e.g., "Wednesday, December 25, 2024 at 04:45 PM")  
  - Flight durations for each segment and the overall itinerary  
- **Carrier**: Airline operating the flight

---

### Example Output

```yaml
Flight 1: Price: 485.81 USD
  Total Duration: 12 hours, 10 minutes
    JFK (Wednesday, December 25, 2024 at 04:45 PM) -> FCO (Thursday, December 26, 2024 at 07:05 AM), Carrier: AZ, Segment Duration: 8 hours, 20 minutes
    FCO (Thursday, December 26, 2024 at 08:20 AM) -> MAD (Thursday, December 26, 2024 at 10:55 AM), Carrier: AZ, Segment Duration: 2 hours, 35 minutes
--------------------------------------------------
Flight 2: Price: 499.21 USD
  Total Duration: 14 hours, 30 minutes
    JFK (Wednesday, December 25, 2024 at 08:30 PM) -> MAD (Thursday, December 26, 2024 at 11:00 AM), Carrier: DL, Segment Duration: 14 hours, 30 minutes
--------------------------------------------------
```

---

## Limitations

- The script uses Amadeus' free tier, which has a limited number of API calls per month.  
- Only retrieves the top 5 cheapest flights.

---

## Notes

- The Amadeus API provides a reliable and scalable way to access flight data. If you encounter any issues, ensure your API key is active and your `.env` file is configured correctly.  
- Modify `max` in the API call to increase the number of results.





  
