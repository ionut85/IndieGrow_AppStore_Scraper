import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def extract_emails(url, retries=3, delay=5, max_redirects=10, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    session.max_redirects = max_redirects

    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Define the sections to search for emails
                email_sections = soup.find_all(['p', 'div', 'span', 'a'], class_=lambda x: x not in ['we-customer-review'])
                email_text = ' '.join([section.get_text() for section in email_sections])

                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_text)
                # Debugging: Print the emails found
                print(f"Extracted emails from {url}: {emails}")
                return emails
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            time.sleep(delay)
    return []

def get_developer_homepage(app_store_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(app_store_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the developer's homepage link using the specific class and text
            a_tag = soup.find('a', class_='link icon icon-after icon-external', string=re.compile('Developer Website'))
            if a_tag and 'href' in a_tag.attrs:
                return a_tag['href']

            # If Developer Website is not found, try to find App Support link
            a_tag = soup.find('a', class_='link icon icon-after icon-external', string=re.compile('App Support'))
            if a_tag and 'href' in a_tag.attrs:
                return a_tag['href']
    except Exception as e:
        print(f"Failed to fetch {app_store_url}: {e}")
    return None

def get_priority_email(emails):
    # Placeholder function to prioritize emails
    # Customize this function as needed
    return sorted(emails)[0] if emails else None

# Load apps and URLs from the previous step
apps_df = pd.read_csv('apps_and_urls.csv')

# Prepare a list to store the results
results = []

for _, row in apps_df.iterrows():
    app_store_url = row['homepage']
    app_name = row['name']
    developer = row['developer']

    # First, try to extract emails from the App Store page
    emails = extract_emails(app_store_url)

    if not emails:
        # If no emails are found, try to get the developer's homepage and extract emails from there
        developer_homepage = get_developer_homepage(app_store_url)
        if developer_homepage:
         #   print(f"Found developer homepage or support page: {developer_homepage}")
            emails = extract_emails(developer_homepage)
         #else:
         #   print(f"No developer homepage or support page found for {app_store_url}")

    if emails:
        primary_email = get_priority_email(emails)
        results.append({
            'email': primary_email,
            'app_name': app_name,
            'developer': developer,
            'homepage': developer_homepage if 'developer_homepage' in locals() and developer_homepage else app_store_url
        })

# Create a DataFrame and save to CSV
emails_df = pd.DataFrame(results)
emails_df.drop_duplicates(subset=['developer'], keep='first', inplace=True)  # Deduplicate by developer
emails_df.to_csv('extracted_emails.csv', index=False)

print("Emails have been extracted and saved to extracted_emails.csv")