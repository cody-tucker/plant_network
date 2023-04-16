#define SensorPin A0
#define MosfetPin D4

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(4, OUTPUT);

}

void loop() {
  // tell the mosfet to let power thru and wait 1 sec
  digitalWrite(MosfetPin, HIGH);
  delay(1000);

  // read the sensor
  float sensor_value = analogRead(SensorPin);
  Serial.println(sensor_value);
  delay(1000);
  // tell the mosfet to stop power flow
  digitalWrite(MosfetPin, LOW);
  // now wait 10sec before taking the next measurement
  delay(10000);

}
