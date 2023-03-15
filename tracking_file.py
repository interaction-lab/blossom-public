import csv
from datetime import datetime
import time

session_times = []
pause_times = []
continue_times = []

def start():
    global session_times
    st = datetime.now()
    start_time = st.strftime("%d/%m/%Y %H:%M:%S")
    session_times.append(start_time)


def end():
    global session_times, pause_times, continue_times
    et = datetime.now()
    end_time = et.strftime("%d/%m/%Y %H:%M:%S")
    session_times.append(pause_times)
    session_times.append(continue_times)
    session_times.append(end_time)
    with open('start_stop_times.csv', 'a') as file:
        w = csv.writer(file)
        w.writerow(session_times)


def pause():
    global pause_times
    pt = datetime.now()
    pause_time = pt.strftime("%d/%m/%Y %H:%M:%S")
    pause_times.append(pause_time)


def cont():
    global continue_times
    ct = datetime.now()
    continue_time = ct.strftime("%d/%m/%Y %H:%M:%S")
    continue_times.append(continue_time)

def main():

    fieldnames = ['Start time', 'Pause time(s)', 'Continue time(s)', 'End time']
    with open('start_stop_times.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(fieldnames)




if __name__ == "__main__":
    main()
