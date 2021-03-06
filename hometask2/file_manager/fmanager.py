__author__ = 'inaumov'

#Simple file manager
#Written by Igor Naumov MIPT 296
#MIPT-Python 2014

import sys, os, shutil, platform

class ExitCommand(object):
    def get_name(self):
        return 'exit'
    def get_args_num(self):
        return 0
    def execute(self, args_line, state=None):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        sys.exit(0)

class ChangeDirCommand(object):
    def get_name(self):
        return 'cd'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.set_current_dir(args[0])

class TouchCommand(object):
    def get_name(self):
        return 'touch'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.create_file(args[0])

class MoveCommand(object):
    def get_name(self):
        return 'mv'
    def get_args_num(self):
        return 2
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.move(args[0], args[1])

class CopyCommand(object):
    def get_name(self):
        return 'cp'
    def get_args_num(self):
        return 2
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.copy(args[0], args[1])

class MkdirCommand(object):
    def get_name(self):
        return 'mkdir'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.make_dir(args[0])

class RemoveCommand(object):
    def get_name(self):
        return 'rm'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.remove(args[0])

class LsCommand(object):
    def get_name(self):
        return 'ls'
    def get_args_num(self):
        return 1
    def execute(self, args_line, state):
        args = ShellUtils.parse_cmd_params(args_line)
        #print('Args: {}'.format(args))
        ShellUtils.check_args_num(self, len(args))

        state.file_manager.show_content(args[0])

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
        self.invite_str = ' $ '
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
            print(self.shell_state.file_manager.current_dir + self.invite_str, end="")
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
    def __init__(self):
        self.current_dir = os.getcwd()

    def join_with_current_dir(self, file_n):
        return os.path.abspath(os.path.join(self.current_dir, file_n))

    def set_current_dir(self, new_dir):
        new_dir = self.join_with_current_dir(new_dir)
        if not os.path.exists(new_dir) or not os.path.isdir(new_dir):
            raise InvalidArgumentException('Directory {} does not exist'.format(new_dir))

        self.current_dir = new_dir

    def make_dir(self, dir_name):
        dir_name = self.join_with_current_dir(dir_name)
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            raise InvalidArgumentException('Directory {} already exists'.format(dir_name))

        try:
            os.mkdir(dir_name)
        except Exception as e:
            raise InvalidArgumentException(e)

        print('Created', dir_name, 'successfully')

    def create_file(self, file_n):
        file_n = self.join_with_current_dir(file_n)
        with open(file_n, 'a'):
            os.utime(file_n, None)

        print('Created', file_n, 'successfully')

    def show_content(self, dir_name):
        dir_name = self.join_with_current_dir(dir_name)
        if not os.path.exists(dir_name) or not os.path.isdir(dir_name):
            raise InvalidArgumentException('Directory {} does not exist'.format(dir_name))

        print('\n'.join(os.listdir(dir_name)))

    def remove(self, file_n):
        file_n = self.join_with_current_dir(file_n)
        if not os.path.exists(file_n):
            raise InvalidArgumentException('File or directory {} does not exist'.format(file_n))

        try:
            if os.path.isfile(file_n):
                os.remove(file_n)
            elif os.path.isdir(file_n):
                shutil.rmtree(file_n)
        except Exception as e:
            raise InvalidArgumentException(e)

        print('Removed', file_n, 'successfully')

    def move(self, src, dst):
        src = self.join_with_current_dir(src)
        dst = self.join_with_current_dir(dst)
        try:
            shutil.move(src, dst)
        except FileNotFoundError as e:
            raise InvalidArgumentException(e)

        print('Moved', src, 'to', dst, 'successfully')

    def copy(self, src, dst):
        src = self.join_with_current_dir(src)
        dst = self.join_with_current_dir(dst)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
        except Exception as e:
            raise InvalidArgumentException(e)

        print('Copied', src, 'to', dst, 'successfully')

shell = Shell()
shell.add_cmd(ExitCommand())
shell.add_cmd(ChangeDirCommand())
shell.add_cmd(MkdirCommand())
shell.add_cmd(CopyCommand())
shell.add_cmd(MoveCommand())
shell.add_cmd(RemoveCommand())
shell.add_cmd(LsCommand())
shell.add_cmd(TouchCommand())

shell.run()