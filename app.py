
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

            print('\n Invalid Command!\n')
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
    print(__doc__)


class ToDo(cmd.Cmd):
    intro = "Welcome to the Amity Room Allocation System\n"
    prompt = "\n Enter a command --> "

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
        print(result[1])

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office|livingspace) <room_name>..."""

        if arg["office"]:
            room_type = "OFFICE"
        if arg["livingspace"]:
            room_type = "LIVINGSPACE"

        room_names = arg["<room_name>"]

        result = function.create_room(room_type, room_names)
        print(result)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""

        person_identifier = arg["<person_identifier>"]
        new_room_name = arg["<new_room_name>"]

        result = function.reallocate_person(person_identifier, new_room_name)
        print(result)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""

        file_name = arg["<file_name>"]
        result = function.load_people(file_name)
        print(result)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""

        if arg["--o"]:
            file_name = arg["--o"]
        else:
            file_name = ""

        function.print_allocations(allocated_file_name=file_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""

        file_name = ""
        if arg["--o"]:
            file_name = arg["--o"]

        function.print_unallocated(destination_file_name=file_name)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        room = arg["<room_name>"]

        function.print_room(room)

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""

        destination = ""
        if arg["--db"]:

            destination = arg["--db"]

        print(function.save_state(destination_db=destination))

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""

        source = ""
        if arg["<sqlite_database>"]:
            source = arg["<sqlite_database>"]

        print(function.load_state(source_db=source))

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

        if type(result) is list:
            for item in result:
                print("\n " + item)
        else:
            print(result)

    @docopt_cmd
    def do_see_person_allocations(self, arg):
        """Usage: see_person_status <person_identifier>"""

        person_identifier = arg["<person_identifier>"]

        print(function.see_person_allocations(person_identifier))

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
            print(result)

        elif type(result) is list and type(result[0]) is list:

            if result[0]:
                print("\n Living spaces with available space\n -----------------------------------------")
                for room in result[0]:
                    print("\n ", room)

            if result[1]:
                print("\n Offices with available space\n -----------------------------------------")
                for room in result[1]:
                    print("\n ", room)
        else:
            if arg["offices"]:
                print("\n Offices with available space\n -----------------------------------------")
                for room in result:
                    print("\n ", room)
            if arg["livingspaces"]:
                print("\n Living spaces with available space\n -----------------------------------------")
                for room in result:
                    print("\n ", room)

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

        if argument == "fellows" and result:
            for name in result:
                print(name)

        elif argument == "fellows" and not result:
            print("\n There are no fellows in the system")

        elif argument == "staff" and result:
            for name in result:
                print(name)

        elif argument == "staff" and not result:
            print("\n There are no staff in the system")

        elif len(result) and (result[0] or result[1]):
            for name in result[0]:
                print(name)
            for name in result[1]:
                print(name)

        else:
            print("\n There are no people in the system")









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