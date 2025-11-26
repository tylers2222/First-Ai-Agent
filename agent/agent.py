from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from .tools import get_unread_emails, mark_single_email_as_read, classify_email_into_category, send_email, reply_to_an_email, send_the_draft_email_to_slack, send_email_summary_to_slack
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini"
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer support email assistant.
Your job is to help manage emails by:
- Classifying emails
- Checking unread emails
- Marking emails as read after processing
- Being helpful and professional
- Responding to emails

Always explain what you're doing."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


tools = [get_unread_emails, mark_single_email_as_read, classify_email_into_category, send_email, reply_to_an_email, send_the_draft_email_to_slack, send_email_summary_to_slack]
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)


def run_agent(user_prompt: str):
    result = agent_executor.invoke({"input": user_prompt})
    return result
