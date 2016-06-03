/*
  Software serial multple serial test
 
 Receives from the hardware serial, sends to software serial.
 Receives from software serial, sends to hardware serial.
 
 The circuit:
 * RX is digital pin 10 (connect to TX of other device)
 * TX is digital pin 11 (connect to RX of other device)
 
 Note:
 Not all pins on the Mega and Mega 2560 support change interrupts,
 so only the following can be used for RX:
 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69
 
 Not all pins on the Leonardo support change interrupts,
 so only the following can be used for RX:
 8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI).
 
 created back in the mists of time
 modified 25 May 2012
 by Tom Igoe
 based on Mikal Hart's example
 
 This example code is in the public domain.
 
 */
 

#include <SoftwareSerial.h>

SoftwareSerial mc_serial(10, 11); // RX, TX
char serial_msg[8] = {'0','0','0','0','0','0','0','0'}; 

int left_motor_vel = 64;
int right_motor_vel = 64;

int left_motor_vel_pre = 64;
int right_motor_vel_pre = 64;

int msg_validate();

// velocity change smoothing...
int smooth_en = 1; // 0 disable, 1 enable
int smooth_interval_delay = 40; // 10ms between each interval

// saturation (max min boundary)
int saturation_en = 1;
int left_motor_vel_max = 94;
int left_motor_vel_min = 34;
int right_motor_vel_max = 94;
int right_motor_vel_min = 34;

// serial starting messages
void serial_start_msg();

// encoder 

const int enc_CLOCK_PIN_L = 52;
const int enc_DATA_PIN_L = 50;
const int enc_CLOCK_PIN_R = 53;
const int enc_DATA_PIN_R = 51;
const int enc_CS_PIN_L = 8;
const int enc_CS_PIN_R = 9;

const int enc_BIT_COUNT = 10;

double enc_velocity_L = 0;
double enc_velocity_R = 0;
double enc_pos_L = 0;
double enc_pos_R = 0;
double enc_pos_L_pre = 0;
double enc_pos_R_pre = 0;

int enc_duration = 50; // 50 ms
unsigned long enc_time = 0;
unsigned long enc_time_pre = 0;

double power_wheel_dia = 0.25;
double power_wheel_dis = 0.56;

int enc_compute_velocity();
int enc_readPosition() ;
unsigned long enc_shiftIn(int enc_cs_pin, const int data_pin, const int clock_pin, const int bit_count);


// PID controller for speed control
int pid_en = 0;

double pid_Kp_L = 20.0;
double pid_Ki_L = 0.0;
double pid_Kd_L = 0.0;
double pid_Kp_R = 20.0;
double pid_Ki_R = 0.0;
double pid_Kd_R = 0.0;

double pid_e_L = 0.0;
double pid_e_L_pre = 0.0;
double pid_ei_L = 0.0;
double pid_ed_L = 0.0;

double pid_Kp_f_L = 64.0/2.2;
double pid_Kp_f_R = 64.0/2.1;

double pid_e_R = 0.0;
double pid_e_R_pre = 0.0;
double pid_ei_R = 0.0;
double pid_ed_R = 0.0;

double pid_velocity_desired_L = 0.0;
double pid_velocity_desired_R = 0.0;
int pid_motor_vel_L = 64;
int pid_motor_vel_R = 64;

int pid_control();

