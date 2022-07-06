import sys
import time
import Logger
from DB import DB


class Timer:
    start_time = 0
    commands = {
        'q': 'quit',
        'r': 'run/pause timer',
        's': 'stop timer',
        'h': 'help',
    }
    loops = []
    db = None

    def __init__(self):
        self.db = DB()

    def show_commands(self, with_error: bool = False):
        if with_error:
            print('the command does not exist')
            print('please enter correct command')

        for key in self.commands:
            print(key + ': ' + self.commands[key])

    def run(self):
        self.insert_loop(time.time())

    def stop(self):
        self.out()

    def out(self):
        if self.is_running():
            self.run()

        self.calc_session_time()
        Logger.write_log('exit...')
        sys.exit()

    def calc_loop_time(self, loop):
        start = loop[0]

        if len(loop) == 2:
            end = loop[1]
        else:
            end = time.time()

        return end - start

    def calc_session_time(self):
        session_time = 0

        for loop in self.loops:
            session_time += self.calc_loop_time(loop)

        return session_time

    def last_loop_index(self):
        loops_len = len(self.loops)
        return loops_len - 1

    def last_loop_len(self):
        last_loop = self.loops[self.last_loop_index()]

        return len(last_loop)

    def is_started(self):
        return len(self.loops) > 0

    def is_paused(self):
        if not self.is_started():
            return False

        return self.last_loop_len() == 2

    def is_running(self):
        if not self.is_started():
            return False

        return self.last_loop_len() == 1

    def insert_loop(self, insert_time):
        if not self.is_started():
            self.start_time = insert_time
            self.loops.insert(0, [insert_time])
            Logger.write_log('timer started...')
        else:
            loops_len = len(self.loops)

            if self.is_running():
                loop = self.loops[self.last_loop_index()]
                loop.insert(1, insert_time)
                self.db.insert(loop[0], loop[1])

                Logger.write_log('timer paused...')
                Logger.write_log('loop time: ' + Logger.session_time(self.calc_loop_time(loop)))
                Logger.write_log('session time: ' + Logger.session_time(self.calc_session_time()))
            elif self.is_paused():
                self.loops.insert(loops_len, [insert_time])
                Logger.write_log('timer continued...')

    def run_command(self, command: str):
        if command == 'q':
            self.out()
        elif command == 'r':
            self.run()
        elif command == 's':
            self.stop()
        elif command == 'h':
            self.show_commands()
        elif command == 'l':
            # print(self.loops)
            for row in self.db.select():
                print(row)
        else:
            self.show_commands(True)

    def exec(self):
        print('\nenter command:')
        command = input()

        self.run_command(command)
        self.exec()
