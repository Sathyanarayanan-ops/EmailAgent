import os
import logging
import requests
import dotenv
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict, Optional

# Custom exception for GitHub API errors
class GitHubAPIError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class GitHubAPI:
    """
    A class for interacting with the GitHub API to retrieve repository, commit, 
    branch, issue, and event details from a user's GitHub account.
    """
    # OWNER = "sathyanarayanan-ops"

    def __init__(self):
        """
        Initializes the GitHubAPI class by loading the GitHub API key from 
        environment variables and setting up headers for API requests.
        """
        dotenv_path = find_dotenv()
        if not dotenv_path:
            raise FileNotFoundError(".env file not found! Ensure it's in the same directory as the script.")
        
        load_dotenv(dotenv_path)
        
        self.GH_API_KEY = os.getenv("GITHUB_API_KEY")
        
        if not self.GH_API_KEY:
            raise ValueError("GitHub API Key is missing from environment variables.")
        
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {self.GH_API_KEY}'
        }
        self.owner = "sathyanarayanan-ops"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def _send_request(self, url: str) -> Dict:
        """
        A helper function to send a GET request to the GitHub API.
        
        Args:
            url (str): The API endpoint to send the GET request to.

        Returns:
            dict: The response JSON if successful, otherwise raises GitHubAPIError.
        """
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Request to {url} failed with status code: {response.status_code}")
            raise GitHubAPIError(f"Request failed for {url} with status code: {response.status_code}")

    def get_repo_list(self) -> List[str]:
        """
        Retrieves the list of repositories for the authenticated user.
        
        Returns:
            List[str]: A list of repository names.
        """
        url = "https://api.github.com/user/repos"
        repo_list_json = self._send_request(url)
        return [repo['name'] for repo in repo_list_json]

    def get_repo_details(self, repo: str) -> Optional[Dict]:
        """
        Retrieves detailed information about a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            dict: A dictionary containing repository details or None if not found.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}"
        return self._send_request(url)

    def get_commits(self, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of commits for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of commit objects or None if no commits are found.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/commits"
        return self._send_request(url)

    def get_commit_details(self, repo: str, commit_sha: str) -> Optional[Dict]:
        """
        Retrieves detailed information about a specific commit.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.
            commit_sha (str): The commit SHA.

        Returns:
            dict: Detailed information about the commit.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/commits/{commit_sha}"
        
        details = self._send_request(url)
        
        return self._send_request(url)

    def get_branches(self, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of branches for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of branch objects.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/branches"
        return self._send_request(url)

    def get_repo_events(self,  repo: str) -> Optional[List[Dict]]:
        """
        Retrieves the events associated with a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of event objects related to the repository.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/events"
        return self._send_request(url)

    def get_issues(self, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of issues for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of issue objects.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/issues"
        return self._send_request(url)
    
    def compare_commits(self,repo, base_commit_sha, head_commit_sha):
        """
        Compare two commits in a GitHub repository to see the differences between them.
        
        Args:
            owner (str): The GitHub username or organization.
            repo (str): The repository name.
            base_commit_sha (str): The SHA of the base commit (older commit).
            head_commit_sha (str): The SHA of the head commit (newer commit).

        Returns:
            dict: A dictionary containing the comparison details, including file changes.
        """
        url = f"https://api.github.com/repos/{self.owner}/{repo}/compare/{base_commit_sha}...{head_commit_sha}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
        
    def extract_code_changes(self,compare_response):
        """
        Extracts only the code changes (diffs) from the GitHub commit comparison response.

        Args:
            compare_response (dict): The response from the GitHub compare commits API.

        Returns:
            list: A list of code changes (diffs) in a human-readable format.
        """
        code_changes = []
        
        if not compare_response:
            return []

        # Loop through the 'files' section to extract diffs from the patch field
        for file in compare_response.get('files', []):
            filename = file.get('filename', 'N/A')
            patch = file.get('patch', None)

            if patch:
                code_changes.append({
                    'filename': filename,
                    'patch': patch
                })
        
        return code_changes
        

# Check compare commit functions 



# Example usage of the GitHubAPI class
github = GitHubAPI()

# Get the repo list
# repo_names = github.get_repo_list()
# print(repo_names)
# print("*************************\n")
# # Get details of a specific repository
# repo_data = github.get_repo_details(owner, "EmailAgent")
# print(repo_data)
# print("*************************\n")
# # Get commits for a specific repository
# commits = github.get_commits("EmailAgent")
# print(commits)
# print("*************************\n")

# commit_detail = github.get_commit_details("EmailAgent","ce036e249de72a38bbfaaa4ba907ed146c3d8f87")
# print(commit_detail)


compare_response = github.compare_commits("EmailAgent","2e745293e90dc0c4053de48134b9be73e07da43d","78b59c919cd4f7367c61c2b01baebd4009acc2e2")

code_changes = github.extract_code_changes(compare_response)
print(code_changes)
# print(compare_commits)




#  You can track the exact changes made to the getRepo.py file through the raw_url and patch data in the files section, which would provide detailed diffs (added and removed lines of code).
# The thing with getting the last commit from the project is that , it could be some minor issue commit such as adding/removing comments
# Thus have the option to get information from last 'n' commits 




