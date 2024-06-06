import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

def get_indie_apps(categories, country='us', limit=50):
    apps = []
    base_url = 'https://itunes.apple.com/{country}/rss/topfreeapplications/limit={limit}/genre={category}/xml'

    for category in categories:
        url = base_url.format(country=country, limit=limit, category=category)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml-xml')

        for entry in soup.find_all('entry'):
            app = {
                'name': entry.find('im:name').text,
                'developer': entry.find('im:artist').text,
                'homepage': entry.find('link', rel='alternate')['href'],
                'reviews': int(entry.find('im:ratingCount').text) if entry.find('im:ratingCount') else 0,
                'averageRating': float(entry.find('im:rating').text) if entry.find('im:rating') else 0.0
            }
            apps.append(app)
    return apps

def extract_emails(url, retries=3, delay=5, max_redirects=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    session.max_redirects = max_redirects

    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            return emails
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            time.sleep(delay)
    return []

def is_indie_developer(app):
    known_large_companies = ['Google', 'Microsoft', 'Facebook', 'Amazon', 'Apple', 'Zillow', 'Pinterest', 'Tinder', 'T-Mobile']
    if app['reviews'] > 5000 or app['developer'] in known_large_companies:
        return False
    return True

def create_email(app, your_name, location):
    email_template = f"""
    Subject: Quick Chat About Growing {app['name']}

    Hey {app['developer']} team,

    My name is {your_name} and I'm reaching out after checking out {app['name']} (downloaded it too, and I've used similar apps in the past).

    Right now, I'm building a product called IndieGrow to help indie app developers grow their user base in the early stages. I was wondering if you'd be available for a quick call in the next few days to chat about how you approach growing your app? What challenges you face and what you'd find valuable to get support with?

    We're also an indie dev team, probably facing the same challenges, but we'd like to validate them.

    Cheers from {location},
    {your_name}
    """
    return email_template.strip()

def remove_duplicates(emails_and_messages):
    seen = set()
    unique_emails_and_messages = []
    for entry in emails_and_messages:
        identifier = (entry['email'], entry['message'])
        if identifier not in seen:
            seen.add(identifier)
            unique_emails_and_messages.append(entry)
    return unique_emails_and_messages

# Parameters
your_name = "Ionut"
location = "Berlin"

categories = [
    '6012',  # Business
    '6013',  # Weather
    '6014',  # Utilities
    '6015',  # Travel
    '6016',  # Sports
    '6017',  # Social Networking
    '6018',  # Reference
    '6020',  # Productivity
    '6021',  # Photo & Video
    '6022',  # News
    '6023',  # Navigation
    '6024',  # Music
    '6025',  # Lifestyle
    '6026',  # Health & Fitness
    '6027',  # Finance
    '6028',  # Entertainment
    '6029',  # Education
    '6001',  # Medical
]

# Retrieve up to 50 apps per category
all_apps = get_indie_apps(categories, limit=50)
indie_apps = [app for app in all_apps if is_indie_developer(app)]

# Extracting emails and composing messages
emails_and_messages = []
for app in indie_apps:
    homepage = app.get('homepage')
    emails = extract_emails(homepage)
    app['emails'] = emails
    for email in emails:
        message = create_email(app, your_name, location)
        emails_and_messages.append({'email': email, 'message': message})

# Remove duplicate entries
unique_emails_and_messages = remove_duplicates(emails_and_messages)

# Convert the list of emails and messages to a DataFrame for better visualization
emails_df = pd.DataFrame(unique_emails_and_messages)

# Define the CSV file path
csv_file_path = 'indie_app_developer_emails.csv'

# Check if the file exists to determine the mode and header
if not os.path.isfile(csv_file_path):
    emails_df.to_csv(csv_file_path, index=False)
else:
    emails_df.to_csv(csv_file_path, mode='a', header=False, index=False)

print(f"Emails and messages have been saved to {csv_file_path}")