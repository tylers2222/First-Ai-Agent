from agent.agent import run_agent
from datetime import datetime

def process_new_emails(limit=20):
    """
    Orchestration layer on processing emails
    """

    print(f"Started processing emails with agent at {datetime.now}")
    print("="*60)

    prompt = """
Check my emails (limit=20)

Steps to take on each email
1) Get the emails data, (id, sender, subject, msg, thread_id) every email will contain this
2) Classify the email using the classify tool

if the email is category 1. "Personal Needing Response", such as a question, create a draft back and send the draft email to slack using the send email to slack tool
if you draft an email put correct spacing and formatting that a reply email usually has. It doesnt all sit in one line.

if the email is category 2. "Personal Not Needing A Response", such as thank yous or invites without responses wanted, send a summary to slack

3) Mark every email as read
    """
    try:
        agent_response = run_agent(prompt)
        print(f"Agents Response: \n{agent_response}")

    except Exception as e:
        print(f"Agent invoke failed: {e}")
