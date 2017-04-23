
"""

################# AMITY ROOM ALLOCATION SYSTEM #############################

Usage:
    app.py create_room (office|livingspace) <room_name>...
    app.py add_person <first_name> <last_name> (staff|fellow) [(y|n)]
    app.py get_person_identifier <first_name> <last_name> (staff|fellow)
    app.py see_person_allocations <person_identifier>
    app.py see_rooms_with_space [(offices|livingspaces)]
    app.py reallocate_person <person_identifier> <new_room_name>
    app.py load_people <file_name>
    app.py print_allocations [--o=filename]
    app.py print_unallocated [--o=filename]
    app.py print_room <room_name>
    app.py save_state [--db=sqlite_database]
    app.py load_state <sqlite_database>
    app.py see_all_people [(fellows|staff)]
    app.py see_all_rooms [(offices|livingspaces)]
    app.py remove_person <person_identifier>
    app.py (-i | --interactive)
    app.py (-h | --help | --version)

"""
import os
import sys
import cmd

from docopt import docopt, DocoptExit
from termcolor import colored, cprint
from tabulate import tabulate

from amity_app.classes.amity import Amity

function = Amity()



def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            cprint('\n Invalid Command!\n', 'red')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def start():
    os.system("clear")
    intro = "Welcome to Amity Room Allocation System"
    prompt = "Amity -->"
    cprint(__doc__, 'green')


