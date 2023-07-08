import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Load configuration from a JSON file
with open('config.json') as f:
    config = json.load(f)

github_token = config['github_token']
headers = {'Authorization': f'token {github_token}'}
repository_owner = config['repository_owner']
repository_name = config['repository_name']

# Use your own JSON key file
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    config['google_credentials_file'], scope)
google_client = gspread.authorize(credentials)

# Open the Google Spreadsheet by its ID (make sure you have edit permissions to it)
spreadsheet_id = config['spreadsheet_id']
spreadsheet = google_client.open_by_key(spreadsheet_id).sheet1


def fetch_all_pages(url):
    """Fetch all pages of results from a URL using the GitHub API."""
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print('Failed to fetch:', response.status_code)
            break
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
