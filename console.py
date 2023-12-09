#!/usr/bin/python3
"""console module
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """console class for HBNB; AirBnb clone
    """
    available_dictionary = {"BaseModel": BaseModel, "User": User}
    available_dictionary["State"] = State
    available_dictionary["City"] = City
    available_dictionary["Amenity"] = Amenity
    available_dictionary["Place"] = Place
    available_dictionary["Review"] = Review
    available_names = ['BaseModel', 'User']
    available_names.append('State')
    available_names.append('City')
    available_names.append('Amenity')
    available_names.append('Place')
    available_names.append('Review')
    prompt = "(hbnb)"

    def do_quit(self, line):
        """implements the quit command
        """
        return True

    def do_EOF(self, line):
        """implements EOF input
        """
        print()
        return True

    def emptyline(self):
        """implements empty line as command
        """
        pass

    def do_create(self, line):
        """creates a new instance, saves to json file then prints it's id
        """
        if not line:
            print("** class name missing **")
        elif line not in self.available_names:
            print("** class doesn't exist **")
        else:
            class_ = self.available_dictionary[line]
            dummy = class_()
            dummy.save()
            print(dummy.id)

    def do_show(self, line):
        """ Prints the string representation of an instance
        based on the class name and id
        """
        if not line:
            print("** class name missing **")
        else:
            # classname, id_value = line.split(" ")
            parts = line.split()
            classname = parts[0]
            if classname not in self.available_names:
                print("** class doesn't exist **")
            elif len(parts) < 2:
                print("** instance id missing **")
            else:
                id_value = parts[1]
                obj_dictionary = storage.all()
                name_and_id = classname + "." + id_value
                if name_and_id not in obj_dictionary.keys():
                    print("** no instance found **")
                else:
                    actual_object = obj_dictionary[name_and_id]
                    print(actual_object)

    def do_destroy(self, line):
        """Deletes an instance based on the class name
        and id and saves the changes into the JSON file
        """
        if not line:
            print("** class name missing **")
        else:
            parts = line.split()
            classname = parts[0]
            if classname not in self.available_names:
                print("** class doesn't exist **")
            elif len(parts) < 2:
                print("** instance id missing **")
            else:
                id_value = parts[1]
                obj_dictionary = storage.all()
                name_and_id = classname + "." + id_value
                if name_and_id not in obj_dictionary.keys():
                    print("** no instance found **")
                else:
                    obj_dictionary.pop(name_and_id)
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all
        """
        if line and line not in self.available_names:
            print("** class doesn't exist **")
        else:
            obj_dictionary = storage.all()
            new_dictionary = {}
            if line:
                for key, value in obj_dictionary.items():
                    if key.startswith(line):
                        new_dictionary[key] = value
            else:
                for key, value in obj_dictionary.items():
                    new_dictionary[key] = value
            # next we iterate new_dictionary.values() calling __str__ on it
            ls = []
            for value in new_dictionary.values():
                ls.append(value.__str__())
            if len(ls) < 1:
                pass
            else:
                print(ls)

    def do_update(self, line):
        """Updates an instance based on the class name and id
        by adding/updating attribute and saves the change into the JSON file
        """
        parts = line.split()
        # if not line:
        if len(parts) == 0:
            """ (ex: $ update)
            """
            print("** class name missing **")
        elif len(parts) > 0:
            _name = parts[0]
            if _name not in self.available_names:
                """ (ex: $ update MyModel)
                """
                print("** class doesn't exist **")
            elif len(parts) == 1:
                """ (ex: $ update BaseModel)
                """
                print("** instance id missing **")
            elif len(parts) == 2:
                """ (ex: $ update BaseModel 121212)
                """
                _name = parts[0]
                _id = parts[1]
                unique_id = _name + "." + _id
                obj_dictionary = storage.all()
                if unique_id not in obj_dictionary.keys():
                    print("** no instance found **")
            elif len(parts) == 3:
                """(ex: $ update BaseModel existing-id)
                """
                print("** attribute name missing **")
            else:
                _name = parts[0]
                _id = parts[1]
                _key = parts[2]
                _value = parts[3]
                unique_id = _name + "." + _id
                obj_dictionary = storage.all()
                if _value.isdigit():
                    _value = int(_value)
                else:
                    check = _value.split(".")
                    if check[0].isdigit() and check[1].isdigit():
                        _value = float(_value)
                unique_object = obj_dictionary[unique_id]
                setattr(unique_object, _key, _value)
                unique_object.save()

    def default(self, line):
        """called when no argument matches the above
        """
        part = line.split('.')
        classname = part[0]
        if len(part) > 1:
            command = part[1]
            if command.startswith("all"):
                HBNBCommand.do_all(self, classname)
            elif command.startswith("count"):
                val = 0
                obj_dictionary = storage.all()
                for key in obj_dictionary.keys():
                    if key.startswith(classname):
                        val += 1
                print(val)
            elif command.startswith("show"):
                arg1 = classname
                id_ = command.strip('show')
                id_ = id_.strip('()')
                actual_line = arg1 + " " + id_
                HBNBCommand.do_show(self, actual_line)
            elif command.startswith("destroy"):
                arg1 = classname
                id_ = command.strip("destroy")
                id_ = id_.strip("()")
                actual_line = arg1 + " " + id_
                HBNBCommand.do_destroy(self, actual_line)
            elif command.startswith("update"):
                line1 = classname
                parts = command.split(',')
                id_attr = ''
                name_attr = ''
                val_attr = ''
                if len(parts) == 3:
                    id_attr = parts[0]
                    """id_attr = id_attr.strip('update')
                    id_attr = id_attr.strip('()')"""
                    id_attr = id_attr.strip('update(')
                    name_attr = parts[1]
                    val_attr = parts[2]
                    val_attr = val_attr.strip(")")
                actual_line = line1 + " " + id_attr + " " + name_attr + " " + val_attr
                HBNBCommand.do_update(self, actual_line)
            else:
                self.stdout.write('*** Unknown syntax: {}\n'.format(line))
        else:
            self.stdout.write('*** Unknown syntax: {}\n'.format(line))


if __name__ == "__main__":
    HBNBCommand().cmdloop()