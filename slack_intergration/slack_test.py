import os

os.chdir("..")

from slack_client import SlackClient
from gmail.gmail_client import EmailMessage

incoming_email = "Hey Tyler,\n\nHope you're well, just reaching out regarding your rsvp to this weeks work party, let me know\n\nRegards, Jason"
draft = "Hey Jason,\n\nYes will be attending\n\nRegards Tyler"
message_id = 23534562
thread_id = 2502535

slack = SlackClient()

e  = EmailMessage(
    to = "jason.acker@gmail.com",
    subject = "Work Party RSVP",
    msg_plain = "Hey Jason,\n\nYes will be attending\n\nRegards Tyler",
    thread_id = thread_id
)

def test_sending_message():
    slack.send_message("Hello World")

def test_sending_email():
    slack.send_email(e, incoming_email)

if __name__ == '__main__':
    test_sending_email()