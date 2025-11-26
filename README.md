<<<<<<< HEAD
# First-Ai-Agent
=======
# AI Agent - Email Director

An intelligent email management system built with LangChain and ChatGPT that automates reading, classifying, and responding to emails in your personal Gmail inbox. The agent integrates with Slack for human-in-the-loop approval of drafted responses.

## Overview

This project demonstrates a production-ready AI agent that:
- Monitors your Gmail inbox for unread emails
- Classifies emails into categories (Personal, Branded, Informational, Transactional)
- Drafts responses for emails requiring replies
- Sends drafts to Slack for approval before sending
- Automatically marks processed emails as read

## Architecture

### Core Components

- **LangChain Agent**: Orchestrates email processing using tool-calling agents
- **Gmail Client**: Handles Gmail API interactions (reading, sending, replying)
- **Slack Integration**: Manages Slack notifications and approval workflows
- **Workflow Orchestrator**: Coordinates the end-to-end email processing pipeline

### How It Works

1. **Email Processing** (`main.py` → `workflow.py`)
   - Fetches unread emails from Gmail
   - Agent classifies each email
   - For personal emails needing response: drafts a reply and sends to Slack
   - For informational emails: sends summary to Slack
   - Marks all processed emails as read

2. **Slack Approval** (`server.py`)
   - Receives draft emails via Slack Bolt app (Socket Mode)
   - Displays email details with Approve/Reject buttons
   - On approval: sends the email reply via Gmail API
   - Uses Slack's built-in Bolt framework instead of traditional webhooks

3. **Agent Tools** (`agent/tools.py`)
   - `get_unread_emails`: Fetches unread emails from Gmail
   - `classify_email_into_category`: Uses LLM to categorize emails
   - `mark_single_email_as_read`: Marks emails as read
   - `send_the_draft_email_to_slack`: Sends draft to Slack for approval
   - `send_email_summary_to_slack`: Sends email summary to Slack
   - `reply_to_an_email`: Sends email replies (after approval)
   - `send_email`: Sends new emails

## Tech Stack

### Agent Library
- **LangChain**: Agent framework and tool orchestration
- **LangChain Classic**: Tool-calling agent implementation

### LLM
- **ChatGPT (OpenAI)**: GPT-4o-mini for email classification and response drafting

### Integrations
- **Gmail API**: Email reading, sending, and management via `simplegmail`
- **Slack API**: Notifications and approval workflow via `slack-bolt`

## Project Structure

```
Email Agent/
├── agent/
│   ├── agent.py              # LangChain agent setup and execution
│   ├── tools.py              # Agent tools (email operations)
│   └── test_agent.py         # Agent testing
├── gmail/
│   ├── gmail_client.py       # Gmail API wrapper
│   └── test_gmail.py         # Gmail client testing
├── slack_intergration/
│   ├── slack_client.py       # Slack API wrapper
│   └── slack_test.py         # Slack client testing
├── utils/
│   └── match_email.py        # Email parsing utilities
├── webhooks/
│   └── slack_webhooks.py     # Webhook handlers
├── main.py                   # Entry point - runs email processing
├── server.py                 # Slack Bolt server for approvals
├── workflow.py               # Email processing orchestration
└── client_secret.json        # Gmail OAuth credentials
```

## Setup

### Prerequisites

- Python 3.12+
- Gmail account with API access
- Slack workspace with app created
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   cd "Email Agent"
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Gmail OAuth**
   - Place `client_secret.json` in the root directory
   - Run authentication: `python3 test_auth.py`
   - Follow OAuth flow to generate `gmail_token.json`

5. **Configure environment variables**
   Create a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SLACK_TOKEN=xoxb-your-slack-bot-token
   SLACK_APP_TOKEN=xapp-your-slack-app-token
   EMAIL_CHANNEL=your-slack-channel-id
   ```

## Usage

### Running the Email Agent

**Process emails:**
```bash
python3 main.py
```

This will:
- Fetch unread emails (default: 20)
- Classify each email
- Draft responses for personal emails
- Send drafts to Slack for approval
- Mark emails as read

**Start Slack approval server:**
```bash
python3 server.py
```

This runs the Slack Bolt app in Socket Mode to:
- Receive draft email notifications
- Handle Approve/Reject button clicks
- Send approved emails via Gmail API

### Workflow

1. **Email Processing** (`main.py`)
   - Agent processes unread emails
   - Classifies and drafts responses
   - Sends to Slack for human review

2. **Slack Approval** (`server.py`)
   - User reviews draft in Slack
   - Clicks "Approve & Send" or "Reject"
   - Approved emails are sent automatically

## Features

- ✅ **Intelligent Email Classification**: Categorizes emails into Personal, Branded, Informational, Transactional
- ✅ **Automated Draft Generation**: Uses GPT-4 to draft contextual email responses
- ✅ **Human-in-the-Loop Approval**: Slack integration for reviewing drafts before sending
- ✅ **Thread-Aware Replies**: Maintains email thread context when replying
- ✅ **Email Management**: Automatically marks processed emails as read
- ✅ **Error Handling**: Robust error handling and logging throughout

## Design Decisions

### Why Slack Bolt Instead of FastAPI?

Opting against a traditional FastAPI server for receiving Slack webhooks, Slack offers a built-in Bolt app to receive results of things like button pushes. This provides:

- **Simpler Architecture**: No need to manage webhook endpoints
- **Socket Mode**: Real-time bidirectional communication
- **Built-in Security**: Handles authentication and verification automatically
- **Easier Development**: Less boilerplate, more focus on business logic

## Testing

```bash
# Test Gmail client
python3 gmail/test_gmail.py

# Test Slack client
python3 slack_intergration/slack_test.py

# Test agent
python3 agent/test_agent.py
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `SLACK_TOKEN` | Slack bot token (xoxb-...) | Yes |
| `SLACK_APP_TOKEN` | Slack app-level token (xapp-...) | Yes |
| `EMAIL_CHANNEL` | Slack channel ID for notifications | Yes |

## Future Enhancements

- [ ] Support for multiple email accounts
- [ ] Email scheduling functionality
- [ ] Advanced filtering rules
- [ ] Analytics and reporting
- [ ] Multi-language support
- [ ] Custom classification categories

## License

Private project - All rights reserved

## Author

Tyler Stewart - First attempt at building an AI agent using LangChain and ChatGPT

>>>>>>> 251fc0d (Initial commit: AI Email Agent with LangChain and ChatGPT)
