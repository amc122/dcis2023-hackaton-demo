import time
import json
import serial

# List serial devices on MAC or Linux
# >> ls /dev/tty.*
# >> ls /dev/cu.*

# List serial devices on Windows
# - Simply use the devices manager

SERIAL_PORT = '/dev/tty.HACKATON-00' # '/dev/rfcomm0'
BAUDRATE = 9600

def time_ms():
    """
    Returns timestamp in ms
    """
    return int(round(time.time()*1000))

def str2telemetry(serial_str):
    """
    Convert serial string (assuming JSON format) to python dictionary
    """
    recv_dict = json.loads(recv_str)
    telemetry = {
        "ts": time_ms(),
        "values": recv_dict         
    }
    return telemetry

ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()        

while True:
    try: 
        recv = ser.readline()
        if recv != '':
            recv_str = str(recv, 'utf-8')
            try:
                telemetry = str2telemetry(recv_str)
                print(telemetry)
            except:
                pass
            
    
    except KeyboardInterrupt: # i.e. Ctrl+C
        print('\nKeyboard Interrupt')
        ser.close()
        exit()