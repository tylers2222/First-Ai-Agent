from typing import List, Any, Optional
from simplegmail import Gmail
from dataclasses import dataclass
import os
from email.mime.text import MIMEText
import base64


@dataclass
class EmailMessage:
    to: str
    subject: str
    msg_plain: str
    thread_id: any

class Gmail_Client:
    def __init__(self, noauth_local_webserver):
        self.gmail = self._authenticate(noauth_local_webserver)

    def _authenticate(self, noauth_local_webserver: bool) -> Gmail:
        # Get the directory where this Python file is located (not where script is run from)
        # __file__ is the path to this .py file
        file_dir = os.path.dirname(os.path.abspath(__file__))  # gmail/ directory
        parent_dir = os.path.dirname(file_dir)  # Email Agent/ directory
        token_path = os.path.join(parent_dir, "gmail_token.json")
        
        if not os.path.exists(token_path):
            print("No gmail token json file found")
            raise FileNotFoundError(f"gmail_token.json not found in {parent_dir}")

        try:    
            print("   Creating Gmail instance...")
            gmail = Gmail(
                client_secret_file=os.path.join(parent_dir, "client_secret.json"),
                creds_file=token_path,
                noauth_local_webserver=noauth_local_webserver
            )
            print("✅ Gmail client initialised")
            return gmail
        except Exception as e:
            print(f"❌ Gmail init error: {e}")
            print(f"   Token path: {token_path}")
            print(f"   Token exists: {os.path.exists(token_path)}")
            raise
    
    def GetUnreadEmails(self, limit) -> List[Any]:
        try:
            messages = self.gmail.get_unread_inbox()
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return None

        if limit > 0:
            messages = messages[:limit]

        messages[0].plain

        print(f"Successfully returned {len(messages)} messages")
        return messages

    def GetEmailById(self, id):
        try:
            emails = self.gmail.get_unread_inbox()
            if not emails:
                print("No Unread Emails Returned")
                return None

            for email in emails:
                if email.id == id:
                    print(f"Email with Id {id} found")
                    return email

            print(f"❌ Email with ID {id} not found in unread inbox")
            return None

        except Exception as e:
            print(f"Error fetching emails: {e}")
            return None

    def MarkEmailAsRead(self, message) -> str:
        try:
            message.mark_as_read()
            return f"Successfully Marked Email: | {message.subject} from {message.sender} | as read"
        except Exception as e:
            return f"Mark as read error: {e}"

    def SendEmail(self, message: EmailMessage) -> str:
        param = {
            "to": message.to,
            "sender": "tylerstewart1204@gmail.com",
            "subject": message.subject,
            "msg_plain": message.msg_plain,
            "signature": False
        }

        try:
            message = self.gmail.send_message(**param)
            if message:
                return message
            else:
                return "failed to return message"
        except Exception as e:
            return f"Failed to create draft: {e}"

    def ReplyToEmail(self, message: EmailMessage) -> str:
        try:
            mime_msg = MIMEText(message.msg_plain)

            mime_msg["to"] = message.to
            mime_msg["from"] = "tylerstewart1204@gmail.com"
            mime_msg["subject"] = f"RE: {message.subject}" if message.subject else ""

            raw = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()

            msg = self.gmail.service.users().messages().send(
                userId="me",
                body={
                    "raw": raw,
                    "threadId": message.thread_id
                }
            ).execute()

            print(f"Successfully sent message: {msg}")
            return "Send was successful"

        except Exception as e:
            return f"Sending reply error: {e}"