void setup()  
{
  // Open serial communications and wait for port to open:
  Serial.begin(19200);
  serial_start_msg();

  // set the data rate for the SoftwareSerial port
  mc_serial.begin(9600);
  // set left/right motor velocity to 0
  mc_serial.write(64); // left motor stop
  mc_serial.write(192); // 64 + 128 = 192, right motor stop
  
  // encoder initialization
  pinMode(enc_DATA_PIN_L, INPUT);
  pinMode(enc_CLOCK_PIN_L, OUTPUT);
  pinMode(enc_DATA_PIN_R, INPUT);
  pinMode(enc_CLOCK_PIN_R, OUTPUT);
  pinMode(enc_CS_PIN_L, OUTPUT);
  pinMode(enc_CS_PIN_R, OUTPUT);
  
  digitalWrite(enc_CLOCK_PIN_L, HIGH);
  digitalWrite(enc_CLOCK_PIN_R, HIGH);
  digitalWrite(enc_CS_PIN_L, HIGH);
  digitalWrite(enc_CS_PIN_R, HIGH);
  
  while(enc_readPosition()==0)
  {
    ;
  } 
  enc_time_pre = millis();
  Serial.println("encoder initialized...");
  
  if(pid_en == 1)
  {
    Serial.println("since pid control enabled, disabling saturation and smoothing ...");
    saturation_en = 0;
    smooth_en = 0;
  }
}

void loop() // run over and over
{
  if (Serial.available())
  {
    char c = Serial.read();
    
    if(c == 'e')
    {
      for(int i = 0; i<7; i++)
      {
        serial_msg[i] = serial_msg[i+1];
      }
      serial_msg[7]= c;
      
      if(msg_validate())
      {
        Serial.print("command receveiced: ");
        Serial.println(serial_msg);
        
        if (saturation_en == 1)
        {
          if (left_motor_vel>left_motor_vel_max)
          {
            left_motor_vel = left_motor_vel_max;
            Serial.print("Saturation Applied: left_motor_vel = ");
            Serial.println(left_motor_vel);
          }
          if (left_motor_vel<left_motor_vel_min)
          {
            left_motor_vel = left_motor_vel_min;
            Serial.print("Saturation Applied: left_motor_vel = ");
            Serial.println(left_motor_vel);
          }
          
          if (right_motor_vel>right_motor_vel_max)
          {
            right_motor_vel = right_motor_vel_max;
            Serial.print("Saturation Applied: right_motor_vel = ");
            Serial.println(right_motor_vel);
          }
          if (right_motor_vel<right_motor_vel_min)
          {
            right_motor_vel = right_motor_vel_min;
            Serial.print("Saturation Applied: right_motor_vel = ");
            Serial.println(right_motor_vel);
          }
        }
        
        if(smooth_en == 0)
        {
          // GUTS left wheel corresponds to Motor Controller's motor 1 
          // 1 is full reverse, 64 is stop and 127 is full forward, (-) 1 <---63--- |64| ---63---> 127 (+)
          if(pid_en == 0)
          {
            mc_serial.write(left_motor_vel);
            left_motor_vel_pre = left_motor_vel;
            delay(2);
            // GUTS right wheel corresponds to Motor Controller's motor 2 
            // 129 (128 + 1) is full reverse, 192 (128 + 64) is stop and 255 (127 + 128) is full forward
            // (-) 129 <---63--- |192| ---63---> 255 (+)
            mc_serial.write(right_motor_vel + 128);
            right_motor_vel_pre = right_motor_vel;
            delay(2);
          }
        }
        else
        {
          int left_motor_vel_change = left_motor_vel - left_motor_vel_pre;
          int right_motor_vel_change = right_motor_vel - right_motor_vel_pre;
          
          int max_abs_vel_change = max(abs(left_motor_vel_change),abs(right_motor_vel_change));
          for(int i=0;i<max_abs_vel_change;i++)
          {
            if(i<abs(left_motor_vel_change))
            {
              if(left_motor_vel_change>0)
              {
                mc_serial.write((left_motor_vel_pre+i+1));
                delay(smooth_interval_delay);
              }
              else
              {
                mc_serial.write((left_motor_vel_pre-i-1));
                delay(smooth_interval_delay);
              }
            }
            
            if(i<abs(right_motor_vel_change))
            {
              if(right_motor_vel_change>0)
              {
                mc_serial.write(((right_motor_vel_pre+i+1)+128));
                delay(smooth_interval_delay);
              }
              else
              {
                mc_serial.write(((right_motor_vel_pre-i-1)+128));
                delay(smooth_interval_delay);
              }
            }
          }
          
          // update the velocity memory
          left_motor_vel_pre = left_motor_vel;
          right_motor_vel_pre = right_motor_vel;
        }
      }
    }
    else
    {
      for(int i = 0; i<7; i++)
      {
        serial_msg[i] = serial_msg[i+1];
      }
      serial_msg[7]= c;
    }
    
  }
  
  // show wheel velocity from encoder measurement
  if((millis()-enc_time_pre)>enc_duration)
  {
    enc_time = millis();
    enc_compute_velocity();
  
    // do pid speed control
    if(pid_en == 1)
    {
      pid_control();
    }
    
    enc_time_pre = enc_time;
  }
}

