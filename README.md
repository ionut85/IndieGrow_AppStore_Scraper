# IndieGrow_AppStore_Scraper
Scrape the iOS AppStore and send Personalized emails to IndieDevs

## IndieGrow AppStore Scraper

### Description

IndieGrow AppStore Scraper is a tool designed to help indie app developers grow their user base by reaching out to them directly. This script scrapes the Apple AppStore to find indie app developers, extracts their contact information, and sends personalized emails to them. It includes functionalities to filter out non-indie developers, extract email addresses from developer homepages, and send emails using an SMTP server.

### Features

- Scrapes the Apple AppStore for app details and developer information.
- Filters out large companies and game apps to focus on indie developers.
- Extracts email addresses from both the AppStore pages and developer homepages.
- Sends personalized emails to the extracted contacts.
- Includes a test mode to send emails to a test address for verification.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ionut85/indiegrow_appstore_scraper.git
   cd indiegrow-appstore-scraper
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - In Replit or your local environment, set the following environment variables:
     - `my_email_smtp` - Your SMTP server (e.g., `smtp.gmail.com`).
     - `my_email_address` - Your email address.
     - `my_email_password` - Your email password.

### Usage

1. **Run the main script to perform all steps sequentially:**
   ```bash
   python main.py
   ```

2. **Scripts can also be run individually:**
   - **Step 1: Scrape Apps and URLs**
     ```bash
     python step1_scrape_apps_and_urls.py
     ```
   - **Step 2: Filter Indie Developers**
     ```bash
     python step2_filter_indie_developers.py
     ```
   - **Step 3: Extract Emails**
     ```bash
     python step3_extract_emails.py
     ```
   - **Step 4: Create Personalized Emails**
     ```bash
     python step4_generate_emails_and_messages.py
     ```
   - **Step 5: Send Emails**
     ```bash
     python send_emails.py
     ```

### Configuration

- **Test Mode:**
  By default, the script runs in test mode and sends emails to the test email address (`xxx@xxx.com). To send emails to actual developers, set `test_mode=False` in the `main()` function call in `main.py`.

### Example

Emails are not sent automatically in order to be manually checked; 
You can send them afterward after completing the other steps by running the send_emails.py script

### License

This project is licensed under the MIT License.

### Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!