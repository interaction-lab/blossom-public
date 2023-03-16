import csv
from datetime import datetime
import time

participant_number = 3

class SessionLogger():
    def __init__(self, filename = "start_stop_times_p"):
        self.log_fname = filename + str(participant_number) + ".csv"
        fieldnames = ['Event Type', 'Time']
        with open(self.log_fname, 'a') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(fieldnames)

    def log_event(self, event):
        dt = datetime.now()
        time = dt.strftime("%d/%m/%Y %H:%M:%S")
        with open(self.log_fname, 'a') as file:
            w = csv.writer(file)
            w.writerow([event, time])
        
# class SessionLogger():
#     def __init__(self):
#         log_fname = "start_stop_times_" + str(participant_number) + ".csv"
#         fieldnames = ['Start time', 'Pause time(s)', 'Continue time(s)', 'End time']
#         with open(log_fname, 'a') as csvfile:
#             writer = csv.writer(csvfile)
#             if csvfile.tell() == 0:
#                 writer.writerow(fieldnames)
#         self.start_time = "NULL"
#         self.end_time = "NULL"
#         self.pause_start_times = ["NULL"]
#         self.pause_end_times = ["NULL"]

    
#     def log_start_time():
#         global session_times
#         st = datetime.now()
#         start_time = st.strftime("%d/%m/%Y %H:%M:%S")
#         session_times.append(start_time)



        

# session_times = []
# pause_times = []
# continue_times = []

# def start():
#     global session_times
#     st = datetime.now()
#     start_time = st.strftime("%d/%m/%Y %H:%M:%S")
#     session_times.append(start_time)


# def end():
#     global session_times, pause_times, continue_times
#     et = datetime.now()
#     end_time = et.strftime("%d/%m/%Y %H:%M:%S")
#     session_times.append(pause_times)
#     session_times.append(continue_times)
#     session_times.append(end_time)
#     with open('start_stop_times.csv', 'a') as file:
#         w = csv.writer(file)
#         w.writerow(session_times)


# def pause():
#     global pause_times
#     pt = datetime.now()
#     pause_time = pt.strftime("%d/%m/%Y %H:%M:%S")
#     pause_times.append(pause_time)


# def cont():
#     global continue_times
#     ct = datetime.now()
#     continue_time = ct.strftime("%d/%m/%Y %H:%M:%S")
#     continue_times.append(continue_time)

# def main():

#     fieldnames = ['Start time', 'Pause time(s)', 'Continue time(s)', 'End time']
#     with open('start_stop_times.csv', 'a') as csvfile:
#         writer = csv.writer(csvfile)
#         if csvfile.tell() == 0:
#             writer.writerow(fieldnames)




# if __name__ == "__main__":
#     main()