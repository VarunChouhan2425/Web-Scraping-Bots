import pandas as pd
from google_scraper_main import google_scraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from random import randint
import time

def glassdoor_scraper(job_title, location):
    chrome_path = r'C:\Users\VARUN CHOUHAN\OneDrive\Desktop\VARUN\data scrapers\attachments\chromedriver.exe'
    chrome_service = ChromeService(executable_path=chrome_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get('https://www.glassdoor.co.in/Job/index.htm') # ?fromAge=1 -- 24hrs filter
    time.sleep(2)  # Waiting for the page to load

    # Find and fill the job title and location input fields
    job_title_input = driver.find_element('id', 'searchBar-jobTitle')
    job_title_input.send_keys(job_title)

    location_input = driver.find_element('id', 'searchBar-location')
    location_input.clear()  # Clear any pre-filled location
    location_input.send_keys(location)

    # Simulate hitting Enter
    location_input.send_keys(Keys.ENTER)

    time.sleep(3)  # Waiting for the search results to load

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    job_list = []

    jobs = soup.find_all('li', class_='JobsList_jobListItem__wjTHv')

    for job in jobs[:10]: # set job data limit
        job_title_element = job.find('a', class_='JobCard_jobTitle___7I6y')
        job_title = job_title_element.text.strip() if job_title_element else None
        
        company_name_element = job.find('span', class_='EmployerProfile_compactEmployerName__LE242')
        company_names = company_name_element.text.strip() if company_name_element else None
        
        location_element = job.find('div', class_='JobCard_location__rCz3x')
        location = location_element.text.strip() if location_element else None

        salary_element = job.find('div', class_='JobCard_salaryEstimate__arV5J')
        salary = salary_element.text.strip() if salary_element else None
        
        job_detail_element = job.find('a', class_='JobCard_jobTitle___7I6y')
        job_detail_url = job_detail_element["href"] if job_detail_element else None

        if job_detail_url:
            driver.get(job_detail_url)
            content = driver.page_source
            soup1 = BeautifulSoup(content, 'html.parser')

            job_descp_element = soup1.find('div', class_='JobDetails_jobDescription__uW_fK')
            job_description = job_descp_element.get_text(strip=True) if job_descp_element else None

            address_list, phone_number_list, review_list = google_scraper([company_names])

        
        job_info = {
            "Job Title": job_title,
            "salary": salary,
            "Company Name": company_names,
            "Location": location,
            "job_detail_url": job_detail_url,
            "job_description": job_description,
            "review": review_list,
            "address": address_list,
            "phone_number6": phone_number_list
        }
        
        job_list.append(job_info)
        delay = randint(4, 9)
        print(f"Waiting for {delay} seconds before the next job...")
        time.sleep(delay)

    driver.quit()

    df = pd.DataFrame(job_list)
    print(df)

    df.to_csv('data2.csv', index=False)

# glassdoor_scraper("Web Developer", "Pune")
