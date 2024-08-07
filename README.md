# Project Overview

This project is a Python script that utilizes Windscribe VPN and the Selenium framework to scrape Expedia for the cheapest flights throughout all of Windscribe's locations.

## User Interaction

The script prompts the user to enter:

- Departure airport code
- Arrival airport code
- Departure date
- Return date

## Project Considerations

To extract the server ID list from the Windscribe locations list, the following command was used:

```bash
windscribe locations | awk '{print $4}' | sed 1d >> labels.txt
```
## Current Status

- **Implementation Required:**
  - Click the nonstop checkbox.
  - Retrieve the final price of the cheapest flight.
  - Output list of flight costs, specifying the minimum

- **Manual Steps:**
  - Captchas must still be completed manually.



