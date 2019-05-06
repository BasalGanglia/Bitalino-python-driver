import csv, datetime, os

class log_writer:
    def __init__(self, logging):
        # Start logging. One log file in strict .csv format for the raw data.
        # Another log file for triggers, error messages etc. Both have timestamp
        # as name, and endings .log and .csv

        #  if logging is set to false we do not log
        self.logging = logging
        if not self.logging:
            return
            
        
# Check if there is directory for log files, if not, create it.        
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        
        current_time = str(datetime.datetime.now().timestamp())
        current_time = current_time.replace(".", "_")
        self.log_file = open("./logs/" + current_time + ".log", 'w')
        self.data_file = open("./logs/" + current_time + ".csv", 'w')
        self.to_csv = csv.writer(self.data_file, delimiter = ',')
        
    # the following will write (generic) message in the log with timestamp.
    # perhaps useful for triggers etc.
    def log_msg(self, msg):
        if not self.logging:
            return
        current_time = str(datetime.datetime.now().timestamp())
        self.log_file.write(current_time +": " + msg + "\n")
        self.log_file.flush()
      
    # Log a data in csv format.   
    def log_data(self, data):
        if not self.logging:
            return
        self.to_csv.writerow(data)
       
    
    #  Destructor: Close the files the object gets destroyed.
    def __del__(self):
        if not self.logging:
            return       
        current_time = str(datetime.datetime.now().timestamp())
        self.log_msg(current_time +": " + " the end.")
        self.data_file.close()
        self.log_file.close()
        