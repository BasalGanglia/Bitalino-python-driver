import time
from bitalino import BITalino
import numpy as np

# This example will collect data for 5 sec.
macAddress = "20:16:12:22:45:56"
# macAddress = "/dev/tty.BITalino-XX-XX-DevB" # on Mac OS replace XX-XX by the 4 final digits of the MAC address
running_time = 30
    
batteryThreshold = 30

#  From the API doc:
#  1. Sequnce number
#  4. digital channels (always present)
#  1-6 analog channels.

A1 = ""
#acqChannels = [0, 1, 2, 3, 4, 5]
#samplingRate = 1000

# small samping rate for testing..
analogChannels= [0, 1]
samplingRate = 10

nSamples = 10
digitalOutput = [1,1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())
    
# Start Acquisition
device.start(samplingRate, analogChannels)

start = time.time()
end = time.time()
while (end - start) < running_time:
    # Read samples
    rec_data = device.read(nSamples)
    print("Data shape {0}, and first row{1}".format(rec_data.shape, rec_data[0]))
    print("full data is {0}".format(rec_data))
   # print("and the mean for EDA (A1) is {0}".format(np.mean(rec_data[:][5])))
    print("means for the batch{0}".format(np.mean(rec_data, axis= 0)))
    end = time.time()

# Turn BITalino led on
device.trigger(digitalOutput)
    
# Stop acquisition
device.stop()
    
# Close connection
device.close()