// the serial msg must follow the pattern 'b' + "xxx"(left motor velocity, 1 - 127) + "xxx"(righ motor velocity, 1 - 127) + 'e'
int msg_validate()
{
  if((serial_msg[0]=='b') && isDigit(serial_msg[1]) && isDigit(serial_msg[2]) && isDigit(serial_msg[3]) && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    int left_vel = (serial_msg[1]-'0')*100 + (serial_msg[2]-'0')*10 + (serial_msg[3]-'0')*1;
    int right_vel = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    
    if (left_vel>0 && left_vel<128 && right_vel>0 && right_vel<128)
    {
      left_motor_vel = left_vel;
      right_motor_vel = right_vel;
      
      return 1;
    }
    else
    {
      return 0;
    }
  }
  // smoothing 
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='o') && (serial_msg[3]=='1') && (serial_msg[4]=='0') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg); 
    if(pid_en == 1)
    {
      Serial.println("can not enable velocity change smoothing under pid control mode, disable pid control first...");
      return 0;
    }  
    smooth_en = 1; 
    Serial.println("velocity change smoothing: on");
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='o') && (serial_msg[3]=='0') && (serial_msg[4]=='0') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);   
    smooth_en = 0; 
    Serial.println("velocity change smoothing: off");
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='i') && (serial_msg[3]=='d') && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);
    
    smooth_interval_delay = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    
    Serial.print("smooth_interval_delay: ");
    Serial.print(smooth_interval_delay);
    Serial.println("ms");
    return 0;
  }
  // saturation
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='t') && (serial_msg[3]=='o') && (serial_msg[4]=='1') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);   
    if(pid_en == 1)
    {
      Serial.println("can not enable saturation under pid control mode, disable pid control first...");
      return 0;
    }
    saturation_en = 1; 
    Serial.println("velocity saturation: on");
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='t') && (serial_msg[3]=='o') && (serial_msg[4]=='0') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);   
    saturation_en = 0; 
    Serial.println("velocity saturation: off");
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='l') && (serial_msg[3]=='a') && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    int value = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    if(value<128 && value>0)
    {
      Serial.print("command received: ");
      Serial.println(serial_msg);
      if(value<left_motor_vel_min)
      {
        Serial.println("left_motor_vel_max should >= left_motor_vel_min");
        
      }
      else
      {
        left_motor_vel_max = value;
        Serial.print("left_motor_vel_max: ");
        Serial.println(left_motor_vel_max);
      }
    }    
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='l') && (serial_msg[3]=='i') && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    int value = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    if(value<128 && value>0)
    {
      Serial.print("command received: ");
      Serial.println(serial_msg);
      if(value>left_motor_vel_max)
      {
        Serial.println("left_motor_vel_min should <= left_motor_vel_max");
      }
      else
      {
        left_motor_vel_min = value;
        Serial.print("left_motor_vel_min: ");
        Serial.println(left_motor_vel_min);
      }
    }    
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='r') && (serial_msg[3]=='a') && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    int value = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    if(value<128 && value>0)
    {
      Serial.print("command received: ");
      Serial.println(serial_msg);
      if(value<right_motor_vel_min)
      {
        Serial.println("right_motor_vel_max should >= right_motor_vel_min");
      }
      else
      {
        right_motor_vel_max = value;
        Serial.print("right_motor_vel_max: ");
        Serial.println(right_motor_vel_max);
      }
    }    
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='s') && (serial_msg[2]=='r') && (serial_msg[3]=='i') && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    int value = (serial_msg[4]-'0')*100 + (serial_msg[5]-'0')*10 + (serial_msg[6]-'0')*1;
    if(value<128 && value>0)
    {
      Serial.print("command received: ");
      Serial.println(serial_msg);
      if(value>right_motor_vel_max)
      {
        Serial.println("right_motor_vel_min should <= right_motor_vel_max");
      }
      else
      {
        right_motor_vel_min = value;
        Serial.print("right_motor_vel_min: ");
        Serial.println(right_motor_vel_min);
      }
    }    
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='h') && (serial_msg[2]=='e') && (serial_msg[3]=='l') && (serial_msg[4]=='p') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);    
    Serial.println("HELP manual as follows: ");
    serial_start_msg();
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='p') && (serial_msg[2]=='i') && (serial_msg[3]=='d') && (serial_msg[4]=='o') && (serial_msg[5]=='1') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);    
    Serial.println("PID controller is on, disabling saturation and smoothing...");
    pid_en = 1;
    
    saturation_en = 0;
    smooth_en = 0;
    left_motor_vel = 64;
    right_motor_vel = 64;
    
    //serial_start_msg();
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='p') && (serial_msg[2]=='i') && (serial_msg[3]=='d') && (serial_msg[4]=='o') && (serial_msg[5]=='0') && (serial_msg[6]=='0') && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);    
    Serial.println("PID controller is off, enabling saturation and smoothing...");
    pid_en = 0;
    pid_velocity_desired_L = 0.0;
    pid_velocity_desired_R = 0.0;
    mc_serial.write(64);
    delay(2);
    mc_serial.write(64 + 128);
    delay(2);
    
    saturation_en = 1;
    smooth_en = 1;
    
    //serial_start_msg();
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='v') && (serial_msg[2]=='l') && isDigit(serial_msg[3]) && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);   
    double sign =  serial_msg[3]-'0';
    if (sign!=0 && sign!=1)
    {
      Serial.println("sign of velocity must be 1 (positive) or 0 (negative)");
      return 0;
    }
    else
    {
      if (sign==1)
      {
        sign = 1.0;
      }
      else if (sign == 0)
      {
        sign = -1.0;
      }
    }
    
    double value = sign*((serial_msg[4]-'0')*1.0 + (serial_msg[5]-'0')*0.1 + (serial_msg[6]-'0')*0.01);
    
    if(value<=2.0 && value>=-2.0)
    {
      pid_velocity_desired_L = value;
      Serial.print("pid_velocity_desired_L is set to");
      Serial.println(pid_velocity_desired_L);
      
      if(pid_en == 0)
      {
        Serial.println("remind: BTW, PID is disabled... ");
      }
    }
    else
    {
      Serial.println("pid_velocity_desired_(L/R) must be between -2.0 and 2.0.");
    }
    
    //serial_start_msg();
    return 0;
  }
  else if((serial_msg[0]=='b') && (serial_msg[1]=='v') && (serial_msg[2]=='r') && isDigit(serial_msg[3]) && isDigit(serial_msg[4]) && isDigit(serial_msg[5]) && isDigit(serial_msg[6]) && (serial_msg[7]=='e'))
  {
    Serial.print("command received: ");
    Serial.println(serial_msg);    
    
    double sign =  serial_msg[3]-'0';
    if (sign!=0 && sign!=1)
    {
      Serial.println("sign of velocity must be 1 (positive) or 0 (negative)");
      return 0;
    }
    else
    {
      if (sign==1)
      {
        sign = 1.0;
      }
      else if (sign == 0)
      {
        sign = -1.0;
      }
    }
    
    double value = sign*((serial_msg[4]-'0')*1.0 + (serial_msg[5]-'0')*0.1 + (serial_msg[6]-'0')*0.01);
    
    if(value<=2.0 && value>=-2.0)
    {
      pid_velocity_desired_R = value;
      Serial.print("pid_velocity_desired_R is set to");
      Serial.println(pid_velocity_desired_R);
      
      if(pid_en == 0)
      {
        Serial.println("remind: BTW, PID is disabled... ");
      }
    }
    else
    {
      Serial.println("pid_velocity_desired_(L/R) must be between -2.0 and 2.0.");
    }
    
    //serial_start_msg();
    return 0;
  }
  else
  {
    return 0;
  }
}

