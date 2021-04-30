from microbit import *
import radio

radio.config(group=2)
radio.on()

while True:
    details = radio.receive_full()
    if details:
        message, rssi, timestamp = details
        print(str(message, 'UTF-8'))
        print("rssi:" + str(rssi))