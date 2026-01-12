# This is a sample Python script.
from datetime import datetime

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_logs():
    # Use a breakpoint in the code line below to debug your script.


    with open("/var/log/auth.log" , encoding="utf-8", errors="replace") as f:
        for line in f.readlines():
            if (line.find("sudo:") > 0):
                date_chunk = line.split(" ")[0]
                dt = datetime.datetime.fromisoformat(date_chunk)
                date = dt.strftime("%Y-%m-%d %H:%M:%S")
                user = line[line.find("sudo: ") + 6:].split(":")[0].strip()
                tty = ""
                if line.find("TTY=") > 0:
                    tty = line[line.find("TTY")+4:].split(";")[0].strip()
                break


if __name__ == '__main__':
    print_logs()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
