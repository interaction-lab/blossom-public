import csv
import datetime


def main():
    session_times = []
    pause_times = []
    continue_times = []
    fieldnames = ['Start time', 'Pause time(s)', 'Continue time(s)', 'End time']
    with open('start_stop_times.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

    def start():
        st = datetime.now()
        start_time = now.strftime("%d/%m/%Y %H:%M:%S")
        session_times.append(start_time)

    def end():
        et = datetime.now()
        end_time = now.strftime("%d/%m/%Y %H:%M:%S")
        session_times.append(pause_times)
        session_times.append(continue_times)
        sesion_times.append(end_time)
        with open('start_stop_times.csv', 'a') as file:
            w = csv.writer(file)
            w.writerow(session_times)

    def pause():
        pt = datetime.now()
        pause_time = now.strftime("%d/%m/%Y %H:%M:%S")
        pause_times.append(pause_time)

    def cont():
        ct = datetime.now()
        continue_time = now.strftime("%d/%m/%Y %H:%M:%S")
        continue_times.append(continue_time)


if __name__ == "__main__":
    main()
