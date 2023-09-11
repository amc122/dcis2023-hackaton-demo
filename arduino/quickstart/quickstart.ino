#include <SoftwareSerial.h>
// [Include more libraries here], e.g. for DHT:
// #include <DHT.h>

#define USB_BAUDRATE 9600
#define BT_BAUDRATE 9600

#define BT_RX D3 // software serial Tx
#define BT_TX D2 // software serial Rx

#define POTEN_PIN A1
#define POTEN_PERIOD 500 // milliseconds

// [Add more pins and sampling periods here], e.g. for DHT:
// #define DHT_PIN D4
// #define DHT_TYPE DHT11
// #define DHT_PERIOD 10000 // milliseconds


// Use SoftwareSerial for bluetooth
SoftwareSerial btSerial(BT_TX, BT_RX);

// [Instantiate more classes here], e.g. for DHT:
// DHT dhtSensor(DHT_PIN, DHT_TYPE);


// Example class to handle sensors and bluetooth telemetry
class MySensors{
  private:
    // Potentiometer
    long potenLevel;
    long potenLastCheck;
    long potenPeriod = POTEN_PERIOD;
    
    // [Add more variables here], e.g. for DHT sensor:
    // float dhtHumidity;
    // float dhtTemperature;
    // long dhtLastCheck;
    // long dhtPeriod = DHT_PERIOD;
    
  public:
    // Funcion para sincronizar los periodos
    void syncChecks(){
      int now = millis();
      this->potenLastCheck = now;
      // [Add additional time counts here], e.g. for DHT:
      // this->dhtLastCheck = now;
    }
    
    // Function to handle potentiometer readings
    void handlePoten(){
      // check timing
      if (millis() - potenLastCheck >= potenPeriod){
        // update last check
        this->potenLastCheck = millis();
        // read potentiometer value
        this->potenLevel = analogRead(POTEN_PIN);
        // send bluetooth data in JSON format
        btSerial.write("{\"potentiometer\":");
        btSerial.print(potenLevel);
        btSerial.write("}\r\n");
      }
    }

    // [Add additional sensor handling functions here], e.g. for DHT:
    /* void handleDht(){
      // check timing
      if (millis() - dhtLastCheck >= dhtPeriod){
        // update last check
        this->dhtLastCheck = millis();
        // [Your code to read temperature and humidity]
        // [Your code to send bluetooth data in JSON format]
      }
    } */

};


// Instantiate custom classes
MySensors sensors;


// Setup default and bluetooth serial ports, pin modes, etc.
void setup(){
  Serial.begin(USB_BAUDRATE); 
  btSerial.begin(BT_BAUDRATE);
  
  sensors.syncChecks();
}


// In the main loop, we read sensor data and send it over bluetooth.
// Optionally, you might want to add control for additional elements/devices 
// such as buttons, leds, displays, and/or handling incoming bluetooth data.
void loop(){

  // Recieve bluetooth data
  if (btSerial.available())
    Serial.write(btSerial.read());

  // Receive data from default serial port
  if (Serial.available())
    btSerial.write(Serial.read());

  // Handle sensors
  sensors.handlePoten();
  // [Handle additional sensors] e.g. for DHT: sensors.handleDht();

  // [Handle other devices such as buttons, leds, displays, etc.]

}
