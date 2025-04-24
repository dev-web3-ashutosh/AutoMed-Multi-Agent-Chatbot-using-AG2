import os
# import google.generativeai as genai
from autogen import ConversableAgent, GroupChat, GroupChatManager
from google import genai
from google.genai.types import HttpOptions
import logging

# Suppress warnings from autogen.oai.client
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)


# Initialize OpenAI Client (API Key is automatically managed from environment variables or configured in OpenAI settings)
# client = OpenAI()
client = genai.Client('GOOGLE_API_KEY')

os.environ['GOOGLE_API_KEY'] = "AIzaSyCL5xbg5VYQIL77No6isVF7PZE5uqZHtjo"
# genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# model = genai.GenerativeModel('gemini-pro')

# Disable Docker execution to prevent runtime errors
code_execution_config = {"use_docker": False}

# Sample LLM Configuration (Replace with actual API keys/config if needed)
llm_config = {"config_list": [{"model": "gemini-2.0-flash", "api_key": os.environ['GOOGLE_API_KEY']}]}  # Replace with real API key


# Step 1: Create AI Agents with Defined Roles
patient_agent = ConversableAgent(
    name="patient",
    system_message="You describe symptoms and ask for medical help.",
    llm_config=llm_config
)

diagnosis_agent = ConversableAgent(
    name="diagnosis",
    system_message="You analyze symptoms and provide a possible diagnosis. Summarize key points in one response.",
    llm_config=llm_config
)

pharmacy_agent = ConversableAgent(
    name="pharmacy",
    system_message="You recommend medications based on diagnosis. Only respond once.",
    llm_config=llm_config
)

consultation_agent = ConversableAgent(
    name="consultation",
    system_message="You determine if a doctor's visit is required. Provide a final summary with clear next steps. IMPORTANT: End your response with 'CONSULTATION_COMPLETE' to signal the end of the conversation.",
    llm_config=llm_config
)

# Step 2: Create GroupChat for Structured Interaction
groupchat = GroupChat(
    agents=[diagnosis_agent, pharmacy_agent, consultation_agent],  # Patient only initiates
    messages=[],
    max_round=5,  # Limits conversation to 5 rounds
    speaker_selection_method="round_robin"  # Ensures structured conversation flow
)

# Step 3: Create GroupChatManager to Handle Conversation
manager = GroupChatManager(name="manager", groupchat=groupchat)

# Step 4: Get Patient Input and Start Consultation
print("\n🤖 Welcome to the AI Healthcare Consultation System!")
symptoms = input("🩺 Please describe your symptoms: ")

print("\n🩺 Diagnosing symptoms...")
response = patient_agent.initiate_chat(
    manager,
    message=f"I am feeling {symptoms}. Can you help?",
)

