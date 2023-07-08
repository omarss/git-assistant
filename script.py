import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json

# Load configuration from a JSON file
with open('config.json') as f:
    config = json.load(f)

try:
    github_token = config['github_token']
    headers = {'Authorization': f'token {github_token}'}
    repository_owner = config['repository_owner']
    repository_name = config['repository_name']
    credentials_file = config['google_credentials_file']
    spreadsheet_id = config['spreadsheet_id']

    # Use your own JSON key file
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file, scope)
    google_client = gspread.authorize(credentials)

    # Open the Google Spreadsheet by its ID (make sure you have edit permissions to it)
    spreadsheet = google_client.open_by_key(spreadsheet_id).sheet1

    def fetch_all_pages(url):
        """Fetch all pages of results from a URL using the GitHub API."""
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise requests.HTTPError(
                    f'Failed to fetch: {response.status_code}')
            yield from response.json()
            links = requests.utils.parse_header_links(
                response.headers['Link'].rstrip('>').replace('>,<', ',<'))
            url = next((link['url']
                       for link in links if link['rel'] == 'next'), None)

    pull_requests_url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/pulls'
    pull_requests = fetch_all_pages(pull_requests_url)

    for pull_request in pull_requests:
        pull_request_number = pull_request['number']
        comments_url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/pulls/{pull_request_number}/comments'
        comments = fetch_all_pages(comments_url)
        for comment in comments:
            row = [pull_request_number, comment['user']['login'],
                   comment['body'], comment['created_at'], comment['html_url']]
            spreadsheet.append_row(row)

except FileNotFoundError:
    print("Error: Configuration file 'config.json' not found.")
    print("Please make sure the 'config.json' file is present and contains the required configuration.")
except KeyError as e:
    print(f"Error: Missing key '{e.args[0]}' in the configuration file.")
    print("Please make sure all the required keys are present in the 'config.json' file.")
except gspread.exceptions.APIError as e:
    print("Error: Google Sheets API error occurred.")
    print("Please check your Google Sheets API credentials and make sure you have proper permissions.")
except requests.exceptions.RequestException:
    print("Error: Failed to connect to the GitHub API.")
    print("Please check your internet connection and try again.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print("Please check the script and the configuration file for any issues.")
