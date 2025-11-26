from webbrowser import get
import os
import time

# Change to root directory where gmail_token.json is located BEFORE importing tools
os.chdir("..")

from tools import get_unread_emails, mark_single_email_as_read
from gmail.gmail_client import Gmail_Client

gmail = Gmail_Client(noauth_local_webserver=True)

def main():
    print("Testing tool")
    result = get_unread_emails.invoke({"limit": 3})
    print(f"Result: \n{result}")

    print("Starting marking as read tool")
    time.sleep(5)
    # getting the list of emails in the test but it will be the LLM that passes the input in prod
    email = gmail.GetUnreadEmails(1)

    res = mark_single_email_as_read.invoke({"id": email[0].id})
    print(f"Result: {res}")

if __name__ == '__main__':
    main()