void serial_start_msg()
{
  Serial.println("Hi, This is GUTS motor control interface :-)");
  Serial.print("Author: Daobilige Su, ");
  Serial.println("Version: v1.3");
  Serial.println();
  Serial.println("----");
  Serial.println("self parameters:");
  Serial.println();
  Serial.println("serial comm baud rate: 19200");
  if(smooth_en)
  {
    Serial.println("velocity change smoothing: on");
    Serial.print("smooth_interval_delay: ");
    Serial.print(smooth_interval_delay);
    Serial.println("ms");
  }
  else
  {
    Serial.println("velocity change smoothing: off");
  }
  if(saturation_en)
  {
    Serial.println("velocity saturation: on");
    Serial.print("left_motor_vel_max: ");
    Serial.println(left_motor_vel_max);
    Serial.print("left_motor_vel_min: ");
    Serial.println(left_motor_vel_min);
    Serial.print("right_motor_vel_max: ");
    Serial.println(right_motor_vel_max);
    Serial.print("right_motor_vel_min: ");
    Serial.println(right_motor_vel_min);
  }
  else
  {
    Serial.println("velocity saturation: off");
  }
  
  if(pid_en)
  {
    Serial.println("pid control: on");
    
    Serial.print("pid_Kp_L: ");
    Serial.println(pid_Kp_L);
    Serial.print("pid_Ki_L: ");
    Serial.println(pid_Ki_L);
    Serial.print("pid_Kd_L: ");
    Serial.println(pid_Kd_L);
    Serial.print("pid_Kp_f_L: ");
    Serial.println(pid_Kp_f_L);
    Serial.print("pid_velocity_desired_L: ");
    Serial.println(pid_velocity_desired_L);
    
    
    Serial.print("pid_Kp_R: ");
    Serial.println(pid_Kp_R);
    Serial.print("pid_Ki_R: ");
    Serial.println(pid_Ki_R);
    Serial.print("pid_Kd_R: ");
    Serial.println(pid_Kd_R);
    Serial.print("pid_Kp_f_R: ");
    Serial.println(pid_Kp_f_R);
    Serial.print("pid_velocity_desired_R: ");
    Serial.println(pid_velocity_desired_R);
    
  }
  else
  {
    Serial.println("pid control: off");
  }
  
  Serial.println();
  Serial.println("control command format:");
  Serial.println();
  Serial.println("velocity setting:");
  Serial.println("b + xxx (left motor velocity, 1-127, 64 is stop) + xxx(right motor velocity, 1-127, 64 is stop) + e   ");
  Serial.println("");
  Serial.println("velocity change smoothing on/off:");
  Serial.println("b + s + o + 1/0 + 0 + 0 + 0 + e   ");
  Serial.println("");
  Serial.println("smooth_interval_delay:");
  Serial.println("b + s + i + d + xxx (000 - 999, unit is (ms)) + e   ");
  Serial.println("");
  Serial.println("velocity saturation on/off:");
  Serial.println("b + s + t + o + 1/0 + 0 + 0 + e   ");
  Serial.println("");
  Serial.println("left_motor_vel_max (under velocity saturation):");
  Serial.println("b + s + l + a + xxx (001 - 127) + e   ");
  Serial.println("");
  Serial.println("left_motor_vel_min (under velocity saturation):");
  Serial.println("b + s + l + i + xxx (001 - 127) + e   ");
  Serial.println("");
  Serial.println("right_motor_vel_max (under velocity saturation):");
  Serial.println("b + s + r + a + xxx (001 - 127) + e   ");
  Serial.println("");
  Serial.println("right_motor_vel_min (under velocity saturation):");
  Serial.println("b + s + r + i + xxx (001 - 127) + e   ");
  Serial.println("");
  Serial.println("enable PID control (auto disabling serial velocity command, saturation and smoothing)");
  Serial.println("b + p + i + d + o + 1 + 0 + e   ");
  Serial.println("");
  Serial.println("disable PID control (auto enabling serial velocity command, saturation and smoothing)");
  Serial.println("b + p + i + d + o + 0 + 0 + e   ");
  Serial.println("");
  Serial.println("set desired PID velocity of left wheel:");
  Serial.println("b + v + l + x (1 for positive 0 for negative) + xxx (x.xx m/s) + e   ");
  Serial.println("");
  Serial.println("set desired PID velocity of right wheel:");
  Serial.println("b + v + r + x (1 for positive 0 for negative) + xxx (x.xx m/s) + e   ");
  Serial.println("");
  
  Serial.println("HELP (see this manual again):");
  Serial.println("b + h + e + l + p + 0 + 0 + e   ");
  Serial.println("----");
  Serial.println("");
  Serial.println("Enjoy your life with GUTS...");
}


