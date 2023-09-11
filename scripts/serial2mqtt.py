import time
import json
import serial
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

SERIAL_PORT = "/dev/tty.HACKATON-00" #"/dev/rfcomm0"
BAUDRATE = 9600
HOST = "192.168.0.23"
DEVICE_TOKEN = "rNMToKmO1ddrD2IXJl0X"
TELEMETRY_BUFFER = 8


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

# Open serial communication if needed
ser.isOpen()    
# MQTT client
client = TBDeviceMqttClient(HOST, username=DEVICE_TOKEN)  

while True:
    try: 
        recv = ser.readline()
        if recv != '':
            recv_str = str(recv, 'utf-8')
            try:
                telemetry = str2telemetry(recv_str)
                client.connect()
                result = client.send_telemetry(telemetry)
                success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
                client.disconnect()
                print(telemetry)
            except:
                print(f"WARNING - Received invalid string: {recv_str}")
            
    
    except KeyboardInterrupt: # i.e. Ctrl+C
        print("\nKeyboard Interrupt")
        # Close serial communication
        ser.close()
        exit()