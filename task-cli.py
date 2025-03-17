import json
import os.path
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import sys


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
    last_id: int = 0

    def to_dict(self):
        """This function is to make the tasks field serializable"""
        return {
            "version": self.version,
            "tasks": [task.__dict__ for task in self.tasks],
            "last_id": self.last_id
        }


class App:
    def __init__(self, storage_path: str, version: str, args: List[str]):
        self.storage_path = storage_path
        self.version = version
        self.args = args

    def create_storage(self):
        if os.path.isfile(self.storage_path):
            print("Storage already exists!")
            return

        storage = Storage(self.version, []).to_dict()
        str_json = json.dumps(storage)
        with open(self.storage_path, "wt") as file:
            file.write(str_json)
        print(f"Storage created successfully in {self.storage_path}")

    def get_storage(self) -> Storage:
        if not os.path.isfile(self.storage_path):
            self.create_storage()

        with open(self.storage_path, "r") as file:
            content = json.loads(file.read())

        # This iterate over the tasks in content and then all dicts in task are expanded inside tha Task object
        tasks = [Task(**task) for task in content["tasks"]]
        last_id = content.get("last_id", 0) # Get last_id or default to 0
        return Storage(version=content["version"], tasks=tasks, last_id=last_id)

    def update_storage(self, storage: Storage):
        new_storage = json.dumps(storage.to_dict())
        with open(self.storage_path, "wt") as file:
            file.write(new_storage)

    def add_task(self, description: str):
        storage = self.get_storage()

        storage.last_id += 1
        new_task = Task(
            id=storage.last_id,
            description=description,
            created_at=datetime.now().isoformat(),
        )
        storage.tasks.append(new_task)
        self.update_storage(storage)
        print(f"Task added successfully (ID: {storage.last_id})")

    def list_tasks(self):
        storage = self.get_storage()
        for task in storage.tasks:
            print(f"Task {task.id}: {task.description}, status: {task.status}, creation date: {task.created_at}, update date: {task.updated_at}")

    def list_done(self):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.status != 'done':
                continue

            print(f"Task {task.id}: {task.description}, status: {task.status}, creation date: {task.created_at}, update date: {task.updated_at}")

    def list_todo(self):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.status != 'todo':
                continue

            print(f"Task {task.id}: {task.description}, status: {task.status}, creation date: {task.created_at}, update date: {task.updated_at}")

    def list_progress(self):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.status != 'in-progress':
                continue

            print(f"Task {task.id}: {task.description}, status: {task.status}, creation date: {task.created_at}, update date: {task.updated_at}")

    def update_task(self, task_id: int, description: str):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.description = description
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)
        print(f"Task with id {task_id} updated")

    def mark_done(self, task_id: int):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.status = "done"
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)

    def mark_in_progress(self, task_id: int):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.status = "in-progress"
                task.updated_at = datetime.now().isoformat()
                break
        self.update_storage(storage)

    def delete_task(self, task_id: int):
        storage = self.get_storage()
        storage.tasks = [task for task in storage.tasks if task.id != task_id]
        self.update_storage(storage)
        print("Task deleted")

    def args_parser(self):
        arg1 = self.args[1]

        match arg1:
            case 'init':
                print("Creating storage file")
                self.create_storage()
            case 'add':
                print("Adding a task\n")
                inp = input("Task description: ")
                self.add_task(inp)
            case 'update':
                arg2 = self.args[2]
                print("Updating task\n")
                inp = input("New description: ")
                self.update_task(int(arg2), inp)
            case 'mark-done':
                arg2 = self.args[2]
                self.mark_done(int(arg2))
                print("Task marked as done")
            case 'mark-in-progress':
                arg2 = self.args[2]
                self.mark_in_progress(int(arg2))
                print("Task marked as in-progress")
            case 'delete':
                arg2 = self.args[2]
                print(f"Removing task with id {arg2}")
                self.delete_task(int(arg2))
            case 'list':
                try:
                    arg2 = self.args[2]
                    if arg2 == "done":
                        self.list_done()
                    elif arg2 == "todo":
                        self.list_todo()
                    elif arg2 == "in-progress":
                        self.list_progress()
                except:
                    self.list_tasks()
            case _:
                print("no")

    def setup(self):
        self.args_parser()


if __name__ == "__main__":
    app = App(STORAGE_PATH, VERSION, sys.argv)
    app.setup()
