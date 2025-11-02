import streamlit as st
import time
from multiprocessing import Process
from apna_scrpr_main import apna_scraper
from glassdoor_scrpr_main import glassdoor_scraper
from indeed_scrapr_main import indeed_scraper
from google_scraper_main import google_scraper

def apna_scraper_with_name(job_title, location):
    apna_scraper(job_title, location)
    st.write("Apna scraping completed!")

def glassdoor_scraper_with_name(job_title, location):
    glassdoor_scraper(job_title, location)
    st.write("Glassdoor scraping completed!")

def indeed_scraper_with_name(job_title, location):
    indeed_scraper(job_title, location) 
    st.write("Indeed scraping completed!")

def trigger():
    st.title("Job Scraper")

    job_title = st.text_input("Enter job title:")
    location = st.text_input("Enter location:")

    if st.button("Scrape Jobs"):
        st.write(f"Title: '{job_title}'")
        st.write(f"Location: '{location}'")
        time.sleep(2)
        st.write("Triggering bots...")
        time.sleep(3)
        st.write("Scraping...")
        
        # Define processes for each scraper with name
        apna_process = Process(target=apna_scraper_with_name, args=(job_title, location))
        glassdoor_process = Process(target=glassdoor_scraper_with_name, args=(job_title, location))
        indeed_process = Process(target=indeed_scraper_with_name, args=(job_title, location))

        # Start all processes
        apna_process.start()
        glassdoor_process.start()
        indeed_process.start()

        # Wait for all processes to finish
        apna_process.join()
        st.write("Apna scraping completed!")
        
        glassdoor_process.join()
        st.write("Glassdoor scraping completed!")
        
        indeed_process.join()
        st.write("Indeed scraping completed!")

        st.write("Job scraping completed!")

if __name__ == "__main__":
    trigger()
