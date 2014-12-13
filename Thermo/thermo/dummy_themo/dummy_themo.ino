void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  Serial.print("1,temperature,72");
  Serial.println();
  delay(5000);
}
