#!/usr/bin/env python3

import logging
import argparse
import os
import textwrap
import subprocess


### Global variables ###
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

parser = argparse.ArgumentParser(
    description=textwrap.dedent("""\
        --------------------------------
        None of these arguments's absolutely required. 
        You can put this script in your root Git directory, and it should do its job.
        --------------------------------
        """),
    prog='./pull.py',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('-i', '--interactive', dest='interactive', default=False,
                    nargs='?', const=True, help='Interactively passing arguments.')
parser.add_argument('-c', '--command', metavar='', default='git pull',
                    help='Command to execute in within repositories.')
parser.add_argument('-d', '--directory', metavar='',
                    default=f'{os.getcwd()}', help='Root directory to recursively pull.')
parser.add_argument('-e', '--exclude', metavar='', default=list(),
                    nargs='*', help='Name of repositories to NOT pullling.')
### End global variables ###


if __name__ == '__main__':

    args = parser.parse_args()

    if args.interactive:
        logging.info('Interactive mode enabled.')
        command = input(
            'Enter command to execute (default: git pull): ') or 'git pull'
        directories = [str(folder) for folder in input(
            'Enter root directory(ies) for execution (default: current): ')] or f'{os.getcwd()}'
        exclude = [str(folder) for folder in input(
            'Enter repostories to exclude from this script (default: none): ')] or None
    else:
        command = args.command
        directories = args.directory
        exclude = args.exclude

    for directory in list(directories.split()):
        for root, dirs, files in os.walk(directory, topdown=True):

            if '.git' in dirs and root.split('/')[-1] not in exclude:
                logging.info(f"Working on {root}")
                process = subprocess.Popen(list(command.split()), stdout=subprocess.PIPE)
                output = process.communicate()[0]
                logging.info(output.decode('utf-8').rstrip('\n'))

            dirs[:] = [d for d in dirs if d not in ['.git']]
