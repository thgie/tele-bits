from microbit import *
import radio

radio.config(group=2)
radio.on()

while True:
    details = radio.receive_full()
    if details:
        message, rssi, timestamp = details
        print(message)
        print("rssi", rssi)
#     message = radio.receive()
#     if message:
#         print(message)