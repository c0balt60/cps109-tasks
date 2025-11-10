'''
    Author: Andrii Naumenko
    Description: CPS109 Project
    Date: 2025-10-23
'''
# pylint: disable=C0301:line-too-long
# pyright: ignore[reportPossiblyUnboundVariable]

from datetime import date, timedelta
from enum import Enum
import functools
from typing import Any, Callable

TODAY = date.today()
TOMORROW = date.today() + timedelta(days=1)

LOGIN_FILE = "logins.txt"
DATA_FILE_PREFIX = "data-"

SECTIONS = [
    "Budget",
    "Categories",
    "Goals",
]

DEFAULT_DATA = [
    "---Budget",
    "",
    "---Categories",
    "",
    "---Goals",
    ""
]

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

def error_boundary(fallback: Any = State.FAIL, err_msg: str = "Error caught") -> Callable[..., Any]:
    '''
    A decorator to catch errors for functions critical to the main loop.
    Catches the exception and returns the fallback value.

    :param fallback: Fallback value if the function errors.
    :type fallback: Any
    :param err_msg: Error message for the given function
    :type err_msg: String
    '''

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            try:
                return func(*args, **kwargs)
            except Exception as e: # pylint: disable=W0718:broad-exception-caught
                print(f"{color("[Exception]", "RED")} -> {color(func.__name__, "BLUE")}: {err_msg} >> Exception: {e}")
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
            column_widths[i] = max(column_widths[i], len(item))

    # Create separator line
    separator = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"

    # Format headers
    header_line = "|" + "|".join([f" {header:<{column_widths[i]}} " for i, header in enumerate(headers)]) + "|"

    # Format data rows
    data_lines: list[str] = []
    for row in data:
        row_line = "|" + "|".join([f" {item:<{column_widths[i]}} " for i, item in enumerate(row)]) + "|"
        data_lines.append(row_line)

    # Combine all parts
    table_output = [separator, header_line, separator] + data_lines + [separator]
    return "\n".join(table_output)

# print(
#     create_table(
#         ["Name", "Address"],
#         [
#             ["Alex", "150 Road"],
#             ["Max", "500 Street"]
#         ]
#     )
# )

class BudgetItem:
    '''
    Abstracted each specific budget item for more fine control
    '''

    def __init__(self, date_val: date | str, budget_type: str, category: str, amount: str) -> None:
        self.date = date_val if isinstance(date_val, date) else date.fromisoformat(date_val)
        self.type = budget_type
        self.category = category
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.date},{self.type},{self.category},{self.amount}"

class User:
    '''
    User abstraction for handling specific-user related actions (when logged in)
    '''

    def __init__(self, username: str, password: str) -> None:
        self.login = username+","+password
        self.username = username
        self.password = password
        self.items: list[BudgetItem] = []
        self.categories: list[str] = []
        self.goals: list[str] = []
        self.load_data()

    def __del__(self):
        print(color("Logging out...", "GREEN"))
        self.save_data()

    #@error_boundary(err_msg="Failed to load data for client.")
    def load_data(self):
        '''
        Read saved data from the txt file and load it in
        '''
        with open(DATA_FILE_PREFIX + self.username + ".txt", 'r', encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines()]

        # username = lines[0].split(":")[1]
        # password = lines[1].split(":")[1]

        # Get indexes
        budget_index = lines.index("---Budget") + 1
        category_index = lines.index("---Categories") + 1
        goal_index = lines.index("---Goals") + 1

        # Gather Budget section
        # print(budget_index, category_index)
        for line in lines[budget_index:category_index-1]:
            # print(line)

            if line.strip():
                # print(line)
                date_str, budget_type, category, amount = line.split(",", 3)
                self.items.append(
                    BudgetItem(date_str, budget_type, category, amount)
                )

        for line in lines[category_index:goal_index-1]:
            self.categories.append(line)

        # Gather Goals
        for line in lines[goal_index:]:
            self.goals.append(line)


        # print("Class dict:", self.__dict__)

    def save_data(self):
        '''
        Write saved class data to txt file for re-use.
        '''
        with open(DATA_FILE_PREFIX + self.username + ".txt", 'w', encoding="utf-8") as file:
            file.write(self.login + "\n")

            self.categories = list(filter(None, self.categories))
            self.goals = list(filter(None, self.goals))

            # Write Budget
            file.write("---Budget\n")
            for item in self.items:
                file.write(f"{str(item)}\n")

            # Write categories
            file.write("---Categories\n")
            for cat in self.categories:
                file.write(f"{cat}\n")

            # Write goals
            file.write("---Goals\n")
            for goal in self.goals:
                file.write(f"{goal}\n")

    #@error_boundary(err_msg="Failed to execute client command.")
    def command(self, cmd: str):
        '''
        Method to process individual clients' commands

        :param cmd: Command to process
        :type cmd: String
        '''
        action = None
        modifiers = None

        if cmd.find('"') != -1:
            str_before = cmd[:cmd.find('"')].split(" ")[:-1]
            #print(str_before)
            action = str_before[0]
            modifiers = str_before[1:] + [cmd[cmd.find('"'):].strip('"')]
        else:
            action, *modifiers = cmd.split(" ")


        # If no modifiers, display command help
        if len(modifiers) < 1:
            getattr(self, f"_{action}")(["-h"])
            return
        # print(action, modifiers)
        match action:
            case "budget":
                self._budget(modifiers)
            case "goal":
                self._goal(modifiers)
            case "category":
                self._category(modifiers)
            case _:
                pass

    def _budget(self, modifiers: list[str]):
        #to_int = int(modifiers[1])
        flag = modifiers[0]
        match flag:
            case "add":
                print(color(">", "BLUE"), f"added {flag}: {modifiers[1]}")
                self.items.append(
                    BudgetItem(
                        TODAY,
                        modifiers[1],
                        modifiers[2],
                        modifiers[3]
                    )
                )
            case "show":
                print([str(item) for item in self.items])
            case _:
                pass



    def _goal(self, modifiers: list[str]):
        flag = modifiers[0]
        match flag:
            case "list" | "-l":
                print(color("> Goals", "BLUE"))
                print(self.goals)
            case "help" | "-h":
                print(color("\n~ Goal Help ~\n", "CYAN"))
            case _:
                pass

    def _category(self, modifiers: list[str]):
        flag = modifiers[0]
        match flag:
            case "add" | "-a":
                if modifiers[1]:
                    if modifiers[1].find("-") != -1:
                        print(color("Only strings can be added to categries not flags. ", "RED"))
                        return

                    if modifiers[1] in self.categories:
                        return
                    self.categories.append(modifiers[1])
                print(self.categories)
            case "list" | "-l":
                print(color("> Categories", "BLUE"))
                print(self.categories)
            case "help" | "-h":
                print(color("\n~ Category Help ~\n", "CYAN"))
                print("\tcategory add 'name'\t--> Creates new category")
                print("\tcategory list [-l]\t|> Lists all current categories")
                print("\tcategory help [-h]\t|> Shows this message\n")
            case _:
                pass

