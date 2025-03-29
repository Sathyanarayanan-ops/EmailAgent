from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

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







