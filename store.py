import pathlib
import sqlite3
import json

from fetcher import HouseStore, House


_schema = """
CREATE TABLE IF NOT EXISTS houses(
    id INTEGER PRIMARY KEY,
    raw TEXT NOT NULL
);
"""


class LiteHouseStore(HouseStore):
    __conn: sqlite3.Connection

    def __init__(self, path: str):
        self.__conn = sqlite3.connect(path)
        self.__ensure_table()

    def __ensure_table(self) -> None:
        with self.__conn as conn:
            conn.execute(_schema)

    def __setitem__(self, key: int, value: House):
        with self.__conn as conn:
            conn.execute(
                "INSERT OR REPLACE INTO houses (id, raw) VALUES (?, ?)",
                (key, json.dumps(House.to_json(value)),),
            )

    def __getitem__(self, key: int):
        with self.__conn as conn:
            cursor = conn.execute("SELECT raw FROM houses WHERE id = ?", (key,))

            results = cursor.fetchall()
            if len(results) == 0:
                raise KeyError("house not exists")
            if len(results) != 1:
                raise RuntimeError("database corrupted")

            raw_data = results[0][0]
            return House.from_json(json.loads(raw_data))

    def __delitem__(self, key: int):
        with self.__conn as conn:
            cursor = conn.execute("DELETE FROM houses WHERE id = ?", (key,))
            if cursor.rowcount != 1:
                raise KeyError("house not exists")

    def __len__(self):
        with self.__conn as conn:
            cursor = conn.execute("SELECT COUNT(id) FROM houses")
            result = cursor.fetchone()
            return result[0]

    def __iter__(self):
        with self.__conn as conn:
            cursor = conn.execute("SELECT id from houses")

            while True:
                row = cursor.fetchone()
                if row is None:
                    return
                yield row[0]
