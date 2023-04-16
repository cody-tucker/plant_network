
int blue_light = 8;
int red_light = 7;

void setup() {
  // put your setup code here, to run once:
  pinMode(blue_light, OUTPUT);
  pinMode(red_light, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(blue_light, HIGH);
  digitalWrite(red_light, LOW);
  delay(1000);
  digitalWrite(blue_light, LOW);
  digitalWrite(red_light, HIGH);
  delay(1000);

}
