import json

from task.config import JSON_DATABASE_NAME
from task.models import ConvertedPricePLN


class JSONFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            return json.load(file)

    def _save_data(self) -> None:
        with open(JSON_DATABASE_NAME, "w") as file:
            json.dump(self._data, file, indent=2)

    def _get_next_id(self) -> str:
        """
        NOTE: I assumed that in my application won't be any technincal issues while
        appending a row to a database with ID which were currently use in a past.
        Thus, first check missing ID values and then append a new data with missing ID.
        """
        ids = sorted(map(int, self._data.keys()))
        missing_ids = [
            str(i) for i in range(ids[0], ids[-1] + 1) if str(i) not in self._data
        ]
        return missing_ids[0] if missing_ids else str(ids[-1] + 1)

    def save(self, entity: ConvertedPricePLN) -> None:
        id_to_save = self._get_next_id()
        entity_to_save = {"id": int(id_to_save), **entity.model_dump()}
        self._data.update({id_to_save: entity_to_save})
        self._save_data()