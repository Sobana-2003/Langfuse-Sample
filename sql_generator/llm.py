import os

from dotenv import load_dotenv
from langfuse.openai import AzureOpenAI


load_dotenv()


client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_version=os.environ["AZURE_VERSION"],
)