import pandas as pd

def is_personal_name(developer):
    # A basic heuristic to determine if the developer name is a personal name
    if len(developer.split()) <= 3:  # If the name has three words or less, assume it's a personal name
        return True
    return False

def create_email(app_name, developer, your_name, location):
    if is_personal_name(developer):
        salutation = f"Hey {developer},"
    else:
        salutation = f"Hey {developer} team,"

    email_template = f"""
    Subject: Quick Chat About Growing {app_name}

    {salutation}

    My name is {your_name} and I'm reaching out after checking out {app_name} (downloaded it too, and I've used similar apps in the past).

    Right now, I'm building a product called IndieGrow to help indie app developers grow their user base in the early stages. I was wondering if you'd be available for a quick call in the next few days to chat about how you approach growing your app? What challenges you face and what you'd find valuable to get support with?

    We're also an indie dev team, probably facing the same challenges, but we'd like to validate them.

    Cheers from {location},
    {your_name}
    """
    return email_template.strip()

emails_df = pd.read_csv('extracted_emails.csv')

your_name = "Ionut"
location = "Berlin"

emails_and_messages = []
for _, row in emails_df.iterrows():
    email = row['email']
    app_name = row['app_name']
    developer = row['developer']
    message = create_email(app_name, developer, your_name, location)
    emails_and_messages.append({'email': email, 'message': message})

emails_and_messages_df = pd.DataFrame(emails_and_messages)
emails_and_messages_df.to_csv('emails_and_messages.csv', index=False)

print("Emails and messages have been saved to emails_and_messages.csv")