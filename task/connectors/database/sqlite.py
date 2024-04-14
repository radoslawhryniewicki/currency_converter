import os

from sqlalchemy import (Column, Engine, Float, Integer, MetaData, String,
                        Table, create_engine, func, insert, select)
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError

from task.models import ConvertedPricePLN


class SQLiteConnector:
    def __init__(self, db_file=".sqlite3.db") -> None:
        self._engine = self._create_sqlalchemy_engine(db_file)
        self._meta = MetaData()

    def _create_table(self, table_name: str) -> None:
        table = Table(
            table_name,
            self._meta,
            Column("id", Integer, primary_key=True),
            Column("currency", String),
            Column("rate", Float),
            Column("price_in_pln", Float),
            Column("date", String),
        )
        table.create(self._engine, checkfirst=True)

    def _create_sqlalchemy_engine(self, db_file: str) -> Engine:
        if not os.path.exists(db_file):
            open(db_file, "a").close()
        return create_engine(f"sqlite:///{db_file}")

    def _get_table(self, table_name: str) -> Table:
        try:
            return Table(table_name, self._meta, autoload_with=self._engine)
        except NoSuchTableError:
            self._create_table(table_name)
            return self._get_table(table_name)

    def save(self, entity: ConvertedPricePLN) -> None:
        try:
            currency_conv_table = self._get_table("CurrencyConversion")
            with self._engine.connect() as conn:
                query = insert(currency_conv_table).values(**entity.model_dump())
                conn.execute(query)
                conn.commit()
        except SQLAlchemyError as e:
            print(f"Error saving data: {e}")
            raise
