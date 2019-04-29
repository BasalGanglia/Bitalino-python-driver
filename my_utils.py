import csv, datetime, os

class logWriter:
    def __init__(self):
        # Start logging. One log file in strict .csv format for the raw data.
        # Another log file for triggers, error messages etc. Both have timestamp
        # as name, and endings .log and .csv

# Check if there is directory for log files, if not, create it.        
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        
        current_time = str(datetime.datetime.now().timestamp())
        current_time = current_time.replace(".", "_")
#        logfilename = current_time + ".log"               
        self.log_file = open("./logs/" + current_time + ".log", 'w')
        self.data_file = open("./logs/" + current_time + ".csv", 'w')
        self.to_csv = csv.writer(self.data_file, delimiter = ',')
        
    # the following will write (generic) message in the log with timestamp.
    # perhaps useful for triggers etc.
    def log_msg(self, msg):
        current_time = str(datetime.datetime.now().timestamp())
        self.log_file.write(current_time +": " + msg)
        self.log_file.flush()
      
    # Log a data in csv format.   
    def log_data(self, data):
        self.to_csv.writerow(data)
        pass
        
    def close_it_all(self):
        current_time = str(datetime.datetime.now().timestamp())
        self.log_file.write(current_time +": " + " the end.")
        self.data_file.close()
        self.log_file.close()
        