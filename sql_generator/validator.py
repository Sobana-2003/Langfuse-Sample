import re

from langfuse import observe


FORBIDDEN_SQL = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
]


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    # Remove Markdown SQL code fences.
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()


@observe()
def validate_sql(sql: str) -> bool:
    cleaned_sql = clean_sql(sql)

    normalized_sql = re.sub(
        r"\s+",
        " ",
        cleaned_sql.upper(),
    )

    for keyword in FORBIDDEN_SQL:
        if re.search(rf"\b{keyword}\b", normalized_sql):
            return False

    return normalized_sql.startswith("SELECT")