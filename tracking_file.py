import csv
from datetime import datetime
import time


def main():
    session_times = []
    pause_times = []
    continue_times = []
    fieldnames = ['Start time', 'Pause time(s)', 'Continue time(s)', 'End time']
    with open('start_stop_times.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(fieldnames)

    def start():
        st = datetime.now()
        start_time = st.strftime("%d/%m/%Y %H:%M:%S")
        session_times.append(start_time)

    def end():
        et = datetime.now()
        end_time = et.strftime("%d/%m/%Y %H:%M:%S")
        session_times.append(pause_times)
        session_times.append(continue_times)
        session_times.append(end_time)
        with open('start_stop_times.csv', 'a') as file:
            w = csv.writer(file)
            w.writerow(session_times)

    def pause():
        pt = datetime.now()
        pause_time = pt.strftime("%d/%m/%Y %H:%M:%S")
        pause_times.append(pause_time)

    def cont():
        ct = datetime.now()
        continue_time = ct.strftime("%d/%m/%Y %H:%M:%S")
        continue_times.append(continue_time)

    start()
    time.sleep(4)
    pause()
    time.sleep(7)
    cont()
    time.sleep(6)
    pause()
    time.sleep(2)
    cont()
    time.sleep(5)
    end()



if __name__ == "__main__":
    main()
