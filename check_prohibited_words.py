import os
import sys
from github import Github
import json

# List of prohibited words
PROHIBITED_WORDS = ['badword1', 'badword2', 'example']

# Authenticate with GitHub
g = Github(os.getenv('GITHUB_TOKEN'))

# Read the PR number from the GitHub Actions context
with open(os.getenv('GITHUB_EVENT_PATH')) as f:
    event_data = json.load(f)

pr_number = event_data['pull_request']['number']
repo_name = os.getenv('GITHUB_REPOSITORY')
repo = g.get_repo(repo_name)

# Get the pull request details
pr = repo.get_pull(pr_number)

# Now let's check the content of the changed files in the PR
files = pr.get_files()  # This retrieves all the files changed in the PR

for file in files:
    file_name = file.filename
    file_patch = file.patch  # The patch is the diff of the changes made to the file
    
    # Check for prohibited words in the diff (code changes)
    for word in PROHIBITED_WORDS:
        if word.lower() in file_patch.lower():
            print(f"Prohibited word '{word}' found in file {file_name} diff.")
            sys.exit(1)

print("No prohibited words found in PR description, title, or file contents.")
