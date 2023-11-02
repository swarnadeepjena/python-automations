#install python & request
import requests  # Import the 'requests' library

# Set your GitHub repository and personal access token (PAT) here.
repository = 'sg-matverse/CLADMA-ml-models'  # Replace with your repository name
token = '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'  # Replace with your PAT

# Define the workflow file to trigger.
workflow_file = 'cladma-cicd.yml'  # Replace with your workflow file name

# Define the branch or event that triggers the workflow (optional).
ref = 'main'  # Replace with the branch or event you want to trigger

# Construct the URL for triggering the workflow.
url = f'https://api.github.com/repos/{repository}/actions/workflows/{workflow_file}/dispatches'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

data = {
    'ref': ref,
}

# Send a POST request to trigger the workflow.
response = requests.post(url, headers=headers, json=data)

if response.status_code == 204:
    print(f"GitHub Action '{workflow_file}' triggered successfully.")
else:
    print(f"Failed to trigger GitHub Action. Status code: {response.status_code}")
    print(f"Response content: {response.content.decode('utf-8')}")
