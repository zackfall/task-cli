import json
import os.path
from typing import List


class Task:
    def __init__(
        self, id: int, description: str, status: str, createdAt: str, updatedAt: str
    ):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_dict(self):
        return self.__dict__


class Storage:
    def __init__(self, version: str, tasks: List[Task]):
        self.version = version
        self.tasks = tasks

    def to_dict(self):
        return {
            "version": self.version,
            "tasks": [task.to_dict() for task in self.tasks],
        }


def create_storage(path: str, version: str):
    if os.path.isfile(path):
        print("[Warning]: The storage.json file already exists")
        return
    storage = Storage(version, []).to_dict()
    str_json = json.dumps(storage)
    with open(path, "wt") as file:
        file.write(str_json)


if __name__ == "__main__":
    create_storage("./storage.json", "0.0.1")
