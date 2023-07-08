# GitHub Pull Request Comments to Google Sheets

This script fetches all comments from all pull requests in a GitHub repository and appends them to a Google Spreadsheet.

## Prerequisites

- Python 3.x
- Google account with access to Google Sheets
- GitHub Personal Access Token
- Client JSON file for accessing the Google Sheets API

## Setup

1. Clone this repository or download the script file.

2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
3. Obtain a GitHub Personal Access Token:

- Go to your GitHub account settings.
- Navigate to "Developer settings" > "Personal access tokens".
- Click on "Generate new token" and provide a name for the token.
- Select the necessary scopes or permissions (e.g., repo:public_repo for accessing public repositories, or repo for accessing private repositories).
- Click on "Generate token" and make sure to copy and save the generated token.

4. Retrieve the client JSON file for accessing the Google Sheets API:

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing project.
- Navigate to the "APIs & Services" > "Credentials" page.
- Click on "Create credentials" and select "Service account".
- Provide a name for the service account, choose the appropriate role, and grant access to the Google Sheets API.
- Click on "Create" and skip the user access configuration.
- On the "Credentials" page, find the newly created service account and click on the three-dot menu, then select "Manage keys".
- Click on "Add key" > "Create new key" > JSON.
- Save the downloaded JSON key file to the same directory as the script and rename it to `client_secret.json`.

5. Open the `config.json` file and update the configuration values:

- `"github_token"`: Replace `"your-github-token"` with your GitHub Personal Access Token.
- `"repository_owner"`: Replace `"your-repository-owner"` with the owner/organization of the repository.
- `"repository_name"`: Replace `"your-repository-name"` with the name of the repository.
- `"google_credentials_file"`: Replace `"your-credentials-file"` with the filename of the client JSON file (e.g., `client_secret.json`).
- `"spreadsheet_id"`: Replace `"your-spreadsheet-id"` with the ID of the Google Spreadsheet you want to append the comments to.

## Running the Script

Run the script with Python:

```bash
python script.py
```

The script will fetch all comments from all pull requests in the specified GitHub repository and append them to the specified Google Spreadsheet. Each row in the spreadsheet will contain the number of the pull request, the username of the commenter, the body of the comment, the date of the comment, and the URL of the comment.
