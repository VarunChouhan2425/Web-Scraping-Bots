from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

def google_scraper(company_names):
    chrome_path = r'C:\Users\VARUN CHOUHAN\OneDrive\Desktop\VARUN\data scrapers\attachments\chromedriver.exe'
    chrome_service = ChromeService(executable_path=chrome_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')  # Add this line if you want to run Chrome in headless mode
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get('https://www.google.com/webhp')

    address_list = []
    phone_number_list = []
    review_list = []

    for company_name in company_names:
        try:
            # Open a new browser window for each company search
            driver.execute_script("window.open('about:blank', '_blank');")
            # Switch to the newly opened window
            driver.switch_to.window(driver.window_handles[-1])

            # Navigate to Google
            driver.get('https://www.google.com/webhp')

            # Find the search input element in each iteration
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'gLFyf'))
            )
            search_input.clear()
            search_input.send_keys(company_name)
            search_input.submit()

            # Wait for search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[aria-label^="Call phone number"]'))
            )

            # Find the span element containing the phone number
            span_element = driver.find_element(By.CSS_SELECTOR, 'span[aria-label^="Call phone number"]')
            phone_number = span_element.text.strip()
        except:
            phone_number = "N/A"

        try:
            address_element = driver.find_element(By.CLASS_NAME, 'LrzXr')
            address = address_element.text.strip()
        except:
            address = "N/A"

        try:
            review_element = driver.find_element(By.CLASS_NAME, 'Aq14fc')
            review = review_element.text.strip()
        except:
            review = "N/A"

        address_list.append(address)
        phone_number_list.append(phone_number)
        review_list.append(review)

        time.sleep(6)  # Add a 6-second delay between each company search

    # Close the current window
    driver.quit()

    return address_list, phone_number_list, review_list

# address_list, phone_number_list, review_list = google_scraper(['panamax infotech ltd'])
# print(address_list)
# print(phone_number_list)
# print(review_list)

