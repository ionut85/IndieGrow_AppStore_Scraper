import smtplib
import pandas as pd
from email.message import EmailMessage
import os
my_secret = os.environ['IndieGrowSMTP']
my_smtp = os.environ['my_email_smtp']
my_test = os.environ['my_test_email']

def send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to_email

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

def main(test_mode=True):
        # Load the CSV file
        emails_df = pd.read_csv('final_indie_app_developer_emails.csv')

        # Email server configuration
        smtp_server = 'smtp.gmail.com'  # Change this if you're using another email provider
        smtp_port = 465  # Change the port if needed
        smtp_username = my_smtp  # Your email address
        smtp_password = my_secret  # Your email password (consider using an app-specific password)

        if test_mode:
            emails_df = emails_df.head(2)  # Select only the top 3 emails for test mode
            test_email = my_test

        for _, row in emails_df.iterrows():
            to_email = test_email if test_mode else row['email']
            message_lines = row['message'].split('\n')
            subject = message_lines[0].replace('Subject: ', '').strip()  # Extracting the subject from the message and removing 'Subject:'
            message_body = '\n'.join(message_lines[1:]).strip()  # Exclude the subject line from the email body

            try:
                send_email(smtp_server, smtp_port, smtp_username, smtp_password, to_email, subject, message_body)
                print(f"Email sent to {to_email}")
            except Exception as e:
                print(f"Failed to send email to {to_email}: {e}")

if __name__ == "__main__":
        main()