import asyncio
from autogen_agentchat.agents import AssistantAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

import os
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv

from autogen_ext.tools.http import HttpTool

model_client=OpenAIChatCompletionClient(model="gemini-1.5-flash-8b",
    api_key="AIzaSyDGmZl1entDw2bVC37o7cP1HOna24vX8wA",)

'''
{
  "fact": "Cats with long, lean bodies are more likely to be outgoing, and more protective and vocal than those with a stocky build.",
  "length": 121
}
'''

schema = {
        "type": "object",
        "properties": {
            "fact": {
                "type": "string",
                "description": "A random cat fact"
            },
            "length": {
                "type": "integer",
                "description": "Length of the cat fact"
            }
        },
        "required": ["fact", "length"],
    }


http_tool = HttpTool(
    name="cat_facts_api",
    description="get a cool cat fact",
    scheme="https",
    host="catfact.ninja",
    port=443,
    path="/fact",
    method="GET",
    return_type="json",
    json_schema= schema
)

agent = AssistantAgent(
    name="CatFactsAgent",
    model_client=model_client,
    system_message='You are a helpful assistant that can provide cat facts using the cat_facts_api tool. Give the result with summary',
    tools=[http_tool],
    reflect_on_tool_use=True
)



async def main(): 
    result = await agent.run(task = 'Give me a random cat fact')

    print(result.messages)

if (__name__ == "__main__"):
    asyncio.run(main())