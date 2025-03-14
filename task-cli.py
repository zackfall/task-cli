import json
import os.path
from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


STORAGE_PATH = "./storage.json"
VERSION = "0.0.1"


@dataclass
class Task:
    id: int | None = None
    description: str | None = None
    status: str = "todo"
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


class App:
    def __init__(self, storage_path: str, version: str):
        self.storage_path = storage_path
        self.version = version

    def create_storage(self):
        if os.path.isfile(self.storage_path):
            return

        storage = Storage(self.version, []).to_dict()
        str_json = json.dumps(storage)
        with open(self.storage_path, "wt") as file:
            file.write(str_json)
        print(f"Storage created succesfully in {self.storage_path}")

    def get_storage(self) -> Storage:
        if not os.path.isfile(self.storage_path):
            self.create_storage()
        with open(self.storage_path, "r") as file:
            content = json.loads(file.read())
        # This iterate over the tasks in content and then all dicts in task are expanded inside tha Task object
        tasks = [Task(**task) for task in content["tasks"]]
        return Storage(version=content["version"], tasks=tasks)

    def update_storage(self, storage: Storage):
        new_storage = json.dumps(storage.to_dict())
        with open(self.storage_path, "wt") as file:
            file.write(new_storage)

    def add_task(self, description: str):
        storage = self.get_storage()
        new_task = Task(
            id=len(storage.tasks) + 1,
            description=description,
            created_at=datetime.now().isoformat(),
        )
        storage.tasks.append(new_task)
        self.update_storage(storage)

    def list_tasks(self):
        storage = self.get_storage()
        for task in storage.tasks:
            print(f"Task {task.id}: {task.description}")

    def update_task(self, task_id: int, description: str):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.description = description
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)

    def check_task(self, task_id: int):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.status = "done"
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)

    def mark_as_progress(self, task_id: int):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.status = "progress"
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)

    def delete_task(self, task_id: int):
        storage = self.get_storage()
        storage.tasks = [task for task in storage.tasks if task.id != task_id]
        self.update_storage(storage)


def setup():
    parser = ArgumentParser(
        prog="Task CLI", description="A task manager in the CLI, easy to use."
    )
    parser.add_argument("add", nargs="*", help="Add a Task")
    parser.add_argument("update", nargs="*", help="Update a Task")
    parser.add_argument("remove", nargs="*", help="Remove a Task")
    parser.add_argument("mark-done", nargs="*", help="Mark a Task as done")
    parser.add_argument("mark-progress", nargs="*", help="Mark a Task as in progress")
    parser.add_argument("list", nargs="*", help="List all tasks")
    parser.add_argument("list-done", nargs="*", help="List all tasks that are done")
    parser.add_argument("list-progress", nargs="*", help="List all tasks that are in progress")
    parser.add_argument("list-todo", nargs="*", help="List all tasks that aren't done")
    args = parser.parse_args()
    print(args.add)
    # app = App(STORAGE_PATH, VERSION)


if __name__ == "__main__":
    setup()
