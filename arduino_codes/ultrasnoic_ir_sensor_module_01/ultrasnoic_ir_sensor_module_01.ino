









#include <Wire.h>

#define SRF_1_ADD 112
#define SRF_2_ADD 113
#define SRF_3_ADD 115
#define SRF_4_ADD 116
#define SRF_5_ADD 117
#define SRF_6_ADD 118

int srf_adds[6] = {SRF_1_ADD, SRF_2_ADD, SRF_3_ADD, SRF_4_ADD, SRF_5_ADD, SRF_6_ADD};
int srf_reading[6] = {0,0,0,0,0,0};
unsigned long rf_start_time = 0;
unsigned long ultrosonic_transmision_time[6] = {0,0,0,0,0,0};

void do_receive_us();

#include <VirtualWire.h>
#define receive_pin 11
byte message[VW_MAX_MESSAGE_LEN];
byte messageLength = VW_MAX_MESSAGE_LEN;

void setup()
{
  Wire.begin();                // join i2c bus (address optional for master)
  Serial.begin(9600);          // start serial communication at 9600bps
  
  vw_set_rx_pin(receive_pin);
  vw_setup(2000); // bps
  vw_rx_start();
   
  Serial.println("ready...");
}



void loop()
{
  
  if (vw_get_message(message, &messageLength))
  {
    do_receive_us();
  }
  
  
}


void do_receive_us()
{
  //Serial.println("got rf");
  rf_start_time = micros();
  
  // step 1: instruct sensor to read echoes
  for(int i = 0; i<6; i++)
  {   
    Wire.beginTransmission(srf_adds[i]); // transmit to device #112 (0x70)
                                 // the address specified in the datasheet is 224 (0xE0)
                                 // but i2c adressing uses the high 7 bits so it's 112
    Wire.write(byte(0x00));      // sets register pointer to the command register (0x00)  
    Wire.write(byte(0x58));      // command sensor to measure in "inches" (0x50)
                                 // use 0x51 for centimeters
                                 // use 0x52 for ping microseconds
                                 // 0x58 	Fake Ranging Mode - Result in micro-seconds
    Wire.endTransmission();      // stop transmitting
    ultrosonic_transmision_time[i] = micros();
  }

  // step 2: wait for readings to happen
  delay(70);                   // datasheet suggests at least 65 milliseconds

  
  // step 3: instruct sensor to return a particular echo reading
  for(int i = 0; i<6; i++)
  { 
    Wire.beginTransmission(srf_adds[i]); // transmit to device #112
    Wire.write(byte(0x02));      // sets register pointer to echo #1 register (0x02)
    Wire.endTransmission();      // stop transmitting
  }

  for(int i = 0; i<6; i++)
  { 
    // step 4: request reading from sensor
    Wire.requestFrom(srf_adds[i], 2);    // request 2 bytes from slave device #112
  
    // step 5: receive reading from sensor
    if(2 <= Wire.available())    // if two bytes were received
    {
      srf_reading[i] = Wire.read();  // receive high byte (overwrites previous reading)
      srf_reading[i] = srf_reading[i] << 8;    // shift high byte to be high 8 bits
      srf_reading[i] |= Wire.read(); // receive low byte as lower 8 bits
      
      if (srf_reading[i]>0)
      {
        srf_reading[i] = srf_reading[i] + (ultrosonic_transmision_time[i] - rf_start_time);
      }
    }
  }

  for(int i = 0; i<6; i++)
  { 
    Serial.print(srf_reading[i]);Serial.print(' ');
  }
  Serial.println();

}
