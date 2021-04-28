from microbit import *
import radio

radio.config(group=2)
radio.on()

while True:
    message = radio.receive()

    if message:
        print(message)
