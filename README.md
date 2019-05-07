# A quick driver app to allow forwarding bitalino data in real-time over the network to Unity/Unreal/MAX etc. 

for example: to record at 100Hz, record A1 and A2 channels, without logging to file, and forward over UDP
ip address 192.168.1.10, port 8000,  as OSC to OSC address: Bitalino   
```console
python bitalino_driver.py --no_logging --sampling_rate 100 --analog_channels "0,1" --dest_ip 192.168.1.10 --dest_port 8000 --osc_path Bitalino
```

By default (if you do not specify --no_logging) it will create "logs" directory, and create two files each time you run it.
One file, with extension .logs that contains errors etc. as well as a datafile in .csv format that logs the recorded the
data with timestamps.

