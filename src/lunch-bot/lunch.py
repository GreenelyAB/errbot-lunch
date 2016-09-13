from errbot import BotPlugin, botcmd
from random import randrange
import os


class Lunch(BotPlugin):
    """Lunch Option Selector Bot """

    def __init__(self, bot):
        super().__init__(bot)
        file_dir = os.path.dirname(__file__)
        self.options_file = os.path.join(file_dir, "options")
        self.options = self._load_options()

    def _load_options(self):
        options = []
        if not os.path.isfile(self.options_file):
            raise Exception("Lunch file does not exist!")
        with open(self.options_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                options.append(line.replace("\n",""))
        return options

    def _save_options(self):
        """Save lunch options to the options file"""
        with open(self.options_file, "w") as f:
            for option in self.options:
                f.write(option + "\n")

    def _select(self):
        return self.options[randrange(0, len(self.options))]

    @botcmd
    def lunch(self, msg, args):
        """Return a random lunch option"""
        if not self.options:
            return "There are no lunch places registered."
        else:
            return self._select()

    @botcmd
    def lunch_add(self, msg, args):
        """Add a lunch option to the list."""
        if not args:
            return ("Need to pass a lunch option to remove."
                   "Example: !lunch add Thai")
        elif args.lower() in [x.lower() for x in self.options]:
            return "{} is already a lunch option".format(args)
        else:
            self.options.append(args)
            self._save_options()
            return "{} has been added as a lunch option".format(args)

    @botcmd
    def lunch_remove(self, msg, args):
        """Remove a lunch option from the list."""
        if not args:
            return ("Need to pass a lunch option to remove."
                   "Example: !lunch remove Thai")
        elif args.lower() not in [x.lower() for x in self.options]:
            return "{} is not a lunch option".format(args)
        else:
            self.options = [
                k for k in self.options if k.lower() != args.lower()]
            self._save_options()
            return "{} has been removed as a lunch option".format(args)

    @botcmd
    def lunch_list(self, msg, args):
        """List the lunch options"""
        return "Lunch Options:\n{}".format(
            "\n".join(["{}".format(k) for k in self.options]))

    @botcmd
    def lunch_empty(self, msg, args):
        """Reset lunch options to the options file"""
        self.options = []
        self._save_options()
        return "All lunch options have been deleted."
