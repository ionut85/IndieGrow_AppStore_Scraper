import pandas as pd

emails_and_messages_df = pd.read_csv('emails_and_messages.csv')

# Remove duplicate entries
unique_emails_and_messages_df = emails_and_messages_df.drop_duplicates()

unique_emails_and_messages_df.to_csv('final_indie_app_developer_emails.csv', index=False)

print("Final emails and messages have been saved to final_indie_app_developer_emails.csv")