int enc_compute_velocity()
{
  //  show current velocity
  if(enc_readPosition())
  {
    int enc_actual_duration = enc_time-enc_time_pre;
    // compute of the velocity of left wheel
    if((enc_pos_L>=(1024-170)) && (enc_pos_L_pre<=170))
    {
      enc_velocity_L = (double(enc_pos_L - (enc_pos_L_pre+1024))/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    else if((enc_pos_L_pre>=(1024-170)) && (enc_pos_L<=170))
    {
      enc_velocity_L = ((double(enc_pos_L+1024) - enc_pos_L_pre)/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    else
    {
      enc_velocity_L = (double(enc_pos_L - enc_pos_L_pre)/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    enc_velocity_L = enc_velocity_L*(-1); // left wheel encoder is reversed.
     
    // compute of the velocity of right wheel
    if((enc_pos_R>=(1024-170)) && (enc_pos_R_pre<=170))
    {
      enc_velocity_R = (double(enc_pos_R - (enc_pos_R_pre+1024))/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    else if((enc_pos_R_pre>=(1024-170)) && (enc_pos_R<=170))
    {
      enc_velocity_R = ((double(enc_pos_R+1024) - enc_pos_R_pre)/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    else
    {
      enc_velocity_R = (double(enc_pos_R - enc_pos_R_pre)/1024.0)*3.1416*power_wheel_dia/(enc_actual_duration/1000.0);
    }
    
    Serial.print("enc_v_L: ");
    Serial.print(enc_velocity_L,4);
    Serial.print(", enc_v_R: ");
    Serial.print(enc_velocity_R,4);
    Serial.print(", enc_a_dur: ");
    Serial.print(enc_actual_duration);
    //Serial.print(", current_time: ");
    //Serial.print(millis());
    Serial.println();
  }
}

//read the current angular position
int enc_readPosition() 
{
  unsigned long sample1_L = 0;
  unsigned long sample2_L = 0;
  unsigned long sample1_R = 0;
  unsigned long sample2_R = 0;
  while(1)
  {
    // Read the same position data twice to check for errors
    sample1_L = enc_shiftIn(enc_CS_PIN_L,enc_DATA_PIN_L, enc_CLOCK_PIN_L, enc_BIT_COUNT);
    sample2_L = enc_shiftIn(enc_CS_PIN_L,enc_DATA_PIN_L, enc_CLOCK_PIN_L, enc_BIT_COUNT);
    delayMicroseconds(25);  // Clock mus be high for 20 microseconds before a new sample can be taken
  
    if (sample1_L == sample2_L)
      break;
  }

  while(1)
  {
    // Read the same position data twice to check for errors
    sample1_R = enc_shiftIn(enc_CS_PIN_R,enc_DATA_PIN_R, enc_CLOCK_PIN_R, enc_BIT_COUNT);
    sample2_R = enc_shiftIn(enc_CS_PIN_R,enc_DATA_PIN_R, enc_CLOCK_PIN_R, enc_BIT_COUNT);
    delayMicroseconds(25);  // Clock mus be high for 20 microseconds before a new sample can be taken
  
    if (sample1_R == sample2_R)
      break;
  }

  //return ((sample1 & 0x0FFF) * 360UL) / 4096.0;
  enc_pos_L_pre = enc_pos_L;
  enc_pos_L = sample1_L;
  enc_pos_R_pre = enc_pos_R;
  enc_pos_R = sample1_R;
  
  Serial.print("encoder_pos_L: ");
  Serial.print(enc_pos_L);
  //Serial.println();
  Serial.print(", encoder_pos_R: ");
  Serial.print(enc_pos_R);
  //Serial.print("encoder_steps_L: ");
  //Serial.print(enc_pos_L - enc_pos_L_pre);
  //Serial.print(", encoder_steps_R: ");
  //Serial.print(enc_pos_R - enc_pos_R_pre);
  Serial.println();
  
  return 1;
}

//read in a byte of data from the digital input of the board.
unsigned long enc_shiftIn(int enc_cs_pin, const int data_pin, const int clock_pin, const int bit_count) 
{
  unsigned long data = 0;
  
  digitalWrite(enc_cs_pin, LOW);
  delayMicroseconds(1);
  
  for (int i=0; i<bit_count; i++) {
    data <<= 1;
    digitalWrite(clock_pin,LOW);
    delayMicroseconds(1);
    digitalWrite(clock_pin,HIGH);
    delayMicroseconds(1);

    data |= digitalRead(data_pin);
  }
  
  delayMicroseconds(1);
  digitalWrite(enc_cs_pin, HIGH);
  
  return data;
}

int pid_control()
{
  pid_e_L_pre = pid_e_L;
  pid_e_R_pre = pid_e_R;
  
  pid_e_L = pid_velocity_desired_L - enc_velocity_L;
  pid_e_R = pid_velocity_desired_R - enc_velocity_R;
  
  pid_ei_L = pid_ei_L +pid_e_L;
  pid_ei_R = pid_ei_L +pid_e_R;
  
  pid_ed_L = pid_e_L - pid_e_L_pre;
  pid_ed_R = pid_e_R - pid_e_R_pre;
  
  pid_motor_vel_L = int(pid_Kp_L*pid_e_L + pid_Ki_L*pid_ei_L + pid_Kd_L*pid_ed_L + pid_Kp_f_L*pid_velocity_desired_L) + 64;
  pid_motor_vel_R = int(pid_Kp_R*pid_e_R + pid_Ki_R*pid_ei_R + pid_Kd_R*pid_ed_R + pid_Kp_f_R*pid_velocity_desired_R) + 64;
  
  //Serial.print("pid_motor_vel_L: ");
  //Serial.print(pid_motor_vel_L);
  //Serial.print(", pid_motor_vel_R: ");
  //Serial.print(pid_motor_vel_R);
  //Serial.println();
  
  // apply neccesary threshhold
  if(pid_motor_vel_L<1)
  {
    pid_motor_vel_L = 1;
  }
  else if(pid_motor_vel_L>127)
  {
    pid_motor_vel_L = 127;
  }
  
  if(pid_motor_vel_R<1)
  {
    pid_motor_vel_R = 1;
  }
  else if(pid_motor_vel_R>127)
  {
    pid_motor_vel_R = 127;
  }
  
  // write to MC
  mc_serial.write(int(pid_motor_vel_L));
  delay(2);
  mc_serial.write(int(pid_motor_vel_R + 128));
  delay(2);
  
  return 1;
}
