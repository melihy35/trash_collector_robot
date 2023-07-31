#ifndef GRIPPER_h
#define GRIPPER_h

#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"


#define GRIPPER_DROP_ANGLE 0
#define GRIPPER_HOLD_ANGLE 100
#define GRIPPER_FALLING_ANGLE 0
#define GRIPPER_RISING_ANGLE 30
#define GRIPPER_DIVING_ANGLE 30
#define GRIPPER_LEAVE_ANGLE 180
#define GRIPPER_DONT_SCAN_ANGLE 100
#define GRIPPER_SCAN_ANGLE 25



enum GripperState
{
  GRIPPER_OPEN = 0,
  GRIPPER_CLOSE = 1
};


class Gripper
{
  private:
    uint8_t pin_mservo;
    uint8_t pin_kservo;
    uint8_t pin_hservo;
    uint8_t pin_vservo;
    uint8_t pin_ir_1;
    uint8_t pin_ir_2;
    uint8_t pin_mdet;
    Servo hservo;
    Servo vservo;
    Servo mservo;
    Servo kservo;

  public:
    bool auto_hold;

    GripperState state;
    Gripper();
    void init(uint8_t pin_hservo_, uint8_t pin_vservo_, uint8_t pin_mservo_, uint8_t pin_kservo_, uint8_t pin_mdet_, uint8_t pin_ir_1_, uint8_t pin_ir_2_);
    bool hold();
    void drop();
    bool isObjectDetected();
    bool detectMaterial();
};

#endif
