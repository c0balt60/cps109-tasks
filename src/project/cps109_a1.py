'''
    Author: Andrii Naumenko
    Description: CPS109 Project simplified
    Date: 2025-11-14
'''
# pylint: disable=broad-except, line-too-long, missing-function-docstring, consider-iterating-dictionary

import argparse
from datetime import timedelta, date as Date
from enum import Enum
import functools
import shlex
import sqlite3
from typing import Any, Callable
from types import SimpleNamespace

# File Defs
DATA_FILE = "todo-database.db"

# Dates
TODAY = Date.today()
TOMORROW = TODAY + timedelta(days=1)

class State(Enum):
    '''
    Enum for general states
    '''
    FAIL = 0
    SUCCESS = 1

class Colors:
    '''
    Terminal colors for asthetics
    '''
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

def color(text: str, shade: str) -> str:
    '''
    Utility for coloring a string.
    '''
    return f"{getattr(Colors, shade)}{text}{Colors.RESET}"

# CLI Message Defs
PROG_NAME = "TO-DO"
WELCOME_MSG = f"{color(PROG_NAME, "YELLOW")} CLI"
WELCOME_SUB = f"A {color("short", "BLUE")} and {color("concise", "CYAN")} task tracker. "

# Util Functions
def error_boundary(fallback: Any = State.FAIL, err_msg: str="Error caught") -> Callable[..., Any]:
    '''
    A decorator to catch errors for functions critical to the main loop.
    Catches the exception and returns the fallback value.

    :param fallback: Fallback value if the function errors.
    :type fallback: Any
    :param err_msg: Error message for the given function
    :type err_msg: String
    '''

    # Capture decorated function and hook the error handler to it
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(
                    f"{color("[Exception]", "RED")} -> {color(func.__name__, "BLUE")}: {err_msg} >> Exception: {e}"
                    )
                return fallback
        return wrapper
    return decorator

def create_table(headers: list[str], data: list[list[str]]) -> str:
    '''
    Create a table using minimal elements for data output.

    :param headers: List of headers for the table
    :type headers: list[str]
    :param data: List of lists of strings containing the data
    :type data: list[list[str]]
    :returns: Formatted table string
    '''

    # Calculate maximum width for each column
    column_widths = [len(header) for header in headers]
    for row in data:
        for i, item in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(item)))

    # Create separator line
    separator = "+" + "+".join(
        ["-" * (width + 2) for width in column_widths]
        ) + "+"

    # Format data using f-string literals and
    #  aligning to the left ':<'

    # Format headers
    header_line = "|" + "|".join(
        [f" {header:<{column_widths[i]}} " for i, header in enumerate(headers)]
        ) + "|"

    # Format data rows
    data_lines: list[str] = []
    for row in data:
        row_line = "|" + "|".join(
            [f" {str(item):<{column_widths[i]}} " for i, item in enumerate(row)]
            ) + "|"
        data_lines.append(row_line)

    # Combine all parts
    table_output = [separator, header_line, separator] + data_lines + [separator]
    return "\n".join(table_output)

def parser_cmds() -> argparse.ArgumentParser:
    '''
    Setup cli commands and return the parser

    :returns ArgumentParser: Parser loaded with all the commands
    '''

    parser = argparse.ArgumentParser(description=f"{PROG_NAME} CLI")
    sub = parser.add_subparsers(dest="command")

    # Add Command
    add_cmd = sub.add_parser("add", help="Insert new to-do item into your list. ")
    add_cmd.add_argument("name")
    add_cmd.add_argument(
        "-d",
        "--description",
        required=False,
        help="short description of the task"
    )
    add_cmd.add_argument(
        "-p",
        "--priority",
        type=int,
        default=3,
        help="priority of task. (1) = Highest"
    )
    add_cmd.add_argument("--due", default=None, help="due date of the task")
    add_cmd.add_argument("-v", "--verbose", action="store_true", help="print modified task list. ")

    # Del Command
    del_cmd = sub.add_parser("del", help="Delete an existing to-do item. ")
    del_cmd.add_argument("id", help="ID for to-do to be deleted. ")
    del_cmd.add_argument(
        "-m",
        "--multiple",
        action="store_true",
        help="accept multiple deletion id's. must be separated by comma"
    )
    del_cmd.add_argument("-v", "--verbose", action="store_true", help="print modified task list. ")

    # List Command
    list_cmd = sub.add_parser("list", help="List to-do tasks. ")
    list_cmd.add_argument(
        "-s",
        "--sort",
        choices=["priority", "due", "created", "completed"],
        help="list by type. "
    )

    # Edit Command
    edt_cmd = sub.add_parser("task", help="Edit an existing tasks. ")
    edt_cmd.add_argument("id", help="ID for to-do to be edited. ")
    edt_cmd.add_argument(
        "-c",
        "--completed",
        action="store_true",
        help="set task comepletion. "
    )
    edt_cmd.add_argument(
        "-d",
        "--due",
        help="change due date of task. "
    )
    edt_cmd.add_argument(
        "-p",
        "--priority",
        type=int,
        help="change priority of task. "
    )
    edt_cmd.add_argument("-v", "--verbose", action="store_true", help="display edited task list. ")

    # Exit Command
    sub.add_parser("exit", help="Exit the CLI. ")

    return parser

