
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive room allocation application.
Usage:
    app.py create_room (office|living_space) <room_name>...
    app.py add_person <first_name> <last_name> (staff|fellow) [<wants_accommodation>]
    app.py get_person_identifier <first_name> <last_name> (staff|fellow)
    app.py see_person_allocations <person_identifier>
    app.py see_rooms_with_space [offices|living_spaces]
    app.py reallocate_person <person_identifier> <new_room_name>
    app.py load_people <file_name>
    app.py print_allocations [--o=filename]
    app.py print_unallocated [--o=filename]
    app.py print_room <room_name>
    app.py save_state [--db=sqlite_database]
    app.py load_state <sqlite_database>
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

            print('Invalid Command!')
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
        """Usage: add_person <first_name> <last_name> <role> [<wants_accommodation>]"""

        name = arg["<first_name>"] + " " + arg["<last_name>"]
        role = arg["<role>"].upper()
        accommodation = arg["<wants_accommodation>"].upper() if arg["<wants_accommodation>"] else "N"

        result = function.add_person(name, role, wants_accommodation=accommodation)
        print(result[1])

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        room_type = arg["<room_type>"].upper()
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

        print(arg)

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
        """Usage: get_person_identifier <first_name> <last_name> <role>"""

        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        role = arg["<role>"]

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






    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print("\nExiting Amity Room Allocation and destroying you current Session\n")
        exit()

opt = docopt(__doc__, sys.argv[1:])

if __name__ == "__main__":
    try:
        start()
        ToDo().cmdloop()
    except KeyboardInterrupt:
        os.system("clear")
        print('Application Exiting')