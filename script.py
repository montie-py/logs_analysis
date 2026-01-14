# This is a sample Python script.
import subprocess
import os
from datetime import datetime, timedelta

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

sudo_log_events = []

class SudoLogEvent:
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
                date = datetime.fromisoformat(date_chunk)
                # date = dt.strftime("%Y-%m-%d %H:%M:%S")
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


def sudo_alarm_logic(sudo_log_event):
    if not sudo_log_events :
        sudo_log_events.append(sudo_log_event)
    else:
        mins_difference = ((sudo_log_event.timestamp - sudo_log_events[0].timestamp) < timedelta(minutes=5))

        if mins_difference:
            sudo_log_events.append(sudo_log_event)
        else:
            sudo_log_events.clear()

        if len(sudo_log_events) == 3:
            os.system("paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga")
            print("⚠️ Anomaly detected: multiple failed SUDO logins:")
            for sudo_log_event in sudo_log_events:
                date = sudo_log_event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f'date: {date}'
                    f'| user: {sudo_log_event.user}'
                    f'| pwd: {sudo_log_event.pwd}'
                    f'| tty: {sudo_log_event.tty}'
                    f'| command: {sudo_log_event.command}'
                    f'| message: {sudo_log_event.message}'
                )
            sudo_log_events.clear()





def too_many_sudos(line):
    if line.find("sudo:") > 0:
        date_chunk = line.split(" ")[0]
        date = datetime.fromisoformat(date_chunk)
        user_message_chunk = line[line.find("sudo: ") + 6:].split(":")
        user = user_message_chunk[0].strip()
        message = user_message_chunk[1][0:user_message_chunk[1].find(';')].strip()
        tty = pwd = command = ""
        if line.find("TTY") > 0:
            pwd = line[line.find("TTY") + 4:].split(";")[0].strip()
        if line.find("PWD") > 0:
            tty = line[line.find("PWD") + 4:].split(";")[0].strip()
        if line.find("COMMAND") > 0:
            command = line[line.find("COMMAND") + 8:].split(";")[0].strip()

        sudo_log_event = SudoLogEvent(date, user, message, tty, pwd, command)

        sudo_alarm_logic(sudo_log_event)

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
