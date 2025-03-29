from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Personal information
personal_info = {
    "first_name": "Sathyanarayanan",
    "last_name": "Rengasamy Suresh",
    "age": "23",
    "email": "sathyanarayanan0705@gmail.com",
    "phone": "+1-540-245-3047",
    "country": "United States",
    "address": "23281 Mora Heights Way",
    "zip": "94024",
    "city": "Los Altos Hills",
    "state": "California",
    "sponsorship": "yes",
    "citizenship": "India",
    "current_visa": "F1",
    "gender": "Male",
    "sexuality": "Heterosexual/Straight",
    "veteran_status": "no",
    "disability": "no",
    "experience_level": "1-2 years",
    "authorized_to_work": "yes",
    "visa_needed": "h1b",
    "school": "Virginia Tech",
    "degree": "Masters",
    "major": "Computer Engineering",
    "experience": """
Software Development Engineer – Ai Planet (May 2024 – Oct 2024), Blacksburg, VA
• Architected RAG pipeline for finetuned-LLM with PEFT & LORA; reduced response time from 35s to 15s.
• Designed and deployed Nginx-based API Proxy handling 6,000+ requests/model.
• Deployed LLM on AWS EKS with CI/CD using Kubernetes, Docker, Jenkins.

Programmer Analyst – Genpact / bEarly Technovations (May 2022 – Aug 2023), Chennai
• Improved query performance by 40% using Casper & Vega; reduced codebase by 10%.
• Built survey data pipeline with unit tests, reducing processing time by 30%.
• Optimized AWS cloud for scalable client solutions.

Undergrad Research Assistant – SASTRA University (Jan 2022 – May 2022)
• Led 5-member team on waste mgmt system with Raspberry Pi + CV model.
• Achieved 95% detection accuracy, results presented at IEEE conf.
"""
}


def apply_to_job(url):
    """Visit a job posting URL and attempt to click the Apply button."""
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        print(f"Visiting {url}")
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Apply Now') or contains(text(), 'Submit Application') or @aria-label='Apply']"))
        )
        apply_button.click()
        print("Clicked on Apply button.")
        time.sleep(5)  # Optional: give time to load next step
        # Further form filling logic will be added here based on the site

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

    finally:
        driver.quit()
        

    


# Example usage
job_urls = [
    "https://careers.roblox.com/jobs/6637846?gh_jid=6637846&gh_src=da92d0c91",
    # Add more URLs here later
]

for url in job_urls:
    apply_to_job(url)
