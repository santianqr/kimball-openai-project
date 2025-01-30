from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from creds import creds
from src.utils import db
import re


class SQLGenerator:
    """
    A utility class to generate and execute SQL queries using an AI language model.
    """

    _table_schema = {
        "dim_country": {"country_id": "bigint", "country": "text"},
        "dim_customer": {"customer_id": "bigint", "country": "text"},
        "dim_date": {
            "date_id": "bigint",
            "invoice_date": "timestamp without time zone",
            "year": "integer",
            "month": "integer",
            "day": "integer",
            "weekday": "integer",
        },
        "dim_product": {
            "product_id": "bigint",
            "stock_code": "text",
            "description": "text",
        },
        "fact_sales": {
            "invoice": "text",
            "product_id": "bigint",
            "customer_id": "bigint",
            "date_id": "bigint",
            "country_id": "bigint",
            "quantity": "bigint",
            "unit_price": "double precision",
            "total_price": "double precision",
        },
    }

    _conn_config = creds.get_openai_config()
    _openai_key = _conn_config["key"]
    _llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=_openai_key)

    @classmethod
    def _generate_template(cls) -> str:
        """
        Generates the SQL prompt template for the AI model.

        Returns:
            str: SQL query generation prompt template.
        """
        return """
        You are an expert in SQL and must generate queries for a PostgreSQL
        database based on the user's request.

        ## Database schema with data types:
        {table_schema}

        ## Instructions:
        - Use the exact table and column names.
        - If the query involves dates, use them from `dim_date` by JOINing on `date_id`.
        - If the query involves customers, use `dim_customer` by JOINing on `customer_id`.
        - If the query involves products, use `dim_product` by JOINing on `product_id`.
        - When working with `unit_price` or `total_price`, remember they are `double precision`.
        - Always group results properly and use `ORDER BY` when necessary.
        - The response must strictly be a SQL query, without additional text.

        ## User Request:
        "{user_request}"

        ## SQL Query:
        """

    @classmethod
    def _clean_sql_query(cls, response_content: str) -> str:
        """
        Cleans the generated SQL query by removing unnecessary code block delimiters.

        Args:
            response_content (str): AI model response containing the SQL query.

        Returns:
            str: Cleaned SQL query.
        """
        return re.sub(r"```(?:sql)?\n([\s\S]*?)```", r"\1", response_content).strip()

    @classmethod
    def generate_table(cls, user_request: str):
        """
        Converts a natural language request into an SQL query and executes it.

        Args:
            user_request (str): User's request in natural language.

        Returns:
            pd.DataFrame | str: Query results as a DataFrame or an error message.
        """
        try:
            prompt_template = PromptTemplate(
                input_variables=["table_schema", "user_request"],
                template=cls._generate_template(),
            )
            prompt_text = prompt_template.format(
                table_schema=cls._table_schema, user_request=user_request
            )

            response = cls._llm.invoke(prompt_text)
            cleaned_query = cls._clean_sql_query(response.content)

            return db.execute_query(cleaned_query)
        except Exception as e:
            return f"❌ Error processing request: {str(e)}"
