import json
import os.path
from dataclasses import dataclass, field
from typing import List

STORAGE_PATH = "./storage.json"
VERSION = "0.0.1"


@dataclass
class Task:
    id: int | None = None
    description: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


@dataclass
class Storage:
    version: str | None = None
    # dataclasses can't have mutable values
    tasks: List[Task] = field(default_factory=list)

    def to_dict(self):
        """This function is to make the tasks field serializable"""
        return {
            "version": self.version,
            "tasks": [task.__dict__ for task in self.tasks],
        }


def create_storage():
    if os.path.isfile(STORAGE_PATH):
        print("[Warning]: The storage.json file already exists")
        return
    storage = Storage(VERSION, []).to_dict()
    str_json = json.dumps(storage)
    with open(STORAGE_PATH, "wt") as file:
        file.write(str_json)


def get_storage() -> Storage:
    with open(STORAGE_PATH, "r") as file:
        content = json.loads(file.read())
    tasks = [Task(**task) for task in content["tasks"]]
    return Storage(version=content["version"], tasks=tasks)


def update_storage(storage: Storage):
    json_storage = json.dumps(storage.to_dict())
    with open(STORAGE_PATH, "wt") as file:
        file.write(json_storage)


def add_task(task: Task):
    storage = get_storage()
    storage.tasks.append(task)
    update_storage(storage)


if __name__ == "__main__":
    storage = get_storage()
    print(storage)
    task = Task(2, "pepe", "done", "hoy", "hoy")
    add_task(task)
    storage = get_storage()
    print(storage)