# Classes
class User:
    '''
    User abstraction for handling specific-user related actions
    '''

    def __init__(self) -> None:
        self.conn = sqlite3.connect(DATA_FILE)
        # Create default sort namespace for nested command call to 'list'
        self._default_sort = SimpleNamespace(command="list", sort=None, completed=None)
        self.load()

    def __del__(self) -> None:
        self.conn.close()

    def load(self) -> None:
        '''
        Load database for user
        '''

        # Create and/or load table from database
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 3,
                due TEXT,
                created TEXT,
                completed INTEGER DEFAULT 0
            );
        """)
        self.conn.commit()
        cursor.close()

    @error_boundary(err_msg="Failed to execute command. ")
    def command(self, args: argparse.Namespace | Any) -> None:
        '''
        Execute the command for given args

        :param args: Arguments from the command
        :type args: Namespace
        '''

        cursor = self.conn.cursor()

        match(args.command):
            case "add":
                cursor.execute("""
                        INSERT INTO tasks (title, description, priority, due, created)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                    tuple(args.__dict__.values())[1:-1] + (TODAY.isoformat(),)
                )
                print(
                    f"> {color("Created task:", "BLUE")} '{args.name}'"
                )

            case "list":
                # Process no items
                size = cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
                if size < 1:
                    print(
                        f"> {color("No items saved. ", "YELLOW")}\n> {color("Type -h for help, use 'add -h' to create new task", "YELLOW")}"
                    )
                    return

                # Process sort without args
                if not args.sort:
                    cursor.execute("SELECT * FROM tasks")

                # Sort by specific
                if args.sort:
                    cursor.execute(f"SELECT * FROM tasks ORDER BY {args.sort} {args.sort=="completed" and "DESC" or "ASC"}")

                rows = cursor.fetchall()
                tbl = create_table(
                    ["ID", "Task", "Description", "Priority", "Due", "Created", "Completed"],
                    [
                        list(row) for row in rows
                    ]
                )
                print(
                    f"> {color("List of TO-DO's", "BLUE")}"
                )
                print(tbl)

            case "task":
                # Fetch current data in row
                row = cursor.execute(
                    f"SELECT * FROM tasks WHERE id = {args.id}"
                ).fetchone()

                values_map = dict(zip(
                    [desc[0] for desc in cursor.description],
                    row
                ))

                # Updates to apply
                updates: dict[str, str] = {}

                # Compare old and new tasks
                for name, new_val in args.__dict__.items():
                    if new_val is not None and name in values_map:
                        updates[name] = new_val

                # Update changed tasks
                cursor.execute(
                    f"UPDATE tasks SET {", ".join(item + " = ?" for item in updates.keys())} WHERE id = ?",
                    tuple(updates.values()) + (args.id,)
                )
                print(
                    f"> {color("Updated to-do ", "YELLOW")}"
                )

            case "del":
                cursor.execute(
                    f"DELETE FROM tasks WHERE id IN ({','.join('?' * len(args.id.strip(",")))})",
                    (args.id)
                )
                print(
                    f"> {color("Deleted to-do(s) ", "RED")}"
                )

            case _:
                pass

        # Commit database changes and close cursor after every command
        self.conn.commit()
        cursor.close()

        # Print changes if command is verbose
        # Not exactly the intended use of the word
        if hasattr(args, "verbose") and args.verbose:
            self.command(
                self._default_sort
            )

# Main Entry
def main() -> None:
    '''
    Main loop for the CLI
    '''
    in_cli = True
    user = User()
    parser = parser_cmds()

    # Output welcome message with todays' date
    print("\n" + f"{WELCOME_MSG}{"":>{4}}<{TODAY.isoformat()}>")
    print(WELCOME_SUB)

    while in_cli:
        # Get user input
        usr_input = input("\n> ")

        # Ignore blank input
        if not usr_input.strip():
            continue

        # Convert string to list using shell syntax
        arg_to_parse = shlex.split(usr_input)

        # Catch parser error
        try:
            args = parser.parse_args(arg_to_parse)
        except SystemExit:
            continue

        # Exit CLI
        if args.command == "exit":
            in_cli = False
            break

        user.command(args)

    # Delete user session on exit
    del user

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print(color("\n> Keyboard interrupt exit...", "RED"))
    finally:
        print(color(f"> Exiting {PROG_NAME}...", "GREEN"))
