# -*- coding: utf-8 -*-
"""
Commandline python tool for forwarding Bitalino data over network.

@author: Ilkka Kosunen (ilkka.kosunen@gmail.com)
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

        #  The following code allows interruption of recording by using
        #  the normal CTRL+C interrupt

        self.interrupter = False

        def signal_handler(signal, frame):
            print("caught a signal")
            # global interrupter
            self.interrupter = True

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def main(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--sampling_rate",
            help="Sampling rate used for recording data",
            type=int,
            default=10,
        )
        parser.add_argument(
            "--offline", help="run in offline mode", action="store_true"
        )
        parser.add_argument(
            "--logging",
            dest="logging",
            help="Log the data",
            action="store_true",
            default=True,
        )
        parser.add_argument(
            "--no_logging", dest="logging", help="Log the data", action="store_false"
        )

        parser.add_argument(
            "--osc_path", help="the osc path prefix", default="/Bitalino"
        )
        parser.add_argument(
            "--dest_ip", help="IP address of the destination", default="127.0.0.1"
        )
        parser.add_argument("--dest_port", help="the port", type=int, default=5005)
        parser.add_argument("--mac_address", default="84:BA:20:AE:BC:42")
        parser.add_argument("--battery_threshold", default=30)
        parser.add_argument("--analog_channels", default="0,1,2,3,4,5")
        parser.add_argument(
            "--batch_size", help="number of samples read in batch", type=int, default=10
        )
        parser.add_argument(
            "--EDA_channel", help="the analog channel inded of EXA", type=int, default=1
        )

        args = parser.parse_args()

        the_logger = log_writer(args.logging)
        the_logger.log_msg("Starting up.")

        # The channel list parsing is bit of a hack.. I'm sure there is some more pythonesque way of doing this
        anal_channels = args.analog_channels.split(",")
        channels = list(map(int, anal_channels))

        # small samping rate for testing..
        analogChannels = args.analog_channels
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

        # Start recording

        device.start(samplingRate, channels)

        while self.interrupter == False:

            # Start Acquisition
            rec_data = device.read(nSamples)

            current_time = datetime.datetime.now().timestamp()
            for sample in rec_data:
                # Delete digital channels (that contains just zeroes but that cannot be ignored)
                # maybe this delete/insert thing is inefficient, but hopefully not inefficient enough
                # to cause issues...
                sample = np.delete(sample, [0, 1, 2, 3, 4])
                sample = np.insert(sample, 0, current_time)
                the_logger.log_data(sample)
                current_time += 1.0 / samplingRate

            #  Following code just for State of Darkness!! Does not generalize and will break if EDA is
            #  recorded from somewhere other than first channel.
            EDA_data = np.mean(rec_data, axis=0)[(4 + args.EDA_channel)]
            print("the EDA_data is:  ", EDA_data)
            osc_address = args.osc_path + "/EDA"
            msg = osc_message_builder.OscMessageBuilder(address=osc_address)
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
    driver = Bitalino_driver()
    driver.main()
