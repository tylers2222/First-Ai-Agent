import unittest
import os
import time
import re
import sys

print("1) Basic imports done")

# Change to Email Agent directory where gmail_token.json is located BEFORE importing agent
# Get the directory where this script is located, then go up one level to Email Agent/
script_dir = os.path.dirname(os.path.abspath(__file__))  # gmail/ directory
email_agent_dir = os.path.dirname(script_dir)  # Email Agent/ directory
os.chdir(email_agent_dir)

# Add Email Agent directory to path so we can import utils
sys.path.insert(0, email_agent_dir)
print("2) Changed dir")

from typing import List
from langchain_core._api.path import HERE
from gmail_client import Gmail_Client, EmailMessage
from utils.match_email import extract_email

print("3) Imports done")

class GmailTest(unittest.TestCase):
    def setUp(self):
        print("Starting up gmail client")
        self.client = Gmail_Client(noauth_local_webserver=True)
        print("Gmail client created")

    def test_get_unread_emails(self):
        print("Starting get the unread emails")
        emails = self.client.GetUnreadEmails(5)
        print(f"{len(emails)} Emails Found")
        self.assertIsInstance(emails, list)

    def test_sending_email(self):
        m = EmailMessage(
            to= "luke.hallal@gmail.com",
            subject= "Hey Lu, Sent From Agent",
            msg_plain= """
Hey Lu,

Im literally sending this from my agent Lu, it is a strictly typed variable though thats why i can be so funny here.

I highly doubt an LLM would call you Lu though right, that would be insane.

anyways, good luck tn Lu, hope you score and hope this email finds you well

Ty
            """
        )

        r = self.client.SendEmail(m)

        print(f"Result: {r}")



if __name__ == '__main__':
    # unittest.main()
    # replying_to_email()
    print("Running gmail test")

    g = GmailTest()
    g.setUp()
    g.test_get_unread_emails()