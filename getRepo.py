'''

Script that uses Github Api , to get the authenticated user

THen get the user's repo


'''


import requests

headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'Authorization': 'token YOUR_PERSONAL_ACCESS_TOKEN'
}
response = requests.get("https://api.github.com/user/repos", headers=headers)
json_data = response.json()

print(json_data)