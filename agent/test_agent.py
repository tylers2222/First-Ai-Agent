import unittest
import os
import time

# Change to Email Agent directory where gmail_token.json is located BEFORE importing agent
# Get the directory where this script is located, then go up one level to Email Agent/
script_dir = os.path.dirname(os.path.abspath(__file__))  # agent/ directory
email_agent_dir = os.path.dirname(script_dir)  # Email Agent/ directory
os.chdir(email_agent_dir)

from agent import run_agent

def main():
    start = time.perf_counter()
    print("Starting Agent Call To Check Email")
    print("-"*60)

    # result = run_agent("Check my emails and let me know how may are unread")
    # result = run_agent("Check my emails and mark the 4th email as read and tell me which one it is")
    # result = run_agent("Can you give me a list of the categories my last 5 emails falls under")
    result = run_agent("Can you classify my emails in a list of categories, if its a branded email in regard to the classification tool call mark it as read, if its an email from luke.hallal@gmail.com and its a personal email. Please respond to him an email answering the question")
    if not result:
        print("Failed LLM call")

    print(result)
    end = time.perf_counter()
    print(f"Time Elapsed: {(end - start):.1f}")

if __name__ == '__main__':
    main()