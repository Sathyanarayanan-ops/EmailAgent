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


import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# -----------------------------------------------------------------------------
# Function: detect_application_entry
# -----------------------------------------------------------------------------
def detect_application_entry(driver):
    """
    Analyze the page to detect the job application entry method.
    Returns a dictionary with an "entry_type" key and relevant details.
    """
    try:
        # Case 1: Apply button present
        apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply')]")
        if apply_buttons:
            # Return HTML snippets for reference (could be useful for debugging)
            return {
                "entry_type": "apply_button",
                "elements": [btn.get_attribute("outerHTML") for btn in apply_buttons]
            }

        # Case 2: Form is already visible (heuristic: at least 3 input fields)
        form_fields = driver.find_elements(By.TAG_NAME, "input")
        if len(form_fields) >= 3:
            return {
                "entry_type": "visible_form",
                "elements": [field.get_attribute("outerHTML") for field in form_fields]
            }

        # Case 3: Account creation / login is required
        page_text = driver.page_source.lower()
        if "sign in" in page_text or "create account" in page_text:
            return {"entry_type": "account_required"}

        return {"entry_type": "unknown"}
    except Exception as e:
        return {"entry_type": "error", "error": str(e)}

# -----------------------------------------------------------------------------
# Function: get_next_action (Placeholder for LangGraph integration)
# -----------------------------------------------------------------------------
def get_next_action(observation):
    """
    Send the observation (dict) to a LangGraph agent and get the next action.
    Here we simulate this decision process.
    In production, replace this function with an actual call to your LangGraph agent.
    """
    # For demonstration, use a simple rule-based decision:
    if observation["entry_type"] == "apply_button":
        return {"action": "click", "target": "apply_button"}
    elif observation["entry_type"] == "visible_form":
        return {"action": "scroll", "target": "form"}
    elif observation["entry_type"] == "account_required":
        return {"action": "login", "target": "login_form"}
    else:
        return {"action": "unknown"}

# -----------------------------------------------------------------------------
# Function: perform_action
# -----------------------------------------------------------------------------
def perform_action(driver, action):
    """
    Use Selenium to perform an action based on the decision.
    """
    try:
        if action["action"] == "click" and action["target"] == "apply_button":
            # Find and click the first apply button
            apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply')]")
            if apply_buttons:
                apply_buttons[0].click()
                print("Clicked the apply button.")
            else:
                print("No apply button found to click.")
        elif action["action"] == "scroll" and action["target"] == "form":
            # Scroll down to help load the form (if it's dynamically loaded)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolled down to load form.")
        elif action["action"] == "login" and action["target"] == "login_form":
            # Example: click a 'Sign In' button. Adjust the XPath as needed.
            login_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Sign In')]")
            if login_buttons:
                login_buttons[0].click()
                print("Clicked the login button.")
            else:
                print("No login button found.")
        else:
            print("Unknown action received from LangGraph decision.")
    except Exception as e:
        print(f"Error performing action: {e}")

# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
def main():
    # Configure Chrome options (adjust as needed)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Set up the WebDriver (ensure chromedriver is in your PATH)
    driver = webdriver.Chrome(options=chrome_options)

    # List of job application URLs to process (example links)
    job_links = [
        "https://careers.roblox.com/jobs/6637846?gh_jid=6637846&gh_src=da92d0c91",
        "https://lifeattiktok.com/search/7480779960623008018?spread=5MWH5CQ",
    ]

    for link in job_links:
        print(f"\nProcessing job link: {link}")
        driver.get(link)
        time.sleep(3)  # Wait for page to load. Use explicit waits in production!

        # 1. Detect the application entry method
        observation = detect_application_entry(driver)
        print("Observation from detection:")
        print(json.dumps(observation, indent=2))

        # 2. Get decision from LangGraph agent (placeholder)
        decision = get_next_action(observation)
        print("Decision from LangGraph agent:")
        print(json.dumps(decision, indent=2))

        # 3. Perform the action
        perform_action(driver, decision)
        time.sleep(2)  # Allow time for the action to take effect

        # Further steps (like filling out the form) can be added here.
        # ...

    # Close the driver after processing all job links.
    driver.quit()

if __name__ == "__main__":
    main()
