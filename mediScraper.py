import pandas as pd
import sys
import csv
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from google_scraper_main import google_scraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def medi_scraper():
    chrome_path = r'chromedriver.exe'
    chrome_service = ChromeService(executable_path=chrome_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    link = 'https://www.medica-tradefair.com/vis/v1/en/search?_query=&view_type=rows&f_type=profile&f_event=medcom2024.MEDICA&f_country=AU&f_country=CA&f_country=DE&f_country=IN&f_country=IL&f_country=NL&f_country=US&f_country=GB&f_country=SE&f_country=CH&f_country=SG'
    print(link)
    driver.get(link)

    company_data_list = []
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    while True:
        companies = driver.find_elements(By.CLASS_NAME, "teaser-row__legend-primary")

        for company_block in companies:
            try:
                name_elem = company_block.find_element(By.CLASS_NAME, "teaser-row__title")
                company_name = name_elem.text if name_elem else "N/A"
                print(company_name)

                parent_row = company_block.find_element(By.XPATH, "./ancestor::div[contains(@class, 'teaser-row')]")
                actions.move_to_element(parent_row).perform()
                time.sleep(1)

                try:
                    button = parent_row.find_element(By.CLASS_NAME, "teaser-row__details")
                    button.click()
                except Exception as e:
                    print(f"Failed to click details for {company_name}: {e}")
                    continue

                try:
                    contact_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".exh-contact")))
                except:
                    print(f"Skipping {company_name} due to no contact info.")
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, "button.icon-button[title='Close']")
                        close_button.click()
                        time.sleep(1)
                    except:
                        pass
                    continue

                try:
                    email_div = contact_div.find_element(By.CLASS_NAME, "exh-contact__email")
                    email = email_div.text.replace("E-mail:", "").strip()
                except:
                    email = "N/A"

                try:
                    phone_div = contact_div.find_element(By.CLASS_NAME, "exh-contact__phone")
                    phone = phone_div.text.replace("Phone:", "").strip()
                except:
                    phone = "N/A"

                try:
                    website_link = contact_div.find_element(By.CSS_SELECTOR, ".exh-contact__links a")
                    website = website_link.get_attribute("href")
                except:
                    website = "N/A"

                print(f"Email: {email}")
                print(f"Phone: {phone}")
                print(f"Website: {website}")

                company_data_list.append({
                    "Company Name": company_name,
                    "Email": email,
                    "Phone": phone,
                    "Website": website
                })

                try:
                    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.icon-button[title='Close']")))
                    close_button.click()
                except Exception as e:
                    print(f"Could not close details popup for {company_name}: {e}")

                time.sleep(1)

            except Exception as e:
                print(f"Error processing a company: {e}")
                continue

        try:
            next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to next page']")))
            is_disabled = next_button.get_attribute("disabled") is not None or \
                          "fcl-ui-state--disabled" in next_button.get_attribute("class")

            if is_disabled:
                print("Reached last page, no more pages to navigate.")
                break

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            next_button.click()
            print("Navigated to next page.")

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "teaser-row__legend-primary")))
            time.sleep(2)

        except Exception as e:
            print(f"Could not find or click next page button: {e}")
            break

    keys = ["Company Name", "Email", "Phone", "Website"]
    with open("companies_data.csv", "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(company_data_list)

    print("Data saved to companies_data.csv")

medi_scraper()
