import os
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Engine as SQLAlchemyEngine
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError

from task.connectors.database.sqlite import SQLiteConnector


@pytest.fixture
def db_file():
    file_path = "test.sqlite3.db"

    yield str(file_path)

    if os.path.exists(file_path):
        os.remove(file_path)


class TestSQLiteConnector:
    def test_create_sqlalchemy_engine(self, db_file):
        connector = SQLiteConnector(db_file)
        engine = connector._create_sqlalchemy_engine(db_file)
        assert isinstance(engine, SQLAlchemyEngine)
        assert os.path.exists(db_file)

    def test_create_table(self, db_file):
        connector = SQLiteConnector(db_file)
        connector._create_sqlalchemy_engine = MagicMock(
            return_value=create_engine(f"sqlite:///{db_file}")
        )
        connector._create_table("CurrencyConversion")
        metadata = MetaData()
        metadata.reflect(bind=connector._engine)
        assert "CurrencyConversion" in metadata.tables

    def test_get_table_existing(self, db_file):
        connector = SQLiteConnector(db_file)
        connector._create_sqlalchemy_engine = MagicMock(
            return_value=create_engine(f"sqlite:///{db_file}")
        )
        connector._create_table("CurrencyConversion")
        table = connector._get_table("CurrencyConversion")
        assert isinstance(table, Table)

    def test_get_table_not_existing(self, db_file):
        connector = SQLiteConnector(db_file)
        connector._create_sqlalchemy_engine = MagicMock(
            return_value=create_engine(f"sqlite:///{db_file}")
        )
        with patch("sqlalchemy.Table") as mock_table:
            mock_table.side_effect = NoSuchTableError
            table = connector._get_table("CurrencyConversion")
        assert isinstance(table, Table)