@error_boundary(err_msg="Failed to login.")
def try_login(username: str, password: str) -> State:
    '''
    Tries logging into your "account"

    :param username: Client username
    :type username: String
    :param password: Client password
    :type password: String
    :returns: Login successful state
    '''

    # Try loging in
    with open(LOGIN_FILE, 'r', encoding="utf-8") as file:
        for login in file:
            usr, pswrd = login.strip().split(",")
            if username == usr and password == str(pswrd):
                return State.SUCCESS

    return State.FAIL

@error_boundary(err_msg="Failed to create new login.")
def new_login(username: str, password: str) -> State:
    '''
    Tries to create new login for user

    :param username: Client username
    :type username: String
    :param password: Client password
    :type password: String
    :returns: State for creation of new login
    '''

    # Check for old login
    old_login = try_login(username, password)
    if old_login == State.SUCCESS:
        return State.FAIL

    # Create login
    with open(LOGIN_FILE, 'a', encoding="utf-8") as logins:
        logins.write(f"{username},{password}\n")
        return State.SUCCESS

    return State.FAIL

def show_help() -> None:
    '''
    Show the help command
    '''
    print(f'''
        {color("~ Commands ~","BLUE")}
    login -> "l" "login"
    new login -> "n" "new-login"
    help (this menu) -> "h" "help"

        {color("~ Account (must be logged in) ~","BLUE")}
    logout -> "out" "x" "logout"
    add (expense | income) -> Adds float to specified section
    set (budget | expenses | income) -> Overwrite specified section
        ''')

@error_boundary(err_msg="Failed to create new database")
def new_data(username: str, password: str) -> State:
    '''
    Creates new data for a new login
    '''

    # TODO: Add try_login boundrary first to check for duplicates

    try:
        with open(DATA_FILE_PREFIX + username + ".txt", 'x', encoding="utf-8"):
            print("New file created.")
        print("Created new file for user.")
    except FileExistsError:
        print("File already exists.")
        return State.SUCCESS


    # Set password
    with open(DATA_FILE_PREFIX + username + ".txt", 'a', encoding="utf-8") as data:
        data.write(f"{username},{password}\n")
        data.writelines([default + "\n" for default in DEFAULT_DATA])

        return State.SUCCESS

    return State.FAIL

def main() -> None:
    '''Main entry'''
    in_loop = True
    login_info = None
    users: dict[str, User] = {}

    while in_loop:
        # Gather CLI input
        user_input = input(f"\nFinancer cli{color(" @"+login_info, "BLUE") if login_info else ""}: ")

        # Logged in user
        if login_info and users[login_info]:
            user = users[login_info]
            # Handle logout
            if user_input in ["x", "logout", "out"]:
                del user
                users.pop(login_info)
                login_info = None
                continue

            user.command(user_input) # type: ignore

            continue

        # Use input
        match user_input:
            # Login
            case "l" | "login":
                print("\n\t~ Login ~")

                if login_info:
                    print(f"Already logged in as: {login_info}")

                usrnm = input("Enter username: ")
                pswrd = input("Enter password: ")

                if try_login(usrnm, pswrd) == State.SUCCESS:
                    login_info = usrnm
                    # Create new user
                    users[login_info] = User(usrnm,pswrd)
                else:
                    print(color("Unable to find login information. ", "RED"))

            case "n" | "new-login":
                print("\n\t~ New Login ~")
                usrnm = input("Enter username: ")
                pswrd = input("Enter password: ")
                new = new_login(usrnm, pswrd)
                if new == State.SUCCESS:
                    print("Created new account!")
                    new_data(usrnm, pswrd)
                else:
                    print("Failed to create new account.")

            case "h" | "help":
                show_help()
            case "exit":
                break
            case _:
                pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\nKeyboard interrupt exit...", "RED"))
    finally:
        print(color("\nExiting Financer...", "GREEN"))
