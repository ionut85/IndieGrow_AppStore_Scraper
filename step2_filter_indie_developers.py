import pandas as pd

def is_indie_developer(app):
    known_large_companies = ['Google', 'Microsoft', 'Facebook', 'Amazon', 'Apple', 'Zillow', 'Pinterest', 'Tinder', 'T-Mobile']
    if app['reviews'] > 5000 or app['developer'] in known_large_companies:
        return False
    return True

apps_df = pd.read_csv('apps_and_urls.csv')
indie_apps = [app for _, app in apps_df.iterrows() if is_indie_developer(app)]

indie_apps_df = pd.DataFrame(indie_apps)
indie_apps_df.to_csv('filtered_indie_apps.csv', index=False)

print("Filtered indie apps have been saved to filtered_indie_apps.csv")