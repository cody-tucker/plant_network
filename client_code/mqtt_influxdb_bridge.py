import re
#from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '192.168.1.249' # ip of the rasp_pi
INFLUXDB_USER = 'ct'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'moisture_data'

MQTT_ADDRESS = '192.168.1.249'
MQTT_USER = 'testuser1'
MQTT_PASSWORD = 'test1'
MQTT_TOPIC = 'moisture'
MQTT_CLIENT_ID = 'MQTT_InfluxDB_Bridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
	
def on_connect(client, userdata, flags, rc):
		"""The callback for when client receives CONNACK from the server"""
		print("Connected with result code (rc)" +str(rc))
		client.subscribe(MQTT_TOPIC)
		
def on_message(client, userdata, msg):
	"""The callback for when a PUBLISH message is received from the server"""
	print(msg.topic + "" + str(msg.payload))
	print(type(msg.payload))
	payload = str(msg.payload)
	print(str(msg.payload))
	print(payload[2:-1])
	if payload[2:-1] == 'HELLO':
		sensor_data = None
	else:
		payload = payload.split('_')[-1]
		#sensor_data = float(msg.payload)
		sensor_data = float(payload[0:-1])
	if sensor_data is not None:
		send_sensor_data_to_influxdb(sensor_data)
		
def send_sensor_data_to_influxdb(sensor_data):
	json_body = [
	{
	'measurement':'soil_moisture',
	'tags':{
	'location':'palm'
		},
	'fields': {
	'value': sensor_data
	}
	}
	]
	influxdb_client.write_points(json_body)
	
def init_influxdb_database():
	databases = influxdb_client.get_list_database()
	if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
		influxdb_client.create_database(INFLUXDB_DATABASE)
	influxdb_client.switch_database(INFLUXDB_DATABASE)
	
def main():
	init_influxdb_database()
	
	mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
	mqtt_client.on_connect = on_connect
	mqtt_client.on_message = on_message
	
	mqtt_client.connect(MQTT_ADDRESS, 1883)
	mqtt_client.loop_forever()
	
if __name__=="__main__":
	print("MQTT to InfluxDB Bridge is running...")
	main()
