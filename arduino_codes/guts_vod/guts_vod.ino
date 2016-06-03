
#include <VirtualWire.h>
#define rf_pin 12 // rf transmit_pin is default 12

unsigned long last_time_u = 0;

#include <Wire.h>
#define SRF_ADD 112

void setup() 
{
 
  Wire.begin();                // join i2c bus (address optional for master)
  
  vw_set_tx_pin(rf_pin);
  vw_setup(2000); // bps
  
}

void loop() {
  if(micros()>(last_time_u+200000))
  {
    last_time_u = last_time_u + 200000;
    
    send("a"); //send a rf message
    
    Wire.beginTransmission(SRF_ADD); // transmit to device #112 (0x70)
                                 // the address specified in the datasheet is 224 (0xE0)
                                 // but i2c adressing uses the high 7 bits so it's 112
    Wire.write(byte(0x00));      // sets register pointer to the command register (0x00)  
    Wire.write(byte(0x5C));      // command sensor to measure in "inches" (0x50)
                                 // use 0x51 for centimeters
                                 // use 0x52 for ping microseconds
                                 // 0x58 	Fake Ranging Mode - Result in micro-seconds
                                 // 0x5C        Transmit an 8 cycle 40khz burst - no ranging takes place
    Wire.endTransmission();      // stop transmitting

    
  }
}

void send (char *message)
{
  vw_send((uint8_t *)message, strlen(message));
  vw_wait_tx();
  
}
