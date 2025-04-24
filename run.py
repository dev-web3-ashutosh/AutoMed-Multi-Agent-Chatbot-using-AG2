from autogen import ConversableAgent, GroupChat, GroupChatManager
from openai import OpenAI
import logging

# Suppress warnings from autogen.oai.client
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)


# Initialize OpenAI Client (API Key is automatically managed from environment variables or configured in OpenAI settings)
client = OpenAI()

# Disable Docker execution to prevent runtime errors
code_execution_config = {"use_docker": False}