from mycroft_bus_client import MessageBusClient, Message

import serial
import serial.tools.list_ports as list_ports

import time

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1

min_signal = -1
max_signal = -255

client = None
listen_once = True
speak_once = True

def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None

def parse_message(msg):
    global min_signal
    global max_signal
    global client
    global listen_once

    print(msg)

    if 'rssi' in msg:
        rssi = msg.split(':')
        signal = int(rssi[1])

        if signal < min_signal:
            min_signal = signal
        
        if signal > max_signal:
            max_signal = signal

        if signal > -50:
            if listen_once:
                listen_once = False
                client.emit(Message('speak', data={'utterance': 'Hello there, ready to talk?'}))
                time.sleep(3)
                client.emit(Message('mycroft.mic.listen'))


def main():
    global client

    print('Setting up client to connect to a local mycroft instance')
    client = MessageBusClient()
    client.run_in_thread()

    client.emit(Message('speak', data={'utterance': 'Ping'}))

    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    while True:
        line = ser_micro.readline()
        if line:  # If it isn't a blank line
            line = line.strip().decode('UTF-8')
            parse_message(line)
    ser_micro.close()

main()
