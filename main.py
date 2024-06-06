import subprocess
import os

def run_script(script_name):
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def pause_for_user():
    input("Press Enter to continue to the next step...")

def main():
    scripts = [
        'step1_scrape_apps_and_urls.py',
        'step2_filter_indie_developers.py',
        'step3_extract_emails.py',
        'step4_generate_emails_and_messages.py',
        'step5_combine_and_save_final_csv.py'
    ]

    print("Running Step 1: Scrape Apps and URLs")
    run_script(scripts[0])
    print("Step 1 completed. Please review the 'apps_and_urls.csv' file.")
    pause_for_user()

    print("Running Step 2: Filter Indie Developers")
    run_script(scripts[1])
    print("Step 2 completed. Please review the 'filtered_indie_apps.csv' file.")
    pause_for_user()

    print("Running Step 3: Extract Emails")
    run_script(scripts[2])
    print("Step 3 completed. Please review the 'extracted_emails.csv' file.")
    pause_for_user()

    print("Running Step 4: Generate Emails and Messages")
    run_script(scripts[3])
    print("Step 4 completed. Please review the 'emails_and_messages.csv' file.")
    pause_for_user()

    print("Running Step 5: Combine and Save Final CSV")
    run_script(scripts[4])
    print("Step 5 completed. Please review the 'final_indie_app_developer_emails.csv' file.")

if __name__ == "__main__":
    main()