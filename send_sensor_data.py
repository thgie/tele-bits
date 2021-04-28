from microbit import *
import radio

radio.config(group=2)
radio.on()

while True:
    if button_a.is_pressed():
        radio.send('button:a')
    if button_b.is_pressed():
        radio.send('button:b')

    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    radio.send("accelerometer:"+str(x)+","+str(y)+","+str(z))

    sleep(500)