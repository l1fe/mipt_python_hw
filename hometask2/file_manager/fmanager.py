__author__ = 'inaumov'

import shutil

#Simple file manager
#Written by Igor Naumov MIPT 296
#MIPT-Python 2014

import sys

class ExitCommand(object):
    def get_name(self):
        return 'exit'
    def get_args_num(self):
        return 0
    def execute(self, args_line, state=None):
        args = ShellUtils.parse_cmd_params(args_line)
        print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        sys.exit(0)

class ChangeDirCommand(object):
    def get_name(self):
        return 'cd'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

class MoveCommand(object):
    def get_name(self):
        return 'mv'
    def get_args_num(self):
        return 2
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

class CopyCommand(object):
    def get_name(self):
        return 'cp'
    def get_args_num(self):
        return 2
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

class MkdirCommand(object):
    def get_name(self):
        return 'mkdir'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

class InvalidArgumentException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FileManagerShellState(object):
    def __init__(self):
        self.file_manager = FileManager()

class ShellUtils(object):
    @staticmethod
    def parse_cmd_params(cmd_params_line):
        if cmd_params_line is None or str(cmd_params_line).strip() == '':
            return []

        cmd_params_line = str(cmd_params_line).strip()
        args = cmd_params_line.split()

        for i in range(len(args)):
            args[i] = args[i].strip()

        return args

    @staticmethod
    def check_args_num(cmd, args_num):
        if cmd.get_args_num() != args_num:
            raise InvalidArgumentException('{}: expected {} args, got {}'.format(cmd.get_name(), cmd.get_args_num(), args_num))

class Shell(object):
    def __init__(self):
        self.invite_str = '$ '
        self.cmd_map = {}
        self.shell_state = FileManagerShellState()

    def add_cmd(self, cmd):
        if cmd is None:
            raise InvalidArgumentException('Command is empty')

        self.cmd_map[cmd.get_name()] = cmd

    def get_cmd(self, cmd_name):
        return self.cmd_map.get(cmd_name, None)

    def execute_cmds(self, cmds):
        for i in range(len(cmds)):
            cmd = self.get_cmd(cmds[i][0])

            if cmd is None:
                raise InvalidArgumentException('Command \'{}\' not found'.format(cmds[i][0]))

            cmd.execute(cmds[i][1], self.shell_state)

    def parse_cmd_line(self, input_line):
        if input_line is None or str(input_line).strip() is None or str(input_line).strip() == '':
            raise InvalidArgumentException('Invalid command arguments')

        input_line = str(input_line).strip()
        cmd_name = ''
        cmd_params = ''

        first_space_entry_ind = input_line.find(' ')
        if first_space_entry_ind == -1:
            cmd_name = input_line
        else:
            cmd_name = input_line[:first_space_entry_ind].strip()
            cmd_params = input_line[first_space_entry_ind:].strip()

        return cmd_name, cmd_params

    def interactive_mode(self):
        while True:
            print(self.invite_str, end="")
            next_entry = ()
            try:
                next_entry = self.parse_cmd_line(input())
            except InvalidArgumentException as e:
                print('Shell error: {}'.format(e))
                continue

            try:
                self.execute_cmds([next_entry])
            except InvalidArgumentException as e:
                print('Shell error: {}'.format(e))
                continue

    def run(self):
        self.interactive_mode()

class FileManager(object):
    currentdir = '.'
    def remove(self, file_n):
        return 0
    def create(self, file_n):
        return 0
    def move(self, file_n_from, file_n_to):
        return 0
    def copy(self, file_n_from, file_n_to):
        return 0

shell = Shell()
shell.add_cmd(ExitCommand())
shell.add_cmd(ChangeDirCommand())
shell.add_cmd(MkdirCommand())
shell.add_cmd(CopyCommand())
shell.add_cmd(MoveCommand())

shell.run()