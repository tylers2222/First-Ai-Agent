import slack
import os
import sys
from dotenv import load_dotenv
import time
import datetime

# Add parent directory to path so we can import gmail
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmail.gmail_client import EmailMessage

load_dotenv()

email_channel_id = os.environ["EMAIL_CHANNEL"]

class SlackClient:
    def __init__(self):
        try:
            self.slack = slack.WebClient(token=os.environ["SLACK_TOKEN"])
        except Exception as e:
            print(f"ERROR: {e}")

    def send_message(self, msg: str):
        try:
            self.slack.chat_postMessage(channel=email_channel_id, text=msg)
        except Exception as e:
            print(f"ERROR Sending Message: {e}")
    def send_email(self, email: EmailMessage, draft_reply: str):
        # a specific impl for sending emails
        try:
            self.slack.chat_postMessage(
                channel=email_channel_id,
                text=f"New Draft Ready To Approve - {datetime.datetime.now()}",
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"Sender: {email.to}"
                        }
                    },

                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"Subject: {email.subject}"
                        }
                    },
                    
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Original Email: {email.msg_plain}"
                        }
                    },

                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Draft Email: {draft_reply}"
                        }
                    },

                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Message_Id: {email.thread_id}"
                        }
                    },

                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "✅ Approve & Send"},
                                "style": "primary",
                                "value": f"approve_{email.to}_email",
                                "action_id": "approve_draft"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "❌ Reject"},
                                "style": "danger",
                                "value": f"approve_{email.to}_email",
                                "action_id": "reject_draft"
                            }
                        ]
                    }
                ]
            )

            print("Successfully sent email")
        except Exception as e:
            print(f"Error sending email to slack: {e}")