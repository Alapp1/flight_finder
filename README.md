# Flight Finder Project

This repository contains two approaches for finding the cheapest flights:

1. **Selenium Scraper**:
   - Uses Windscribe VPN and Selenium to scrape Expedia for flight prices.
   - Best suited for scenarios where an API is not available or not feasible.

2. **Amadeus API Implementation**:
   - Leverages the Amadeus Flight Offers Search API to programmatically fetch flight prices.
   - Recommended for reliability, speed, and API compliance.

## Project Structure

- **README.md**: This file, providing an overview of the project and approaches.
- **README_selenium.md**: Details the Selenium-based scraping implementation.
- **README_amadeus.md**: Details the Amadeus API-based implementation.

## Comparison of Approaches

| Feature                          | Selenium Scraper               | Amadeus API             |
|----------------------------------|--------------------------------|-------------------------|
| **Ease of Setup**                | Moderate                       | Simple                  |
| **Reliability**                  | Low (CAPTCHA issues)           | High                    |
| **Scalability**                  | Limited                        | High                    |
| **Performance**                  | Slower (requires browser)      | Faster (API-based)      |
| **Data Accuracy**                | Depends on scraping success    | High                    |

## Next Steps

- To use the Selenium Scraper, refer to [README_selenium.md](README_selenium.md).
- To use the Amadeus API implementation, refer to [README_amadeus.md](README_amadeus.md).
