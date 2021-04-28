from mycroft_bus_client import MessageBusClient, Message

import serial
import serial.tools.list_ports as list_ports

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1

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


def main():
    print('Setting up client to connect to a local mycroft instance')
    client = MessageBusClient()
    client.run_in_thread()


    client.emit(Message('speak', data={'utterance': 'I am listening'}))

    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:  # If it isn't a blank line
            line = line.strip()
            if line == 'button:a':
                client.emit(Message('mycroft.mic.listen'))
            print(line)
    ser_micro.close()

main()
