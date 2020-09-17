"""
pyt

Usage:
  pyt hello
  pyt gid  <file> [--append] [--pattern=PATTERN] [--output=OUTFILE]
  pyt -h | --help
  pyt --version
  pyt cms [--port=PORT] [--server=SERVER] --tests=SELECTED_TESTS
  pyt cms m [--port=PORT] [--server=SERVER] --tests=SELECTED_TESTS
  pyt cms2 --tests=SELECTED_TESTS

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -s, --server SERVER               App server [default: localhost]
  -p, --port PORT                   Port for app server [default: 3000]
  -t, --tests SELECTED_TESTS        Select test suites or test cases to run. Defaults to run all test.
  -o, --output OUTFILE              Output file for result.
  --pattern PATTERN                        Regular expression to find test ids [default: ^(\w+\.)+(\w+)?$].
  --append                          Update test ids but not changing existing ids.
  m                                 set CMS_MOCK to true

Examples:
  pyt hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tzmgit/pyt-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
