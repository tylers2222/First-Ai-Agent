from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import json
from dotenv import load_dotenv
from gmail.gmail_client import Gmail_Client, EmailMessage
from utils.match_email import extract_email

load_dotenv()

app = App(token=os.environ["SLACK_TOKEN"])
gmail = Gmail_Client(noauth_local_webserver=True)

def extract_data_from_blocks(blocks) -> dict:
    """Extract the data from slacks return json """

    try:
        to = blocks[0]["text"]["text"].split(": ")[1] #"Sender: jason.acker@gmail.com"
        subject = blocks[1]["text"]["text"].split(": ")[1]
        msg = blocks[3]["text"]["text"].split(": ")[1]
        thread_id = blocks[4]["text"]["text"].split(": ")[1]

        to = extract_email(to)

        print(f"to: {to} -- subject: {subject} -- msg: {msg} -- thread_id: {thread_id}")

        return {
            "to": to,
            "subject": subject,
            "msg": msg,
            "thread_id": thread_id,
        }

    except Exception as e:
        print(f"Error extracting block: {e}")
        return None


@app.action("approve_draft")
def handle_approve(ack, body, client):
    ack()

    print("=" * 60)
    print("=" * 60)

    data = extract_data_from_blocks(body["message"]["blocks"])
    if not data:
        print("Couldnt get the data from slack")
        return

    real_email = extract_email(data["to"])

    try:
        e = EmailMessage(
            to = real_email,
            subject = data["subject"],
            msg_plain = data["msg"],
            thread_id = data["thread_id"],
        )

        resp = gmail.ReplyToEmail(e)
        print(f"Email Result: {resp}")

        if "HttpError" in resp:
            print(f"To: {real_email}")
            print(f"Thread_Id: {data["thread_id"]}")
            return

        #impl a message back to slack in the future

    except Exception as e:
        print(f"Send Email Error: {e}")
        print(f"To: {real_email}")
        print(f"Thread_Id: {data["thread_id"]}")
        return


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("Starting Socket Mode...")
    handler.start()