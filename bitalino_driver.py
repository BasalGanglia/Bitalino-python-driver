# -*- coding: utf-8 -*-
"""
Commandline python tool for forwarding Bitalino data over network.

@author: Ilkka
"""

import argparse
import random
import time
import sys
import socket
import signal
import datetime
import argparse

from bitalino import BITalino
import numpy as np

from pythonosc import osc_message_builder
from pythonosc import udp_client
from struct import *
from util.log_writer import log_writer

class Bitalino_driver:
  
  def __init__(self):
    self.interrupter = False
    def signal_handler(signal, frame):
      print( "caught a signal")
      # global interrupter
      self.interrupter = True
  
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
  def main(self):   
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--sampling_rate", help = "Sampling rate used for recording data", type = int, default = 10)
    parser.add_argument("--offline", help="run in offline mode", action="store_true")
    parser.add_argument("--logging", help="Log the data", action="store_true", default="True")  
    parser.add_argument("--osc_path", help="the osc path prefix", default="Bitalino")
    parser.add_argument("--dest_ip",
                          help="IP address of the destination", default="127.0.0.1")
    parser.add_argument("--dest_port", help="the port", type=int, default=8000)
    parser.add_argument("--mac_address", default = "20:16:12:22:45:56")
    parser.add_argument("--battery_threshold", default = 30)
    parser.add_argument("--analog_channels", default = "0,1,2,3,4,5")
    parser.add_argument("--batch_size", help = "number of samples read in batch", type = int, default = 10)
  
  
    args = parser.parse_args()

    the_logger = log_writer(True)
    the_logger.log_msg("Starting up.")
    
    # Testing the csv logger:
   # the_logger.log_data([1, 3, 4, 5, 6])
   # return
    
# The channel list parsing is bit of a hack.. I'm sure there is some more pythonesque way of doing this
    anal_channels = args.analog_channels.split(',')
    channels = list(map(int, anal_channels))
  
   # acqChannels = [0, 1, 2, 3, 4, 5]
    #samplingRate = 1000
    
    # small samping rate for testing..
    analogChannels= args.analog_channels
    samplingRate = args.sampling_rate
    nSamples = args.batch_size
    
    # Connect to BITalino
    device = BITalino(args.mac_address)
    
    # Set battery threshold
    batty = device.battery(args.battery_threshold)
  
  # If we are not in offline mode we start streaming to given UDP port.
  # He we just create a UDPClient for that.
    if not args.offline:
      client = udp_client.SimpleUDPClient(args.dest_ip, args.dest_port)  
  
  # Add stuff like which channels to record here!!
    running_time = 10
    
    # Read BITalino version
    print(device.version())
    
    # Start recording
    
    print("The channels we are recording: {0} ".format(channels))
    device.start(samplingRate, channels)
  #  device.start(samplingRate, acqChannels)
    # Turn BITalino led on
    # device.trigger(digitalOutput) 
   
    while self.interrupter == False:  
  
      # Start Acquisition
      rec_data = device.read(nSamples)  
    
#      print("Data shape {0}, and first row{1}".format(rec_data.shape, rec_data[0]))
      print("full data is {0}".format(rec_data))
      current_time = datetime.datetime.now().timestamp()
 #     print("current_time is now: ", current_time)
      #  We have to generate time stamps for each of the samples we record in a batch.
      for sample in rec_data:
#        print("current_time before printing to sample: ", current_time)
        # Delete digital channels (that contains just zeroes but that cannot be ignored)
        # maybe this delete/insert thing is inefficient, but hopefully not inefficient enough
        # to cause issues...
        sample = np.delete(sample, [0, 1, 2, 3, 4])
        sample = np.insert(sample, 0, current_time)
        the_logger.log_data(sample)
        current_time += (1.0 / samplingRate)
        print("storing sample: ", sample)
      # print("and the mean for EDA (A1) is {0}".format(np.mean(rec_data[:][5])))

  #    print("current time after loop ", current_time)
  
  #  Following code just for State of Darkness!! Does not generalize and will break if EDA is
  #  recorded from somewhere other than first channel.
      EDA_data = np.mean(rec_data, axis= 0)[5]
      osc_address = args.osc_path + "/EDA"
      msg = osc_message_builder.OscMessageBuilder(address = osc_address)     
      msg.add_arg(EDA_data)
      msg = msg.build()
      if not args.offline:
        client.send(msg)

    # Stop acquisition
    device.stop()
    
    # Close connection
    device.close()
    
    return

if __name__ == "__main__":
  # # Attempt to ctrl-c work in windows.. not very succesful.
  driver = Bitalino_driver()
  
  driver.main()
