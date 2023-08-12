import requests
import time

username = "YOUR_USERNAME"
url = f"https://api.github.com/users/{username}/repos"

access_token = "YOUR_ACCESS_TOKEN_HERE"
headers = {'Authorization': f'token {access_token}'}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Error fetching repositories: {response.status_code}")
    print(response.text)
    exit()

repos = response.json()
commit_counts = {}

for repo in repos:
    repo_name = repo['name']
    url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"

    for _ in range(1):
        response = requests.get(url, headers=headers)
        if response.status_code == 202:
            time.sleep(2)
            continue
        elif response.status_code != 200:
            print(f"Error fetching {repo_name}: {response.status_code}")
            print(response.text)
            break

        contributors_stats = response.json()

        for stats in contributors_stats:
            if stats['author']['login'] == username:
                commit_counts[repo_name] = stats['total']
        break

# 각 레포지토리와 커밋 횟수 출력
for repo_name, commits in commit_counts.items():
    print(f"Repository: {repo_name}, Commits: {commits}")

# 가장 많은 커밋을 한 프로젝트 찾기
if commit_counts:
    most_commited_repo = max(commit_counts, key=commit_counts.get)
    print(f"\nThe most committed project is {most_commited_repo} with {commit_counts[most_commited_repo]} commits.")
else:
    print("No commits found for the given username.")
