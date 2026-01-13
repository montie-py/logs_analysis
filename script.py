# This is a sample Python script.
import subprocess
from datetime import datetime

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class LogEvent:
    def __init__(self, timestamp, user, message, tty, pwd, command):
        self.timestamp = timestamp
        self.user = user
        self.tty = tty
        self.pwd = pwd
        self.command = command,
        self.message = message

def daily_logs():
    # Use a breakpoint in the code line below to debug your script.


    with open("/var/log/auth.log" , encoding="utf-8", errors="replace") as f:
        for line in f.readlines():
            if line.find("sudo:") > 0 and line.find("incorrect") > 0:
                date_chunk = line.split(" ")[0]
                dt = datetime.fromisoformat(date_chunk)
                date = dt.strftime("%Y-%m-%d %H:%M:%S")
                user_message_chunk = line[line.find("sudo: ") + 6:].split(":")
                user = user_message_chunk[0].strip()
                message = user_message_chunk[1][0:user_message_chunk[1].find(';')].strip()
                tty = pwd = command = ""
                if line.find("TTY") > 0:
                    pwd = line[line.find("TTY")+4:].split(";")[0].strip()
                if line.find("PWD") > 0:
                    tty = line[line.find("PWD") + 4:].split(";")[0].strip()
                if line.find("COMMAND") > 0:
                    command = line[line.find("COMMAND") + 8:].split(";")[0].strip()
                break


def too_many_sudos(line):
    if line.find("sudo:") > 0:
        date_chunk = line.split(" ")[0]
        dt = datetime.fromisoformat(date_chunk)
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
        user = line[line.find("sudo: ") + 6:].split(":")[0].strip()
        tty = pwd = command = ""
        if line.find("TTY") > 0:
            pwd = line[line.find("TTY") + 4:].split(";")[0].strip()
        if line.find("PWD") > 0:
            tty = line[line.find("PWD") + 4:].split(";")[0].strip()
        if line.find("COMMAND") > 0:
            command = line[line.find("COMMAND") + 8:].split(";")[0].strip()


        print("date: %s, user: %s, tty: %s, pwd: %s, command: %s" % (date, user, tty, pwd, command))


def check_anomalies(output_line):
    too_many_sudos(output_line)


def realtime_logs():
    auth_tail = subprocess.Popen(
        ["tail", "-F", "/var/log/auth.log"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in auth_tail.stdout:
        check_anomalies(line.strip())




if __name__ == '__main__':
    realtime_logs()
    # daily_logs()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
