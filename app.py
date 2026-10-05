from dotenv import load_dotenv

from langfuse import get_client, observe, propagate_attributes

from sql_generator.generator import generate_sql
from sql_generator.validator import validate_sql


load_dotenv()

langfuse = get_client()


@observe(name="sql_generator")
def sql_generator(question: str):
    sql = generate_sql(question)

    is_valid = validate_sql(sql)

    return {
        "sql": sql,
        "valid": is_valid,
    }


def main():
    question = input("\nEnter your question: ")

    with propagate_attributes(
        user_id="student-001",
        session_id="sql-learning-session-001",
        tags=[
            "sql-generator",
            "learning",
        ],
        metadata={
            "application": "sql-generator",
            "environment": "development",
        },
    ):
        result = sql_generator(question)

    print("\nGenerated SQL:")
    print(result["sql"])

    print("\nSQL Valid:")
    print(result["valid"])

    langfuse.flush()


if __name__ == "__main__":
    main()