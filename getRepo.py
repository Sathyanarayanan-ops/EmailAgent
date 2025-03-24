'''

Script that uses Github Api , to get the authenticated user

THen get the user's repo


'''


import requests
import os 
import dotenv
from dotenv import load_dotenv, find_dotenv



dotenv_path = find_dotenv()
if not dotenv_path:
    print("⚠️ .env file not found! Ensure it's in the same directory as main.py.")
# Load the .env file explicitly
load_dotenv(dotenv_path)
#  Read the API Key
GH_API_KEY = os.getenv("GITHUB_API_KEY")




headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'Authorization': 'token YOUR_PERSONAL_ACCESS_TOKEN'
}
response = requests.get("https://api.github.com/user/repos", headers=headers)
json_data = response.json()

print(json_data)