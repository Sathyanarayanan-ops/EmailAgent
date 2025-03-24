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




def get_repo_list()-> list:
        
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {GH_API_KEY}'  # Add 'Bearer' prefix
    }

    # Send the request to GitHub API
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    # Check if request is successful
    if response.status_code == 200:
        repo_list_json = response.json()
        
        repo_names = [repo['name'] for repo in repo_list_json]
        return repo_names
        # print(repo_list_json)
    else:
        print(f"Request failed with status code: {response.status_code}")
        
        
    

def get_repo_details(owner,repo):
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {GH_API_KEY}'  # Authorization with Bearer token
    }
    
        # Send the request to the GitHub API to get repository info
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None
    
owner = "sathyanarayanan-ops"
repo = "EmailAgent"
repo_data  = get_repo_details(owner,repo)

if repo_data:
    print(repo_data)