import os
import json
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.environ["APP_DB_HOST"],
        port=os.environ["APP_DB_PORT"],
        dbname=os.environ["APP_DB_NAME"],
        user=os.environ["APP_DB_USER"],
        password=os.environ["APP_DB_PASSWORD"],
    )


def save_execution_log(
    *,org_id, org_user_id,agent_id,project_id,
    question_id,
    session_id,
    session_question_id,
    trace_id,
    step_name,
    step_type,
    status,
    question,
    prompt,
    response,
    model_name,
    input_tokens,
    output_tokens,
    total_tokens,
    duration,
    metadata,
    started_at,
    completed_at,
):
    sql = """
        INSERT INTO dhimath_metadata.llm_execution_logs (
            org_id,
            org_user_id,
            agent_id,
            project_id,
            question_id,
            session_id,
            session_question_id,
            trace_id,
            step_name,
            step_type,
            status,
            question,
            prompt,
            response,
            model_name,
            input_tokens,
            output_tokens,
            total_tokens,
            duration,
            metadata,
            started_at,
            completed_at
        )
        VALUES (
            %(org_id)s,
            %(org_user_id)s,
            %(agent_id)s,
            %(project_id)s,
            %(question_id)s,
            %(session_id)s,
            %(session_question_id)s,
            %(trace_id)s,
            %(step_name)s,
            %(step_type)s,
            %(status)s,
            %(question)s,
            %(prompt)s,
            %(response)s,
            %(model_name)s,
            %(input_tokens)s,
            %(output_tokens)s,
            %(total_tokens)s,
            %(duration)s,
            %(metadata)s,
            %(started_at)s,
            %(completed_at)s
        )
    """

    params = {
        "org_id": org_id,
        "org_user_id": org_user_id,
        "project_id": project_id,
        "agent_id": agent_id,
        "question_id": question_id,
        "session_id": session_id,
        "session_question_id": session_question_id,
        "trace_id": trace_id,
        "step_name": step_name,
        "step_type": step_type,
        "status": status,
        "question": question,
        "prompt": prompt,
        "response": response,
        "model_name": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "duration": duration,
        "metadata": json.dumps(metadata) if metadata else None,
        "started_at": started_at,
        "completed_at": completed_at,
    }

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

        connection.commit()