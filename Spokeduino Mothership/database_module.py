import inspect
import logging
import os
import sqlite3
from typing import Any


class DatabaseModule:
    """
    Handles all database interactions for the Spokeduino application.
    """
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_line_info(self) -> str:
        return f"{inspect.stack()[1][2]}:{inspect.stack()[1][3]}"

    def initialize_database(self, schema_file: str, data_file: str) -> None:
        """
        Check for database existence and integrity, and recreate if necessary.
        :param schema_file: Path to the SQL schema initialization file.
        :param data_file: Path to the SQL default data initialization file.
        """
        if not os.path.exists(self.db_path):
            logging.warning(f"Database file not found at {self.db_path}. "
                            f"Creating a new one.")
            self.recreate_database(schema_file, data_file)
        else:
            # Check database integrity
            if not self.check_integrity():
                logging.error("Database integrity check failed. "
                              "Recreating database.")
                self.recreate_database(schema_file, data_file)

    def check_integrity(self) -> bool:
        """
        Check the database integrity using PRAGMA integrity_check.
        :return: True if the database is valid, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                result = connection.execute(
                    "PRAGMA integrity_check;"
                    ).fetchone()
                return result and result[0] == "ok"
        except sqlite3.Error as e:
            logging.error(f"Failed to perform integrity check: {e}")
            return False

    def recreate_database(self, schema_file: str, data_file: str) -> None:
        """
        Recreate the database by executing
        the schema and default data SQL scripts.
        :param schema_file: Path to the SQL schema file.
        :param data_file: Path to the SQL data file.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()

                # Load schema
                with open(schema_file, "r") as f:
                    cursor.executescript(f.read())
                logging.info("Database schema applied successfully.")

                # Load default data
                with open(data_file, "r") as f:
                    cursor.executescript(f.read())
                logging.info("Default data applied successfully.")

                connection.commit()
        except (sqlite3.Error, IOError) as e:
            logging.error(f"Failed to recreate the database: {e}")

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
            logging.error(f"{self._get_line_info()}: " \
                          f"SQL error: {e}\nQuery: {query}")
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
            logging.error(f"{self._get_line_info()}: " \
                          f"SQL error: {e}\nQuery: {query}")
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