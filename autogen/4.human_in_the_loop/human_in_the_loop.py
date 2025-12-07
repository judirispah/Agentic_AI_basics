import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

model_client=OpenAIChatCompletionClient(model="gemini-2.5-flash",
    api_key="AIzaSyB4V4UF7nqItjx1-0pMhH58CibeCUe40V4",)


assistant = AssistantAgent(
    name="template_creator",
    description="Agent that creates clean policy skeleton templates (only main headings)",
    model_client=model_client,
    system_message=(
        "You are a policy template designer. "
        "For every request, generate ONLY the high-level skeleton of the policy. "
        "Output STRICTLY the main headings — no explanations, no details. "
        "Structure must follow standard policy document format "
        "Your output should always be:\n"
        "- Clean\n"
        "- Numbered\n"
        "- Professional\n"
        "Do not add examples, notes, sub headings or subtext unless asked."
    ),
)


user_proxy_agent = UserProxyAgent(
    name ='UserProxy',
    description='you are a user proxy agent',
    input_func=input
)

termination_condition = TextMentionTermination(text='APPROVE')


team = RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=10
)

stream = team.run_stream(task = 'generate a password management policy')

async def main():
    await Console(stream)

if (__name__ == '__main__'):
    asyncio.run(main())