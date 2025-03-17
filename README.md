# Task CLI

### How to use the program

First you have to create the storage file
```bash
python task-cli.py init
```
Then you can start working with the program. To add a task do the following:
```bash
python task-cli.py add
```
It will input you to enter the description for the task.

You can list the task with the following:
```bash
python task-cli.py list
```
You can also combine the list command with **3 subcommand** more, the `todo`, `done` and `in-progress` subcommands.
```bash
python task-cli.py list {todo, done, in-progress}
```
Now you can update tasks with the following:
```bash
python task-cli.py update 1 # change it with the id of the task you want to update
```
Then it will ask you for the new description for the task.

You can also delete a task that you don't need anymore:
```bash
python task-cli.py delete 1 # change it with the id of the task you want to delete
```
You can also mark the tasks as done or as in progress with the following commands:
```bash
python task-cli.py mark-{done, in-progress}
```
