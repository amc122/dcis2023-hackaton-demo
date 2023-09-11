from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

HOST = "192.168.0.23"
DEVICE_TOKEN = "rNMToKmO1ddrD2IXJl0X"

telemetry = {"potentiometer": 50.0}#, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
client = TBDeviceMqttClient(HOST, username=DEVICE_TOKEN)
# Connect to ThingsBoard
client.connect()
# Sending telemetry without checking the delivery status
# client.send_telemetry(telemetry) 
# Sending telemetry and checking the delivery status (QoS = 1 by default)
result = client.send_telemetry(telemetry)
# get is a blocking call that awaits delivery status  
success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
# Disconnect from ThingsBoard
client.disconnect()
