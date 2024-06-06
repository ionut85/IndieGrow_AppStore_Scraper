import requests
from bs4 import BeautifulSoup
import pandas as pd

def is_large_company(app_data):
    large_company_keywords = ['Inc.', 'Ltd.', 'Corp.', 'LLC', 'Google', 'Microsoft', 'Facebook', 'Amazon', 'Apple', 'Zynga']
    developer_name = app_data.get('artistName', '')
    if any(keyword in developer_name for keyword in large_company_keywords):
        return True
    return app_data.get('userRatingCount', 0) > 5000

def get_apps_and_urls(categories, country='us', limit=15):
    apps = []
    base_url = 'https://itunes.apple.com/{country}/rss/topfreeapplications/limit={limit}/genre={category}/xml'
    search_api_url = 'https://itunes.apple.com/lookup?id={app_id}&country={country}'

    for category in categories:
        url = base_url.format(country=country, limit=limit, category=category)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml-xml')

        for entry in soup.find_all('entry'):
            app_id = entry.find('id').text.split('/id')[-1].split('?')[0]
            search_url = search_api_url.format(app_id=app_id, country=country)
            try:
                search_response = requests.get(search_url)
                search_response.raise_for_status()

                app_data = search_response.json().get('results', [{}])[0]

                # Exclude games
                if app_data.get('primaryGenreName', '').lower() == 'games':
                    continue

                # Exclude apps with 0 ratings or from large companies
                if app_data.get('userRatingCount', 0) == 0 or is_large_company(app_data):
                    continue

                # Commented out the print statement
                # print(f"Fetched data for app ID {app_id}: {app_data}")

                app = {
                    'name': entry.find('im:name').text,
                    'developer': entry.find('im:artist').text,
                    'homepage': entry.find('link', rel='alternate')['href'],
                    'reviews': app_data.get('userRatingCount', 0)
                }
                apps.append(app)
            except requests.exceptions.RequestException as e:
                print(f"Request failed for app ID {app_id}: {e}")
            except ValueError as e:
                print(f"JSON decode failed for app ID {app_id}: {e}")
    return apps

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

all_apps = get_apps_and_urls(categories, limit=15)
apps_df = pd.DataFrame(all_apps)
apps_df.to_csv('apps_and_urls.csv', index=False)

print("Apps and URLs have been saved to apps_and_urls.csv")