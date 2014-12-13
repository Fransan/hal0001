#include <stdlib.h>
//#include <SoftwareSerial.h>
#include <OneWire.h>

#define SSID ""
#define PASS ""
#define COLLECTOR_IP "192.168.2.6"
#define COLLECTOR_PORT "8448"
//SoftwareSerial monitor(10, 11); // RX, TX
OneWire  ds(2);  // on pin 2

void setup()
{
  Serial.begin(9600);
  sendDebug("AT");
  delay(5000);
  if(Serial.find("OK")){
    connectWiFi();
  }
}

void loop(){
  byte i;
  byte present = 0;
  byte data[12];
  byte addr[8];
  
  if ( !ds.search(addr)) {
    //Serial.print("No more addresses.\n");
    ds.reset_search();
    delay(250);
    return;
  }
  
  if ( OneWire::crc8( addr, 7) != addr[7]) {
      return;
  }
  
  ds.reset();
  ds.select(addr);
  ds.write(0x44,0);         // start conversion, with parasite power on at the end
  delay(1000);     // maybe 750ms is enough, maybe not
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad
  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
  }
  
  float tempC = ( (data[1] << 8) + data[0] )*0.0625;
  char buffer[10];
  String tempF = "1,temperature,";
  String tempStr = dtostrf(tempC, 4, 1, buffer);
  tempF += tempStr; 
  updateTemp(tempF);
  delay(10000);
}

void updateTemp(String tenmpF){
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += COLLECTOR_IP;
  cmd += "\",";
  cmd += COLLECTOR_PORT;
  sendDebug(cmd);
  delay(2000);
  if(Serial.find("Error")){
    return;
  }
  cmd = tenmpF;
  cmd += "\r\n";
  Serial.print("AT+CIPSEND=");
  Serial.println(cmd.length());
  if(Serial.find(">")){
    Serial.print(cmd);
  }else{
    sendDebug("AT+CIPCLOSE");
  }
}

void sendDebug(String cmd){
  Serial.println(cmd);
} 
 
boolean connectWiFi(){
  Serial.println("AT+CWMODE=1");
  delay(2000);
  String cmd="AT+CWJAP=\"";
  cmd+=SSID;
  cmd+="\",\"";
  cmd+=PASS;
  cmd+="\"";
  sendDebug(cmd);
  delay(5000);
  if(Serial.find("OK")){
    return true;
  }else{
    return false;
  }
}

