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

top1 = 'indoor/palm/moisture'
top2 = 'outdoor/veggies/moisture'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

channel_list = ['indoor/palm/moisture', 'outdoor/veggies/moisture']

class SensorData():
	"""
	Class stores sensor data when recieved
	"""
	def __init__(self, location, datatype, value):
		self.location = location
		self.datatype = datatype
		self.value = value

def multi_channel_sub(client, channel_list):
	for i in channel_list:
		print(f'Subscribing to {i}..')
		con = client.subscribe(i)
		print(con)
			
	
def on_connect(client, userdata, flags, rc):
		"""The callback for when client receives CONNACK from the server"""
		print("Connected with result code (rc)" +str(rc))

		#client.subscribe(MQTT_TOPIC)
		con1 = client.subscribe(top1)
		print(con1)
		con2 = client.subscribe(top2)
		print(con2)
		
def on_message(client, userdata, msg):
	"""The callback for when a PUBLISH message is received from the server
	unless there is a specific on_message callback for that topic"""
	print(f'The topic is: {str(msg.topic)} with msg: {str(msg.payload)}')
	print(type(msg.payload))
	payload = str(msg.payload)
	print(str(msg.payload))
	print(payload[2:-1])
	topic = str(msg.topic)
	
	# Get the payload data we want. formatted as "Topic_666.00"
	if payload[2:-1] == 'HELLO':
		sensor_data = None
	else:
		data_payload = payload.split('_')[-1]
		sensor_data = float(data_payload[0:-1])
		
		data_topic = topic.split('/')
		# Now get the topic which will contain the sensor location (for now)
		location_data = data_topic[1]
		print(location_data)
		measurement_data = 'soil_moisture'
		
		current_data = SensorData(location_data, measurement_data, sensor_data)
		
		
	# if we have real data (not the test data 'HELLO') send it to influx db		
	if sensor_data is not None:
		send_sensor_data_to_influxdb(current_data)
		
def on_message_indoor(client, userdata, msg):
	"""
	for specific subscription... gonna take a different route rn...
	"""
	print(f'The topic is: {str(msg.topic)} with msg: {str(msg.payload)}')
	print(type(msg.payload))
	payload = str(msg.payload)
	print(str(msg.payload))
	print(payload[2:-1])
	topic = str(msg.topic)
	
	# Get the payload data we want. formatted as "Topic_666.00"
	if payload[2:-1] == 'HELLO':
		sensor_data = None
	else:
		data_payload = payload.split('_')[-1]
		sensor_data = float(data_payload[0:-1])
		
		data_topic = topic.split('/')
		# Now get the topic which will contain the sensor location (for now)
		location_data = data_topic.split('/')[1]
		measurement_data = 'soil_moisture'
		
		current_data = SensorData(location_data, measurement_data, sensor_data)
		
		
	# if we have real data (not the test data 'HELLO') send it to influx db		
	if sensor_data is not None:
		send_sensor_data_to_influxdb(current_data)
	
	

		
def send_sensor_data_to_influxdb(sensor_data):
	json_body = [
	{
	'measurement':sensor_data.datatype,
	'tags':{
	'location':sensor_data.location
		},
	'fields': {
	'value': sensor_data.value
	}
	}
	]
	influxdb_client.write_points(json_body)
	
def init_influxdb_database():
	databases = influxdb_client.get_list_database()
	if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
		influxdb_client.create_database(INFLUXDB_DATABASE)
	influxdb_client.switch_database(INFLUXDB_DATABASE)
	
def main(channel_list):
	init_influxdb_database()
	
	mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
	mqtt_client.on_connect = on_connect
	#multi_channel_sub(mqtt_client, channel_list)
	mqtt_client.on_message = on_message
	#mqtt_client.message_callback_add("indoor/palm/moisture", on_message_indoor)
	#mqtt_client.on_message_add("outdoor/veggies/moisture", on_message_outdoor)
	
	mqtt_client.connect(MQTT_ADDRESS, 1883)
	mqtt_client.loop_forever()
	
	# Here add on message callbacks for each topic
	
	
if __name__=="__main__":
	print("MQTT to InfluxDB Bridge is running...")
	main(channel_list)