class ToDo(cmd.Cmd):
    intro = colored("\n Welcome to the Amity Room Allocation System\n", "blue")
    prompt = colored("\n Enter a command --> ", "blue")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (staff|fellow) [(y|n)]"""

        name = arg["<first_name>"] + " " + arg["<last_name>"]

        if arg["staff"]:
            role = "STAFF"
        if arg["fellow"]:
            role = "FELLOW"

        if arg["y"]:
            accommodation = "Y"
        elif arg["n"]:
            accommodation = "N"
        else:
            accommodation = "N"

        result = function.add_person(name, role, wants_accommodation=accommodation)

        if result[1] in ["\n Use letters only for person name\n",
                        "\n Names should not exceed 80 characters",
                        "\n role must be staff or fellow",
                        "\n Staff cannot be allocated living spaces\n"]:
            color = "red"
        else:
            color = "green"

        cprint(result[1], color)

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office|livingspace) <room_name>..."""

        if arg["office"]:
            room_type = "OFFICE"
        if arg["livingspace"]:
            room_type = "LIVINGSPACE"

        room_names = arg["<room_name>"]

        result = function.create_room(room_type, room_names)

        if result[0]:
            cprint(result[0], "green")
        if result[1]:
            cprint(result[1], "red")
        if result[2]:
            cprint(result[2], "red")


    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""

        person_identifier = arg["<person_identifier>"]
        new_room_name = arg["<new_room_name>"]

        result = function.reallocate_person(person_identifier, new_room_name)

        new_room_name = new_room_name = new_room_name.upper()

        if result in ["\n Room name should consist of letters and/or digits only",
                      "\n Room name should not exceed 40 characters",
                      "\n Person identifier looks something like s-1a " + \
                      "or f-2a\nuse the <get_person_identifier> command" + \
                              " to get a valid ID",
                      "\n Person identifier does not exist in the system " + \
                      "\n use the <get_person_identifier> command to get a valid ID",
                      "\n Room " + new_room_name + " is fully occupied",
                      "\n Person is already allocated to room " + new_room_name,
                      "\n Cannot reallocate a staff member to a living space",
                      "\n Room " + new_room_name + " does not exist in the system"
                      ]:
            color = "red"
        else:
            color = "green"

        cprint(result, color)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""

        file_name = arg["<file_name>"]
        result = function.load_people(file_name)

        if result in ["\n Supply a reasonable file name",
                      "\n Supply a real file in the text_files folder",
                      "\n Source must be a txt file",
                      "\n Contents of text file are not in the correct format",
                      "\n File is empty, has no contents"
                      ]:
            color = "red"

        elif result == "\n There is no free space currently, use the create_room command to create new space":
            color = "yellow"

        else:
            color = "green"

        cprint(result, color)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""

        if arg["--o"]:
            file_name = arg["--o"]
        else:
            file_name = ""

        result = function.print_allocations(allocated_file_name=file_name)

        if result in ["\n Supply a reasonable file name",
                      "\n Destination must be a txt file"
                      ]\
                  or type(result) is str and result.startswith("FIle IOError - "):

            color = "red"

        elif result == "\n There are currently no allocations in the system":

            color = "yellow"

        else:

            color = "green"

        if type(result) is list:
            for line in result:
                cprint(line, color)
        else:
            cprint(result, color)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""

        file_name = ""
        if arg["--o"]:
            file_name = arg["--o"]

        result = function.print_unallocated(destination_file_name=file_name)

        if result in ["\n Supply a reasonable file name",
                      "\n Destination must be a txt file"
                      ]\
                  or type(result) is str and result.startswith("FIle IOError - "):

            color = "red"

        elif result == "\n There are no unallocated people in the system":

            color = "yellow"

        else:

            color = "green"

        if type(result) is list:
            for line in result:
                cprint(line, color)
        else:
            cprint(result, color)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        room = arg["<room_name>"]

        result = function.print_room(room)

        room = room.upper()

        if result in ["\n Use letters and/or digits only for room names",
                      "\n Room name should not be more than 40 characters"]:

            color = "red"

        elif result == "\n Room " + room + " does not exist in the system":

            color = "yellow"

        else:
            color = "green"

        if type(result) is list:
            for line in result:
                cprint("\n" + line, color)
        else:
            cprint(result, color)

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""

        destination = ""
        if arg["--db"]:

            destination = arg["--db"]

        result = function.save_state(destination_db=destination)

        if result in ["\n Supply a reasonable file name",
                      "\n Destination must be a db file",
                      "\n Failed to create database"
                      ] \
                or type(result) is str and result.startswith("\n An error"):

            color = "red"

        elif result == "\n There is no data in the system to save":

            color = "yellow"

        else:
            color = "green"

        cprint(result, color)

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""

        source = ""
        if arg["<sqlite_database>"]:
            source = arg["<sqlite_database>"]

        result = function.load_state(source_db=source)

        if result in ["\n Supply a reasonable file name",
                      "\n File extension must be .db"
                      ] \
                or result.startswith("\n DB access error"):

            color = "red"

        elif result == "\n File does not exist":

            color = "yellow"

        else:
            color = "green"

        cprint(result, color)

    @docopt_cmd
    def do_get_person_identifier(self, arg):
        """Usage: get_person_identifier <first_name> <last_name> (staff|fellow)"""

        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]

        if arg["staff"]:
            role = "staff"
        if arg["fellow"]:
            role = "fellow"

        result = function.get_person_identifier(first_name, last_name, role)

        if result in ["\n Use letters only for person name",
                      "\n Person name should not exceed 100 characters"
                      ]:

            color = "red"

        elif result == "\n Person does not exist in the system":

            color = "yellow"

        else:
            color = "green"

        if type(result) is list:
            for item in result:
                cprint("\n " + item, color)
        else:
            cprint(result, color)

    @docopt_cmd
    def do_see_person_allocations(self, arg):
        """Usage: see_person_status <person_identifier>"""

        person_identifier = arg["<person_identifier>"]

        result = function.see_person_allocations(person_identifier)

        if result in ["\n Person identifier looks something like s-1a or f-2a\n use the " +\
                      "<get_person_identifier> command to get a valid ID",
                      "\n Person identifier does not exist in the system " + \
                      "\n use the <get_person_identifier> command to get a valid ID"
                      ]:

            color = "red"

        else:
            color = "green"

        cprint(result, color)

    @docopt_cmd
    def do_see_rooms_with_space(self, arg):
        """Usage: see_rooms_with_space [(offices|livingspaces)]"""

        if arg["offices"]:
            argument = "offices"
        elif arg["livingspaces"]:
            argument = "livingspaces"
        else:
            argument = ""

        result = function.see_rooms_with_space(room_type=argument)

        if result == "\n There are no rooms with space":
            cprint(result, "yellow")

        elif type(result) is list and type(result[0]) is list:

            if result[0]:
                cprint("\n Living spaces with available space\n -----------------------------------------", "blue")
                for room in result[0]:
                    cprint("\n " + room, "green")

            if result[1]:
                cprint("\n Offices with available space\n -----------------------------------------", "blue")
                for room in result[1]:
                    cprint("\n " + room, "green")
        else:
            if arg["offices"]:
                cprint("\n Offices with available space\n -----------------------------------------", "blue")
                for room in result:
                    cprint("\n " + room, "green")
            if arg["livingspaces"]:
                cprint("\n Living spaces with available space\n -----------------------------------------", "blue")
                for room in result:
                    cprint("\n " + room, "green")

    @docopt_cmd
    def do_see_all_people(self, arg):
        """Usage: see_all_people [(fellows|staff)]"""

        if arg["fellows"]:
            argument = "fellows"
        elif arg["staff"]:
            argument = "staff"
        else:
            argument = ""

        result = function.see_all_people(role=argument)

        table_fellows = []
        table_staff = []

        if argument == "fellows" and result:
            for name in result:

                row = name.split()
                table_fellows.append([row[0], row[1] + " " + row[2], row[3]])

            cprint(tabulate(table_fellows, headers=["PERSON ID", "NAME", "FELLOW"], tablefmt="fancy_grid"), "green")

        elif argument == "fellows" and not result:
            cprint("\n There are no fellows in the system", "yellow")

        elif argument == "staff" and result:
            for name in result:
                row = name.split()
                table_staff.append([row[0], row[1] + " " + row[2], row[3]])

            cprint(tabulate(table_staff, headers=["PERSON ID", "NAME", "ROLE"], tablefmt="fancy_grid"), "green")

        elif argument == "staff" and not result:
            cprint("\n There are no staff in the system", "yellow")

        elif len(result) and (result[0] or result[1]):

            for name in result[0]:

                row = name.split()
                table_fellows.append([row[0], row[1] + " " + row[2], row[3]])
            cprint(tabulate(table_fellows, headers=["PERSON ID", "NAME", "ROLE"], tablefmt="fancy_grid"), "green")

            for name in result[1]:

                row = name.split()
                table_staff.append([row[0], row[1] + " " + row[2], row[3]])
            cprint(tabulate(table_staff, headers=["PERSON ID", "NAME", "ROLE"], tablefmt="fancy_grid"), "green")

        else:
            cprint("\n There are no people in the system", "yellow")

    @docopt_cmd
    def do_see_all_rooms(self, arg):
        """USage: see_all_rooms [(offices|livingspaces)]"""

        if arg["offices"]:
            argument = "offices"
        elif arg["livingspaces"]:
            argument = "livingspaces"
        else:
            argument = ""

        result = function.see_all_rooms(room_type=argument)

        tbl_offices = []
        tbl_living_spaces = []

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        if argument == "offices" and result:

            for office in result:

                row = office.split("-")
                tbl_offices.append([row[0].strip(), row[1].strip()])
            cprint(tabulate(tbl_offices, headers=["ROOM NAME", "ROOM TYPE"], tablefmt="fancy_grid"), "green")

        elif argument == "offices" and not result:
            cprint("\n There are no offices in the system", "yellow")

        elif argument == "livingspaces" and result:

            for livingspace in result:

                row = livingspace.split("-")
                tbl_living_spaces.append([row[0].strip(), row[1].strip()])
            cprint(tabulate(tbl_living_spaces, headers=["ROOM NAME", "ROOM TYPE"], tablefmt="fancy_grid"), "green")

        elif argument == "livingspaces" and not result:
            cprint("\n There are no livingspaces in the system", "yellow")

        elif len(result) and (result[0] or result[1]):

            for livingspace in result[0]:
                row = livingspace.split("-")
                tbl_living_spaces.append([row[0].strip(), row[1].strip()])
            cprint(tabulate(tbl_living_spaces, headers=["ROOM NAME", "ROOM TYPE"], tablefmt="fancy_grid"), "green")

            for office in result[1]:
                row = office.split("-")
                tbl_offices.append([row[0].strip(), row[1].strip()])
            cprint(tabulate(tbl_offices, headers=["ROOM NAME", "ROOM TYPE"], tablefmt="fancy_grid"), "green")

        else:
            cprint("\n There are no rooms in the system", "yellow")

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    @docopt_cmd
    def do_remove_person(self, arg):
        """Usage: remove_person <person_identifier>"""

        person_id = arg["<person_identifier>"]

        result = function.remove_person(person_id)

        if result == "\n Person identifier looks something like s-1a or f-2a\n use the " +\
                      "<get_person_identifier> command to get a valid ID":

            color = "red"

        elif result == "\n Person identifier does not exist in system":

            color = "yellow"

        else:

            color = "green"

        cprint(result, color)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print("\n Exiting Amity Room Allocation and destroying your current Session\n")
        exit()

opt = docopt(__doc__, sys.argv[1:])

if __name__ == "__main__":
    try:
        start()
        ToDo().cmdloop()
    except KeyboardInterrupt:
        os.system("clear")
        print('\n Application Exiting')