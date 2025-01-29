from src.utils import db

class loader:

    @staticmethod
    def upload_model(dim_product, dim_customer, dim_date, dim_country, fact_sales):
        """
        Carga los cinco DataFrames en la base de datos PostgreSQL.

        :param db: Objeto de conexión a la base de datos que contiene el método upsert_table().
        :param dim_product: DataFrame de la dimensión de productos.
        :param dim_customer: DataFrame de la dimensión de clientes.
        :param dim_date: DataFrame de la dimensión de fechas.
        :param dim_country: DataFrame de la dimensión de países.
        :param fact_sales: DataFrame de la tabla de hechos (ventas).
        :return: Mensaje indicando si la carga fue exitosa.
        """
        try:
            db.upsert_table(dim_product, "dim_product")
            db.upsert_table(dim_customer, "dim_customer")
            db.upsert_table(dim_date, "dim_date")
            db.upsert_table(dim_country, "dim_country")

            # Subir la tabla de hechos después (porque depende de las dimensiones)
            db.upsert_table(fact_sales, "fact_sales")

            return "✅ Carga exitosa: Todas las tablas han sido subidas a PostgreSQL."

        except Exception as e:
            return f"❌ Error al cargar los datos a PostgreSQL: {str(e)}"
