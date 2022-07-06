import time
import os


def formatted_time(time_value):
    return time.strftime('%H:%M:%S', time.localtime(time_value))


def session_time(time_value):
    seconds = int(time_value % 60)
    minutes = int(time_value / 60 % 60)
    hours = int(time_value / 60 / 60)

    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


def print_log(text):
    print(formatted_time(time.time()) + ': ' + text)


def write_log(text):
    insert_time = time.time()
    formatted_insert_time = formatted_time(insert_time)
    file_name = time.strftime('%d.%m.%Y', time.localtime(insert_time))
    dir_name = 'log'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    path = dir_name + '/' + file_name
    file = open(path, 'a')
    file.write(formatted_insert_time + ': ' + text + '\n')
    print_log(text)
