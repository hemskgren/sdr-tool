# sdr-tool(s)


### rtl433-counter

count uniqe sender of messages

Requirement: one or two computer with rtl_433 installed and one usb rtl-sdr stick.

On computer with rtl-sdr usb radio stick(server):

```code
$ ifconfig | grep 192
        inet 192.168.96.20  netmask 255.255.255.0  broadcast 192.168.96.255

$ rtl_tcp -a 192.168.96.20 -p 1234 &

Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
```

On client with uv installed.

Help:

```code
$ uv run rtl433-counter.py -h
2025-03-23 20:41:54,947 - INFO - Starting listener
usage: rtl433-counter.py [-h] [--host HOST] [--port PORT] [--frequency FREQUENCY] [--exec EXEC] [--details {yes,no}]

rtl433-counter settings

options:
  -h, --help            show this help message and exit
  --host HOST           Host of the rtl_433 remote listner
  --port PORT           Port of the rtl_433 remote listner
  --frequency FREQUENCY
                        Frequency to listen on remote listner
  --exec EXEC           rtl_433 path
  --details {yes,no}    detail log
```

Starting:

```code
$ uv run rtl433-counter.py --host 192.168.96.20 --details no
2025-03-23 20:16:21,294 - INFO - Starting rtl433-counter
2025-03-23 20:16:21,302 - INFO - Using: /usr/bin/rtl_433 connecting Host: 192.168.96.20 Port: 1234 for listening on frequency: 433.920M
rtl_433 version 23.11 (2023-11-28) inputs file rtl_tcp RTL-SDR SoapySDR
2025-03-23 20:16:36,192 - INFO - Counting seen messages:
{'id': 135,
 'mic': 'CRC',
 'model': 'Fineoffset-TelldusProove',
 'temperature_C': -21.1,
 'time': '2025-03-23 20:16:36'}
Message recived - counter: {'Fineoffset-TelldusProove': 1}
Message recived - counter: {'Fineoffset-TelldusProove': 2}

 ```

 Stopping by ctrl + c and print collected data

 ```code
 ^CSignal caught, exiting!
Stopped by user - print collected data
2025-03-23 20:39:37,123 - INFO - Collected data:
2025-03-23 20:39:37,124 - INFO - {'Fineoffset-TelldusProove': 29}
{'time': '2025-03-23 20:16:36', 'model': 'Fineoffset-TelldusProove', 'id': 135, 'temperature_C': -21.1, 'mic': 'CRC'}
```