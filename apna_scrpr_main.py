from bs4 import BeautifulSoup
import pandas as pd
from google_scraper_main import google_scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def apna_scraper(job_title, location):
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=options)

    api_url = f'https://apna.co/'
    print(api_url)

    # Mimic human-like behavior by adding random delays
    def random_delay():
        time.sleep(random.uniform(2, 4))  

    # Visit the URL
    driver.get(api_url)
    random_delay()

    # Find and fill the job title input field
    job_title_input = None
    for locator in [
        (By.CSS_SELECTOR, "input[placeholder='Search jobs by \\'skill\\'']"),
        (By.CSS_SELECTOR, "input[placeholder='Search jobs by \\'title\\'']"),
        (By.CSS_SELECTOR, "input[placeholder='Search jobs by \\'company\\'']")
    ]:
        try:
            job_title_input = driver.find_element(*locator)
            break
        except NoSuchElementException:
            pass
            
    if job_title_input is None:
        print("Unable to find the job title input field.")
        driver.quit()
        return

    job_title_input.send_keys(job_title)

    # Find and fill the location input field
    location_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search for an area or city']")
    location_input.click()  # Click to focus on the input field
    driver.execute_script("arguments[0].value = ''", location_input)  # Clear any pre-filled location
    location_input.send_keys(location,' ','Region')
    time.sleep(2)
    action = ActionChains(driver)
    action.send_keys(Keys.ARROW_DOWN).perform()
    action.send_keys(Keys.ENTER).perform()

    # Wait for the button to become clickable
    search_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "styles__ApplyButton-sc-163gdpk-16"))
    )

    # Click the button
    search_button.click()

    random_delay()

    # Extract HTML content after JavaScript execution
    html_content = driver.page_source

    # Now you can use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all job listings based on their HTML structure
    jobs = soup.find_all('div', class_='JobCardList__Grid-sc-1v9ot9b-1 gTeTVH')

    # Initialize lists to store data
    job_titles = []
    company_names = []
    locations = []
    salarys = []
    job_detail_urls = []
    job_descriptions = []

    # Extract job titles, company names, and locations
    for job in jobs[:10]: 
        job_title_elements = job.find_all('a', class_='JobListCardstyles__JobTitle-ffng7u-7 cuaBGE')
        for job_title_element in job_title_elements:
            job_titles.append(job_title_element.text.strip())
        
        company_name_elements = job.find_all('div', class_='JobListCardstyles__JobCompany-ffng7u-8 gguURM')
        for company_name_element in company_name_elements:
            company_names.append(company_name_element.text.strip())
        
        salary_elements = job.find_all('p', class_='m-0 truncate text-sm leading-[20px] text-[#8C8594]')
        for salary_element in salary_elements:
            salarys.append(salary_element.text.strip())
        
        location_elements = job.find_all('p', class_='m-0 text-sm leading-[20px] text-[#8C8594]')
        for location_element in location_elements:
            locations.append(location_element.text.strip())

        job_detail_elements = job.find_all('a', class_='JobListCardstyles__JobTitle-ffng7u-7 cuaBGE')
        for job_detail_element in job_detail_elements:
            relative_url = job_detail_element['href']
            full_url = f"https://apna.co{relative_url}?search=true"
            job_detail_urls.append(full_url)

    # Extract job descriptions
    for url in job_detail_urls:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        random_delay()
        html_content = driver.page_source
        driver.quit()
        soup1 = BeautifulSoup(html_content, 'html.parser')
        job_desc_element = soup1.find('div', class_='md:mt-[24px]')
        if job_desc_element:
            job_descriptions.append(job_desc_element.text.strip())
        else:
            job_descriptions.append("Job description not found.")
        
        random_delay()

    
    address_list, phone_number_list, review_list = google_scraper(company_names)

    df = pd.DataFrame({'Job Title': job_titles, 
                       'Company Name': company_names, 
                       'Location': locations, 
                       'Salary': salarys, 
                       'job_detail_url': job_detail_urls, 
                       'job_description': job_descriptions,
                        'address': address_list,
                        'phone number': phone_number_list,
                        'review': review_list
                       })
    print(df)
    df.to_csv('data1.csv', index=False)  # Set index=False to avoid saving the DataFrame index

# Example usage:
# apna_scraper("Web Developer", "Pune")
