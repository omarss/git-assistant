# GitHub Pull Request Comments to Google Sheets

This script fetches all comments from all pull requests in a GitHub repository and appends them to a Google Spreadsheet.

## Prerequisites

- Python 3
- `gspread` and `oauth2client` Python libraries. You can install these with pip:

    ```
    pip install gspread oauth2client
    ```

- A GitHub personal access token. You can create one in the [GitHub settings](https://github.com/settings/tokens).
- The owner and name of the GitHub repository you want to fetch comments from.
- A Google Spreadsheet that you have edit permissions to, and its ID. You can find the ID in the URL of the spreadsheet. For example, in the URL `https://docs.google.com/spreadsheets/d/1qPyC1RvkRHIANr1I2A4efA8YU1ZiV1HkVJxPv3Sv3iw/edit#gid=0`, the ID is `1qPyC1RvkRHIANr1I2A4efA8YU1ZiV1HkVJxPv3Sv3iw`.
- A JSON key file for a Google service account that has edit permissions to the Google Spreadsheet. You can create a service account and download the JSON key file in the [Google Cloud Console](https://console.cloud.google.com/).

## Configuration

Create a `config.json` file in the same directory as the script, with the following content:

```json
{
    "github_token": "your-token-here",
    "repository_owner": "owner",
    "repository_name": "repo",
    "google_credentials_file": "client_secret.json",
    "spreadsheet_id": "your-spreadsheet-id"
}

Replace `"your-token-here"`, `"owner"`, `"repo"`, `"client_secret.json"`, and `"your-spreadsheet-id"` with your own values.

## Running the Script

Run the script with Python:

```bash
python script.py

The script will fetch all comments from all pull requests in the specified GitHub repository and append them to the specified Google Spreadsheet. Each row in the spreadsheet will contain the number of the pull request, the username of the commenter, the body of the comment, the date of the comment, and the URL of the comment.
