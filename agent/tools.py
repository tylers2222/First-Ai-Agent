from langchain_openai import ChatOpenAI
from typing import Any, List
import sys
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum

# Add parent directory to path so we can import gmail
# MUST be before any gmail imports!
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmail.gmail_client import Gmail_Client, EmailMessage
from langchain.tools import tool

from slack_intergration.slack_client import SlackClient

gmail = Gmail_Client(noauth_local_webserver=True)
slack = SlackClient()
no_emails = "No unread emails"

load_dotenv()


class EmailCategory(str, Enum):
    PERSONAL = "personal"
    BRANDED = "branded"
    INFORMATIONAL = "informational"
    TRANSACTIONAL = "transactional"
    UNKNOWN = "unknown"

class EmailClassification(BaseModel):
    category: EmailCategory = Field(description="the email category")
    reasoning: str = Field(description="Brief explination of how the category was satisfied")

classifier_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
).with_structured_output(EmailClassification)

@tool
def classify_email_into_category(email_content: str) -> str:
    """
    Classify an email into categories: personal, branded, information, transactional, or unknown.
    """
    
    # Don't use nested braces, just interpolate directly
    prompt = f"""Classify this email into ONE category:

Categories:
1. Personal Needing Response: 
    - Email from another person needing responding to
    - Often from a gmail account address or a personal name in the senders email address

2. Personal Not Needing Response:
    - Often at the end of a thread, if all the responding has been done
    - Sometimes a personal email just needs acknowledgement with a read such as an invite somehwere

3. Branded: 
    - Email from a brand with promotions/marketing
    - Sales and Discounts
    - Generic content related to what they would do. Example: Linkedin send an email saying "we found jobs you'd be a match for" its branded because its just a generic email
    - It aims to get you on their app
    - Something a company would send all the time

4. Informational: 
    - Informational updates (not promotional or transactional)
    - Example: Company has an outage or your payment is due tomorrow

5. Transactional: 
    - Receipt, purchase confirmation, order update
    - Post purchase book keeping

6. Unknown: 
    - Doesn't fit any above categories

Email content:
{email_content}

Think:
1. Who sent this (company, personal email, brand)
2. What is the purpose (inform, get person back on their app, notify, transaction)
3. Which category fits best?

Respond with ONLY the category name in lowercase, nothing else."""
    
    result = classifier_llm.invoke(prompt)
    category = result.category.strip().lower()
    reasoning = result.reasoning
    print(f"Reasoning: {reasoning}")
    return f"Email classified as: {category}"

@tool
def get_unread_emails(limit: int) -> str:
    """Tool that gets all the unread emails up until a certain limit and returns a formatted list with the summary of sender and email contents etc"""

    emails = gmail.GetUnreadEmails(limit)
    if not emails:
        return no_emails

    res = []
    for i, email in enumerate(emails):
        e = f"""
        {i}. ID: {email.thread_id}
        
        Subject: {email.subject}
        Sender: {email.sender}
        Email: {email.plain}
        """
        res.append(e)

    return "\n".join(res)

@tool
def mark_single_email_as_read(id) -> str:
    """
    Tool to turn an unread email into read via the gmail SDK
    Function input is the index of an email and marks it as read
    """

    message = gmail.GetEmailById(id=id)
    if not message:
        return no_emails

    return gmail.MarkEmailAsRead(message=message)



writer_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)

# build a writing part here
@tool 
def send_email(to: str, subject: str, msg: str) -> str:
    """
    Tool to send emails

    Dont use em dashes, keep it professional but personalable. Like a regular human speaks

    Sign off with Email with my name Tyler
    """

    m = EmailMessage(
        to=to,
        subject=subject,
        msg_plain=msg,
        thread_id=None
    )

    return gmail.SendEmail(m)

@tool 
def reply_to_an_email(to: str, subject: str, msg: str, thread_id: str) -> str:
    """
    Tool to reply to an email in the format that actually creates a thread of reply emails, instead of just a regular email back

    Get the most recent thread Id using .thread_id on the email
    """

    print("="*60)
    print("="*60)
    print("Agent Reply Tool Called")
    print(f"TO: {to}")
    print(f"THREAD ID: {thread_id}")
    print("="*60)
    print("="*60)

    m = EmailMessage(
        to = to,
        subject = subject,
        msg_plain = msg,
        thread_id = thread_id
    )

    return gmail.ReplyToEmail(m)

@tool
def send_the_draft_email_to_slack(original_from:str, original_subject:str, original_body:str, thread_id:str, draft_reply:str) -> str:
    """Send a drafted *reply* to Slack, attached to an email thread.

    if the email address is in a string like "Luke Hallal <luke@gmail.com>, extract the email from the surround char's for clear sanitised output

    original_from: sender of the inbound email (e.g. "luke@gmail.com")
    original_subject: subject line of the inbound email
    original_body: body text of the inbound email
    thread_id: provider thread id for that inbound email
    draft_reply: the reply you propose sending
    """

    e = EmailMessage(original_from, original_subject, original_body, thread_id)
    
    try:
        slack.send_email(e, draft_reply)

        return f"Sucessfully sent draft email {thread_id}"
    except Exception as e:
        return f"Failed to send draft email {thread_id}"

@tool
def send_email_summary_to_slack(fromWho: str, subject: str, summary: str) -> str:
    """Tool to send messages to slack, used when theres an email that needs summarising 
    but not replying to send the summary to slack.
    
    fromWho: Is the senders email
    subject: Is the subject of the email they sent
    summary: is the summary of the email you came up with

    format the summary in a professional manner, using formatting in the summary
    """

    r = f"From: {fromWho}\nSubject: {subject}\n\nSummary: {summary}"

    try:
        slack.send_message(r)

        return f"Successfully sent email summary from {fromWho}"
    except Exception as e:
        return f"Error sending email summary from {fromWho} : {e}"