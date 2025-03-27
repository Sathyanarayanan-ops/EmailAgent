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

    def get_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Retrieves detailed information about a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            dict: A dictionary containing repository details or None if not found.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        return self._send_request(url)

    def get_commits(self, owner: str, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of commits for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of commit objects or None if no commits are found.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        return self._send_request(url)

    def get_commit_details(self, owner: str, repo: str, commit_sha: str) -> Optional[Dict]:
        """
        Retrieves detailed information about a specific commit.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.
            commit_sha (str): The commit SHA.

        Returns:
            dict: Detailed information about the commit.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
        return self._send_request(url)

    def get_branches(self, owner: str, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of branches for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of branch objects.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        return self._send_request(url)

    def get_repo_events(self, owner: str, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves the events associated with a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of event objects related to the repository.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/events"
        return self._send_request(url)

    def get_issues(self, owner: str, repo: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of issues for a specific repository.
        
        Args:
            owner (str): The GitHub username or organization name.
            repo (str): The repository name.

        Returns:
            List[Dict]: A list of issue objects.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        return self._send_request(url)


owner = "sathyanarayanan-ops"
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
# commits = github.get_commits(owner, "EmailAgent")
# print(commits)
# print("*************************\n")

commit_detail = github.get_commit_details(owner,"EmailAgent","ce036e249de72a38bbfaaa4ba907ed146c3d8f87")
print(commit_detail)


#  You can track the exact changes made to the getRepo.py file through the raw_url and patch data in the files section, which would provide detailed diffs (added and removed lines of code).
# The thing with getting the last commit from the project is that , it could be some minor issue commit such as adding/removing comments
# Thus have the option to get information from last 'n' commits 
