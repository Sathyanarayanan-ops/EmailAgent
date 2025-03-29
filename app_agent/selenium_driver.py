from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests

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
# url = "https://careers.roblox.com/jobs/6637846/apply"
# driver = webdriver.Chrome()
# driver.get(url)
# driver.maximize_window()
# WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

# get_page_info("https://lifeattiktok.com/search/7480779960623008018?spread=5MWH5CQ")

API_BASE_URL = 'https://api.skyvern.com/v1/tasks'
API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ4ODgyNDUyNTIsInN1YiI6Im9fMzc2MjQ3OTQzOTkwMDk3NTMwIn0.THuYL7fWnXnMFc9IzRZ2LBmp_0bvTN0nUpQgGMo4EfY'

headers = {
    'x-api-key': f'{API_TOKEN}',
    'Content-Type': 'application/json'
}

task_payload = {
    "url":"https://careers.roblox.com/jobs/6637846/apply",
    "navigation_goal" : "Apply for a job",
    "data_extraction_goal" :"Was the job application successful?",
    "proxy_location" : "RESIDENTIAL",
    "navigation_payload" : personal_info
}

def create_task():
    response = requests.post(API_BASE_URL, json=task_payload, headers=headers)
    if response.status_code == 201:
        task_info = response.json()
        task_id = task_info.get('id')
        print(f"Task created with ID: {task_id}")
        return task_id
    else:
        print("Error creating task:", response.text)
        return None

def poll_task(task_id):
    task_url = f"{API_BASE_URL}/{task_id}"
    while True:
        status_response = requests.get(task_url, headers=headers)
        if status_response.status_code == 200:
            status_info = status_response.json()
            status = status_info.get('status')
            print("Task status:", status)
            if status == 'completed':
                print("Task completed successfully!")
                break
            elif status == 'failed':
                print("Task failed.")
                break
            else:
                time.sleep(2)
        else:
            print("Error checking task status:", status_response.text)
            break

if __name__ == "__main__":
    task_id = create_task()
    if task_id:
        poll_task(task_id)