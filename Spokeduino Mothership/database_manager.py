import inspect
import logging
import sqlite3
from typing import Any


def get_line_info() -> str:
    return f"{inspect.stack()[1][2]}:{inspect.stack()[1][3]}"


class DatabaseManager:
    """
    Handles all database interactions for the Spokeduino application.
    """
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def execute_select(self, query: str, params: tuple = ()) -> list[Any]:
        """
        Execute a SELECT query and return all results.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor: sqlite3.Cursor = connection.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")
            return []

    def execute_query(self, query: str, params: tuple = ()) -> int | None:
        """
        Execute an INSERT, UPDATE, or DELETE query and return the last row ID.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor: sqlite3.Cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()
                self.db_changed = True
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")
            return None

    def vacuum(self) -> None:
        """
        Optimize the database by running VACUUM.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("VACUUM;")
                logging.info("Database vacuumed successfully.")
        except sqlite3.Error as e:
            logging.error(f"DatabaseManager.vacuum error: {e}")