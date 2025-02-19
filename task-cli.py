import json
import logging
import os.path
from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


def setup_daily_logger():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    current_time = datetime.now().strftime("%m_%d_%y_%I_%M_%p")
    log_file = os.path.join(log_dir, f"{current_time}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
        filemode="w",
        encoding="utf-8",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s"
    )  # Added line number
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)

    return logging.getLogger(__name__)


logger = setup_daily_logger()

STORAGE_PATH = "./storage.json"
VERSION = "0.0.1"
HELP_MESSAGE = """
Usage:
    task-cli.py init
    task-cli.py add <description>
    task-cli.py list
    task-cli.py update <id> <description>
    task-cli.py check <id>
    task-cli.py progress <id>
    task-cli.py uncheck <id>
    task-cli.py delete <id>
"""


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
            logger.error("The storage.json file already exists")
            return

        storage = Storage(self.version, []).to_dict()
        str_json = json.dumps(storage)
        with open(self.storage_path, "wt") as file:
            file.write(str_json)

    def get_storage(self) -> Storage:
        if not os.path.isfile(self.storage_path):
            logger.info("Storage file does not exist. Creating a new one...")
            self.create_storage()

        with open(self.storage_path, "r") as file:
            content = json.loads(file.read())
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

    def uncheck_undone(self, task_id: int):
        storage = self.get_storage()
        for task in storage.tasks:
            if task.id == task_id:
                task.status = "todo"
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
    parser.add_argument("init")
    parser.add_argument("add")
    args = parser.parse_args()
    print(args.init)
    # app = App(STORAGE_PATH, VERSION)


if __name__ == "__main__":
    setup()
