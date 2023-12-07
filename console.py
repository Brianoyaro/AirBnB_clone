#!/usr/bin/python3
"""console module
"""
import cmd
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it, and prints the id"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in ['BaseModel']:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = args[0] + '.' + args[1]
        if key not in objects:
            print("** no instance found **")
            return
        print(objects[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in ['BaseModel']:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = args[0] + '.' + args[1]
        if key not in objects:
            print("** no instance found **")
            return
        del objects[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        objects = storage.all()
        if not arg:
            print([str(obj) for obj in objects.values()])
            return
        try:
            arg_class = eval(arg)
            if arg_class.__name__ not in ['BaseModel']:
                print("** class doesn't exist **")
                return
            print([str(obj) for key, obj in objects.items() if key.split('.')[0] == arg_class.__name__])
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in ['BaseModel']:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = args[0] + '.' + args[1]
        if key not in objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_name = args[3]
        try:
            value = eval(args[4])
        except (NameError, SyntaxError):
            value = args[4]
        setattr(objects[key], attribute_name, value)
        storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
