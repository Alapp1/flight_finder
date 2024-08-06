#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
import windscribe
from twocaptcha import TwoCaptcha

def get_labels(file_path):
    with open(file_path, 'r') as file:
        labels = [line.strip() for line in file]
    return labels

def connect_to_server(label):
    try:
        windscribe.connect(label)
        print(windscribe.status())
    except Exception as e:
        print("Error connecting to VPN")
        print(windscribe.status())

def solve_captcha(driver, api_key):
    solver = TwoCaptcha(api_key)
    
    try:
        site_key = driver.find_element(By.CSS_SELECTOR, 'div.g-recaptcha').get_attribute('data-sitekey')
        url = driver.current_url
        
        result = solver.recaptcha(sitekey=site_key, url=url)
        
        code = result['code']
        
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{code}';")
        driver.execute_script("document.getElementById('captcha-form').submit();")
        print("CAPTCHA solved")
        
        return True
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")
        return False

def check_for_captcha(driver):
    try:
        

        # Define potential CAPTCHA indicators
        captcha_indicators = [
        "iframe[src*='recaptcha']",
        "div.g-recaptcha",
        "div.rc-anchor",
        "div#captcha",
        "input#captcha",
        "span#captcha"
        ]

        captcha_found = False

        # Check for CAPTCHA elements
        for selector in captcha_indicators:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"CAPTCHA detected using selector: {selector}")
                captcha_found = True
                break
            except TimeoutException:
                continue

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error checking for CAPTCHA: {e}")

    return captcha_found

def manually_check_captcha():
    print("Please solve the CAPTCHA if present, then press Enter to continue...")
    input()

def main():
    labels = get_labels('labels.txt')

    # Get user input
    departure_city = input("Enter the departure city code (e.g., JFK): ")
    arrival_city = input("Enter the arrival city code (e.g., LAX): ")
    departure_date = input("Enter the departure date (e.g., Aug 5, 2024): ")
    return_date = input("Enter the return date (e.g., Aug 15, 2024): ")

    departure_flight_inputs = {
            
        'Departure': departure_city,
        'Arrival': arrival_city,
        'DepartureDate': departure_date,
        'ReturnDate': return_date
    }
    
    api_key = 'a8516eb96621f7008c4abc827b0e00f8'  # Replace with your actual 2Captcha API key
    
    for label in labels:
        connect_to_server(label)
        cheapest_flight = find_cheapest_flights(departure_flight_inputs, api_key)
        print("Cheapest Flight: ", cheapest_flight)

def find_cheapest_flights(flight_info, api_key):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome('/home/mule/Downloads/chromedriver-linux64', chrome_options=options)

    leaving_from = flight_info['Departure']
    going_to = flight_info['Arrival']
    departure_date = flight_info['DepartureDate']
    return_date = flight_info['ReturnDate']
    
    # Go to Expedia
    driver.get("https://www.expedia.com/Flights")
    time.sleep(2)
    
    manually_check_captcha()

    #if check_for_captcha(driver):
        #time.sleep(3)
        #solve_captcha(driver, api_key)
    
    # Complete Leaving From Portion
    try:
        leaving_from_button_selector = 'button[aria-label="Leaving from"]'
        leaving_from_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, leaving_from_button_selector))
        )
        leaving_from_button.click()
        print("Clicked 'Leaving from' button")

        leaving_from_input_selector = 'input[data-stid="origin_select-menu-input"]'
        leaving_from_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, leaving_from_input_selector))
        )
        leaving_from_input.send_keys(leaving_from)
        time.sleep(1)
        leaving_from_input.send_keys(Keys.ENTER)
        print("Entered departure city")
        
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error interacting with 'Leaving from' field: {e}")
        driver.quit()
        return "Error interacting with 'Leaving from' field"
    
    # Complete Going To Portion
    try:
        going_to_button_selector = 'button[aria-label="Going to"]'
        going_to_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, going_to_button_selector))
        )
        going_to_button.click()
        print("Clicked 'Going to' button")

        going_to_input_selector = 'input[data-stid="destination_select-menu-input"]'
        going_to_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, going_to_input_selector))
        )
        going_to_input.send_keys(going_to)
        time.sleep(1)
        going_to_input.send_keys(Keys.ENTER)
        print("Entered arrival city")
        
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error interacting with 'Going to' field: {e}")
        driver.quit()
        return "Error interacting with 'Going to' field"
    
    time.sleep(2)
    
    # Complete Departure Date Portion
    try:
        date_selector_button = 'button[aria-label*="Dates"]'
        date_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, date_selector_button))
        )
        date_button.click()
        print("Clicked Date Selector button")

        # Select Departure Date
        departure_date_selector = f'button[aria-label="{departure_date}"]'
        while True:
            try:
                departure_date_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, departure_date_selector))
                )
                departure_date_element.click()
                break
            except TimeoutException:
                next_month_selector = 'button[data-stid="date-picker-paging"][2]'
                driver.find_element(By.CSS_SELECTOR, next_month_selector).click()
                time.sleep(1)
        time.sleep(1)
        
        # Select Return Date
        return_date_selector = f'button[aria-label="{return_date}"]'
        while True:
            try:
                return_date_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, return_date_selector))
                )
                return_date_element.click()
                break
            except TimeoutException:
                next_month_selector = 'button[data-stid="date-picker-paging"][2]'
                driver.find_element(By.CSS_SELECTOR, next_month_selector).click()
                time.sleep(1)

        apply_date_selector = 'button[data-stid="apply-date-picker"]'
        driver.find_element(By.CSS_SELECTOR, apply_date_selector).click()
        print("Applied dates")
        
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error interacting with Date Selector: {e}")
        driver.quit()
        return "Error interacting with Date Selector"
    
    # Click Search
    try:
        search_button_selector = 'button#search_button'
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_button_selector))
        )
        search_button.click()
        print("Clicked Search Button")
        time.sleep(5) 
        manually_check_captcha()
        # Wait for CAPTCHA and solve it using 2Captcha
        #captcha_solved = solve_captcha(driver, api_key)
        #if not captcha_solved:
            #driver.quit()
            #return "Error solving CAPTCHA"
        
        # Wait for page to load
        time.sleep(15)
        
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error clicking Search Button: {e}")
        driver.quit()
        return "Error clicking Search Button"

    # Select "Price (lowest to highest)" from the sort dropdown
    try:
        sort_dropdown_selector = 'select#sort-filter-dropdown-SORT'
        sort_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, sort_dropdown_selector))
        )
        sort_dropdown.click()
        print("Clicked sort dropdown menu")

        price_highest_to_lowest_selector = 'option[value="PRICE_INCREASING"]'
        price_highest_to_lowest_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, price_highest_to_lowest_selector))
        )
        price_highest_to_lowest_option.click()
        print("Selected 'Price (lowest to highest)' option")
        
        time.sleep(5)  # Let the page update with the new sorting
        
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error interacting with sort dropdown: {e}")
        driver.quit()
        return "Error interacting with sort dropdown"

    # Click Non-Stop    
    try:
        # Select and click the 'Nonstop' checkbox
        nonstop_checkbox_selector = "input#NUM_OF_STOPS"
        nonstop_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, nonstop_checkbox_selector))
        )
        nonstop_checkbox.click()
        print("Clicked 'Nonstop' checkbox")

    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error finding or clicking the 'Nonstop' checkbox: {e}") 

if __name__ == "__main__":
    main()

