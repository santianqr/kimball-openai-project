from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from creds import creds
from src.utils import db
import re

class generator:
    # Esquema de la base de datos como variable de clase
    table_schema = {
        "dim_country": {
            "country_id": "bigint",
            "country": "text"
        },
        "dim_customer": {
            "customer_id": "bigint",
            "country": "text"
        },
        "dim_date": {
            "date_id": "bigint",
            "invoice_date": "timestamp without time zone",
            "year": "integer",
            "month": "integer",
            "day": "integer",
            "weekday": "integer"
        },
        "dim_product": {
            "product_id": "bigint",
            "stock_code": "text",
            "description": "text"
        },
        "fact_sales": {
            "invoice": "text",
            "product_id": "bigint",
            "customer_id": "bigint",
            "date_id": "bigint",
            "country_id": "bigint",
            "quantity": "bigint",
            "unit_price": "double precision",
            "total_price": "double precision"
        }
    }

    # Clave de API de OpenAI como variable de clase
    conn_config = creds.openai_config()
    openai_key = conn_config["key"]

    # Inicialización del modelo de lenguaje como variable de clase
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_key)

    @classmethod
    def _generate_template(cls):
        """
        Genera la plantilla de prompt para el modelo de lenguaje.

        :return: Cadena de texto con la plantilla del prompt.
        """
        return """
        Eres un experto en SQL y debes generar consultas para una base de datos PostgreSQL según la solicitud del usuario.

        ## Estructura de la base de datos con tipos de datos:
        {table_schema}

        ## Instrucciones:
        - Usa los nombres exactos de las tablas y columnas.
        - Si la consulta requiere fechas, úsalas desde `dim_date` con `JOIN` en `date_id`.
        - Si la consulta involucra clientes, úsalos desde `dim_customer` con `JOIN` en `customer_id`.
        - Si la consulta involucra productos, úsalos desde `dim_product` con `JOIN` en `product_id`.
        - Cuando trabajes con `unit_price` o `total_price`, recuerda que son `double precision` (números flotantes de alta precisión).
        - Siempre agrupa correctamente y usa `ORDER BY` si es necesario.
        - La respuesta debe ser exclusivamente la consulta SQL, sin palabras adicionales.

        ## Solicitud del usuario:
        "{user_request}"

        ## Consulta SQL:
        """

    @classmethod
    def _clean_sql_query(cls, response_content):
        """
        Elimina los delimitadores de bloque de código de la respuesta del modelo.

        :param response_content: Respuesta del modelo de lenguaje.
        :return: Cadena de texto con la consulta SQL limpia.
        """
        cleaned_query = re.sub(r"```(?:sql)?\n([\s\S]*?)```", r"\1", response_content).strip()
        return cleaned_query

    @classmethod
    def generate_table(cls, user_request):
        """
        Convierte una solicitud en lenguaje natural a una consulta SQL y la ejecuta.

        :param user_request: Cadena de texto con la solicitud del usuario.
        :return: DataFrame con los resultados de la consulta o una cadena de error.
        """
        try:
            # Formatear el prompt con la solicitud del usuario
            prompt_template = PromptTemplate(
                input_variables=["table_schema", "user_request"],
                template=cls._generate_template()
            )
            prompt_text = prompt_template.format(
                table_schema=cls.table_schema,
                user_request=user_request
            )

            # Obtener la respuesta del modelo de lenguaje
            response = cls.llm.invoke(prompt_text)

            # Limpiar la consulta SQL generada
            cleaned_query = cls._clean_sql_query(response.content)

            # Ejecutar la consulta en la base de datos
            df = db.execute_query(cleaned_query)

            return df

        except Exception as e:
            return f"Error al procesar la solicitud: {str(e)}"

