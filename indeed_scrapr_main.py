import pandas as pd
from google_scraper_main import google_scraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from random import randint
import time

def indeed_scraper(job_title, location):
    chrome_path = r'C:\Users\VARUN CHOUHAN\OneDrive\Desktop\VARUN\data scrapers\attachments\chromedriver.exe'
    chrome_service = ChromeService(executable_path=chrome_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')  # Add this line if you want to run Chrome in headless mode
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    link = f'https://in.indeed.com/jobs?q={job_title}&l={location}&radius=100' #&fromage=1 -- 24hrs filter
    print(link)
    driver.get(link)
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    job_list = []

    jobs = soup.find_all("div", class_="job_seen_beacon")
    for job in jobs[:5]: # set job data limit
        company_name_elem = job.find("span", class_="css-92r8pb eu4oa1w0")
        company_names = company_name_elem.text.strip() if company_name_elem else None

        company_location_elem = job.find("div", class_="css-1p0sjhy eu4oa1w0")
        company_location = company_location_elem.text.strip() if company_location_elem else None

        salary_elem = job.find("div", class_="metadata salary-snippet-container css-5zy3wz eu4oa1w0")
        salary_text = salary_elem.find("div", class_="css-1cvo3fd eu4oa1w0").text.strip() if salary_elem else None

        job_title_elem = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
        job_title = job_title_elem.text.strip() if job_title_elem else None

        link_tag = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
        link_half = link_tag["href"]
        base_url = "https://in.indeed.com"
        job_detail_url = f"{base_url}{link_half}"

        driver.get(job_detail_url)
        content = driver.page_source
        soup1 = BeautifulSoup(content, 'html.parser')
        
        job_desc_elements = soup1.find_all('div', class_='jobsearch-jobDescriptionText')
        job_desc = ' '.join([desc.text.strip() for desc in job_desc_elements]) if job_desc_elements else None

        phone_no_elements = soup1.find_all('span', class_='jobsearch-JobDescription-phone-number')
        phone_no = None  # Default value if no phone number is found
        if phone_no_elements:
            phone_no_texts = [element.text.strip() for element in phone_no_elements]
            # Combine multiple phone numbers into a single string if necessary
            phone_no = ', '.join(phone_no_texts)
        
        
        address_list, phone_number_list, review_list = google_scraper([company_names])



        job_info = {
            "Job Title": job_title,
            "Salary": salary_text,
            "Company Name": company_names,
            "Location": company_location,
            "job_detail_url": job_detail_url,
            "job_description": job_desc,
            "phone_number": phone_no,
            "review": review_list,
            "address": address_list,
            "phone_number6": phone_number_list
        }
        job_list.append(job_info)
        delay = randint(4, 9)
        print(f"Waiting for {delay} seconds before the next job...")
        time.sleep(delay)

        df = pd.DataFrame(job_list)
        print(df)
        df.to_csv('data3.csv', index=False)
    
    # driver.quit()

# indeed_scraper("python Developer", "Pune")
