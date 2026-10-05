import os
import time
from datetime import datetime, timezone

from langfuse import observe, get_client
from langfuse.openai import AzureOpenAI

from .prompts import SYSTEM_PROMPT
from .database import save_execution_log


client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_version=os.environ["AZURE_VERSION"],
)


langfuse = get_client()


@observe(name="generate_sql")
def generate_sql(
    question: str,
    question_id=None,
    session_id=None,
    session_question_id=None,
) -> str:

    started_at = datetime.now(timezone.utc)
    start_time = time.perf_counter()

    response = None
    sql = None

    try:
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

        sql = response.choices[0].message.content

        duration = int(
            (time.perf_counter() - start_time) * 1000
        )

        trace_id = langfuse.get_current_trace_id()

        usage = response.usage

        input_tokens = (
            usage.prompt_tokens
            if usage
            else None
        )

        output_tokens = (
            usage.completion_tokens
            if usage
            else None
        )

        total_tokens = (
            usage.total_tokens
            if usage
            else None
        )

        completed_at = datetime.now(timezone.utc)

        save_execution_log(
            org_id= 1,
            org_user_id = 1,
            agent_id = 101,
            project_id= 102,
            question_id=question_id,
            session_id=session_id,
            session_question_id=session_question_id,
            trace_id=trace_id,
            step_name="generate_sql",
            step_type="GENERATION",
            status="SUCCESS",
            question=question,
            prompt=SYSTEM_PROMPT,
            response=sql,
            model_name=os.environ["AZURE_DEPLOYMENT_NAME"],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            duration=duration,
            metadata={
                "source": "sql-generator",
                "environment": "development",
            },
            started_at=started_at,
            completed_at=completed_at,
        )

        return sql

    except Exception:
        duration = int(
            (time.perf_counter() - start_time) * 1000
        )

        completed_at = datetime.now(timezone.utc)

        trace_id = langfuse.get_current_trace_id()

        save_execution_log(
            org_id= 1,
                        org_user_id = 1,
                        agent_id = 101,
                        project_id= 102,
            question_id=question_id,
            session_id=session_id,
            session_question_id=session_question_id,
            trace_id=trace_id,
            step_name="generate_sql",
            step_type="GENERATION",
            status="FAILED",
            question=question,
            prompt=SYSTEM_PROMPT,
            response=None,
            model_name=os.environ["AZURE_DEPLOYMENT_NAME"],
            input_tokens=None,
            output_tokens=None,
            total_tokens=None,
            duration=duration,
            metadata={
                "source": "sql-generator",
                "environment": "development",
            },
            started_at=started_at,
            completed_at=completed_at,
        )

        raise


# import os

# from langfuse import observe, propagate_attributes
# from langfuse.openai import AzureOpenAI

# from .prompts import SYSTEM_PROMPT
# from dotenv import load_dotenv
# load_dotenv()

# client = AzureOpenAI(
#     api_key=os.environ["AZURE_API_KEY"],
#     azure_endpoint=os.environ["AZURE_ENDPOINT"],
#     api_version=os.environ["AZURE_VERSION"],
# )


# @observe()
# def generate_sql(question: str) -> str:

#     response = client.chat.completions.create(
#         name="sql-generation",
#         model=os.environ["AZURE_DEPLOYMENT_NAME"],
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": SYSTEM_PROMPT,
#             },
#             {
#                 "role": "user",
#                 "content": question,
#             },
#         ],
#     )

#     return response.choices[0].message.content