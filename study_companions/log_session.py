import csv
from datetime import datetime
import socket
import boto3
import subprocess

# The rpi name
rpi_name = socket.gethostname()

# Set up AWS credentials and region
aws_access_key_id = 'AKIATOJSXW3AQXDXSRNZ'
aws_secret_access_key = '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'
region_name = 'us-west-2'

# Set up S3 bucket and file name
bucket_name = 'study-companions-spring-23'


class SessionLogger():
    def __init__(self, filename = "start_stop_times_"):
        self.log_fname = filename + str(rpi_name) + ".csv"
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

    def store_log(self):
        print("We will create an S3 client")
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)
        # Upload log to S3
        try:
            print("We are uploading this")
            s3.upload_file(self.log_fname, bucket_name, self.rpi_name + "/" + self.day + "/" + self.log_fname)
            print('File ' + self.log_fname + ' uploaded successfully')
        except Exception as e:
            print('Error uploading ' + self.log_fname)
        print("We have called subprocess")

