import os
import smtplib
import requests
import yagmail
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Load environment variables from the .env file
load_dotenv('.env')

# Get credentials and email address from environment variables
sender = os.getenv('USERNAME_ACCOUNT')
password = os.getenv('PASSWORD')
mail_to = os.getenv('MAIL_TO')

# Configure the email client
yag = yagmail.SMTP(user=sender, password=password)

# List of URLs to check
urls_to_check = [
    'https://blazedemo.com/',
    'https://blazedemo.com/reserve.php',
    'https://blazedemo.com/purchase.php'
]

listofUrls = {}
flag = True

# Check the status of each URL
for url in urls_to_check:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            message = f'Notification: The endpoint {url} is currently returning status code {response.status_code}. Thank you.'
            listofUrls[url] = response.status_code
            flag = False
        else:
            print(f'The endpoint {url} is functioning correctly.')
    except requests.exceptions.RequestException as e:
        listofUrls[url] = 'Connection Error'
        flag = False

# Create the email message
subject = "SEO Status: ERRORS IN THE FOLLOWING URLS"

email_body = "Good morning. The following links have reported errors in their status codes:\n"
email_body += "Reference: [LINK]  -  [ERROR]\n"

current_date = datetime.now().date()

# Create an Excel file with the results
df = pd.DataFrame(listofUrls.items(), columns=['URL', 'Error Status'])
excel_file = f"status_report_{current_date}.xlsx"
df.to_excel(excel_file, index=False)

# Add results to the message
for key, value in listofUrls.items():
    email_body += f"{key} : {value}\n"

email_body += "\nAn Excel file with more details is attached.\nThank you.\n"

# Send the email if there are errors
if not flag:
    yag.send(mail_to, subject, [email_body, excel_file])

print("The report has been sent successfully.")
