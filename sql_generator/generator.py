import os

from langfuse import observe, propagate_attributes
from langfuse.openai import AzureOpenAI

from .prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_version=os.environ["AZURE_VERSION"],
)


@observe()
def generate_sql(question: str) -> str:

    response = client.chat.completions.create(
        name="sql-generation",
        model=os.environ["AZURE_DEPLOYMENT_NAME"],
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return response.choices[0].message.content