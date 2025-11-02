from multiprocessing import Process
from apna_scrpr_main import apna_scraper
from glassdoor_scrpr_main import glassdoor_scraper
from indeed_scrapr_main import indeed_scraper

def trigger():
    job_title = input("Enter job title: ")
    location = input("Enter location: ")

    # Define processes for each scraper
    apna_process = Process(target=apna_scraper, args=(job_title, location))
    glassdoor_process = Process(target=glassdoor_scraper, args=(job_title, location))
    indeed_process = Process(target=indeed_scraper, args=(job_title, location))

    # Start all processes
    apna_process.start()
    glassdoor_process.start()
    indeed_process.start()

    # Wait for all processes to finish
    apna_process.join()
    glassdoor_process.join()
    indeed_process.join()

if __name__ == "__main__":
    trigger()
