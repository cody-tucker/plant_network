//#include <WiFi.h>
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

// Pin on ESP8266 to receive soil moisture data
#define SensorPin A0

//WiFi Info
char ssid[] = "Level2Diagnostic";
const char* password = "TokyoDrifter32";

// MQTT Info
//const char* mqtt_server = "192.168.178.82";
IPAddress broker(192,168,1,249);
const int mqtt_port = 1883;
const char* mqtt_username = "testuser1";
const char* mqtt_password = "test1";
//MQTT channels
const char* moisture_topic = "moisture";
const char* client_id = "client_indoor";

//unsigned long previousMillis = 0;
//unsigned long interval = 40000;
//
//unsigned long restartInterval = 10000;
//unsigned long previousRestartMillis = 0;

// Initialize WiFi and MQTT Client Objects
WiFiClient wifiClient;
PubSubClient client(wifiClient);

//void connect_MQTT(){
//  delay(10);
//  Serial.println();
//  Serial.print("Connecting to...");
//  Serial.println(ssid);
//
//  //Connect to WiFi
//  WiFi.begin(ssid, password);
//  //Wait until connection is confirmed before continuing
//  while (WiFi.status() != WL_CONNECTED){
//    delay(500);
//    Serial.print(".");
////    // if it takes more than 10seconds to connect on boot, then restart
////    if (currentRestartMillis - previousRestartMillis >= restartInterval){
////      ESP.restart();
//  }
//  //Debugging
//  Serial.println("WiFi Connected");
//  Serial.print("IP address: ");
//  Serial.println(WiFi.localIP());
//
//  //Connect to MQTT Broker
//  // see my old code for better version?
//  if (client.connect(client_id, mqtt_username, mqtt_password)){
//    Serial.println("Succesful connection to MQTT Broker!");
//  }
//  else{
//    Serial.println("Failed to connect to MQTT Broker...");
//  } 
//}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(10);
  Serial.println('\n');

  WiFi.begin(ssid, password);
  Serial.print("Connecting to...");
  Serial.print(ssid);
  Serial.println("...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(++i);
    Serial.print(" ");
  }

  Serial.println('\n');
  Serial.println("WiFi connection established");
  Serial.println("My IP address is: ");
  Serial.print(WiFi.localIP());

  client.setServer(broker, mqtt_port);
  client.setKeepAlive(60);

    //Connect to the mqtt broker on rasp pi
  Serial.print('\n');
  Serial.println("Connecting to MQTT Broker...");
  Serial.print(broker);
  Serial.print(':');
  Serial.print(mqtt_port);

  
  while (!client.connected()) {
    Serial.print('\n');
    Serial.println("Attempting MQTT Connection...");
    client.connect(client_id);
    if (client.connect(client_id)) {
      Serial.println("Succesful connection to MQTT Broker!");
      client.publish(moisture_topic, "HELLO");
    }
    else{
      Serial.println("Connection to MQTT Broker Failed...");
      Serial.print('\n');
      Serial.print("rc= ");
      Serial.print(client.state());
      Serial.println("Trying again in 3 seconds...");
      delay(3000);
    }
  }
  


}

void loop() {
//  //unsigned long currentMillis = millis();
//  //connect_MQTT();
//  //previousMillis = currentMillis;
//  //Serial.setTimeout(2000);
//


  

  // read the sensor
  float sensor_value = analogRead(SensorPin);
  Serial.println(sensor_value);
  delay(10000);

  //Convert reading to string and package for sending
  String send_val="Moisture_" + String((float)sensor_value);
  //String send_val = String((float)sensor_value);

  if (client.publish(moisture_topic, send_val.c_str())){
    Serial.println("Data Sent!");
  }
  else{
    Serial.println("Data failed to send...Reconnecting to Broker to try again...");
    Serial.print("rc= ");
    Serial.print(client.state());
    Serial.println();
    client.connect(client_id);
    delay(100);
    client.publish(moisture_topic, send_val.c_str());
  }
  client.disconnect();
  delay(1000);

  // sleep for 20mins 1.2e9
  // 30mins = 1.8e9
  ESP.deepSleep(1.2e9);
  //ESP.deepSleep(60000);

  


}
