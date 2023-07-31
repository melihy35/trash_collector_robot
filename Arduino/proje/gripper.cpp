#include "gripper.h"


Gripper::Gripper()
{
  state = GRIPPER_OPEN;
  auto_hold = false;
}

void Gripper::init(uint8_t pin_hservo_, uint8_t pin_vservo_, uint8_t pin_mservo_, uint8_t pin_kservo_, uint8_t pin_mdet_, uint8_t pin_ir_1_, uint8_t pin_ir_2_)
{
  pin_hservo = pin_hservo_;
  pin_vservo = pin_vservo_;
  pin_mservo = pin_mservo_;
  pin_kservo = pin_kservo_;

  pin_ir_1 = pin_ir_1_;
  pin_ir_2 = pin_ir_2_;
  pinMode(pin_ir_1, INPUT);
  pinMode(pin_ir_2, INPUT);

  pin_mdet = pin_mdet_;
  pinMode(pin_mdet, INPUT);

  hservo.attach(pin_hservo);
  hservo.write(GRIPPER_DROP_ANGLE);
  
  vservo.attach(pin_vservo);
  vservo.write(GRIPPER_FALLING_ANGLE);
  
  mservo.attach(pin_mservo);
  mservo.write(GRIPPER_LEAVE_ANGLE);
  
  kservo.attach(pin_kservo);
  kservo.write(GRIPPER_DONT_SCAN_ANGLE);
}

bool Gripper::hold()
{
  state = GRIPPER_CLOSE;
  hservo.write(GRIPPER_HOLD_ANGLE);
  delay(500);
  vservo.write(GRIPPER_RISING_ANGLE);
  delay(500);

  return true;
}

void Gripper::drop()
{
  state = GRIPPER_OPEN;
  auto_hold = false;
  vservo.write(GRIPPER_FALLING_ANGLE);
  delay(500);
  hservo.write(GRIPPER_DROP_ANGLE);
  delay(500);
}

bool Gripper::isObjectDetected()
{
  int cnt = 0;
  for (int i = 0; i < 50; i++)
  {
    if (!digitalRead(pin_ir_1))
    {
      cnt++;
    }
    if (!digitalRead(pin_ir_2))
    {
      cnt++;
    }
  }
  if ((float)cnt / 100.0 > 0.4)
  {
    return true;
  }
  else
  {
    return false;
  }
}

bool Gripper::detectMaterial()
{
  bool isMetal = false;
  for (int i = 0; i < 4; i++)
  {
    mservo.write(GRIPPER_DIVING_ANGLE);

    unsigned long start = millis();
    while (millis() - start < 500)
    {
      isMetal |= !digitalRead(pin_mdet); 
    }

    if (i > 1)
    {
      for (int i=GRIPPER_DONT_SCAN_ANGLE; i >= GRIPPER_SCAN_ANGLE; i--)
      {  
        kservo.write(i);
        isMetal |= !digitalRead(pin_mdet); 
        delay(5);
        isMetal |= !digitalRead(pin_mdet); 
      }
      
      start = millis();
      while (millis() - start < 100)
      {
        isMetal |= !digitalRead(pin_mdet); 
      }
      
      kservo.write(GRIPPER_DONT_SCAN_ANGLE);
      isMetal |= !digitalRead(pin_mdet); 

      start = millis();
      while (millis() - start < 100)
      {
        isMetal |= !digitalRead(pin_mdet); 
      }    
    }
          
    isMetal |= !digitalRead(pin_mdet); 
    mservo.write(GRIPPER_LEAVE_ANGLE);
    isMetal |= !digitalRead(pin_mdet); 

    start = millis();
    while (millis() - start < 500)
    {
      isMetal |= !digitalRead(pin_mdet); 
    }
  }

  return isMetal;
}
