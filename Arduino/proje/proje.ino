#include "gripper.h"


#define GRIPPER_MSERVO_PIN 11
#define GRIPPER_KSERVO_PIN 6
#define GRIPPER_HSERVO_PIN 9
#define GRIPPER_VSERVO_PIN 10
#define GRIPPER_IR_1 12
#define GRIPPER_IR_2 13
#define GRIPPER_MDET A0

#define MSG_HOLD "HOLD"
#define MSG_AUTO_HOLD "AUTO_HOLD"
#define MSG_DROP "DROP"
#define MSG_FDB_IS_DET "IS_DET"
#define MSG_FDB_IS_HOLD "IS_HOLD"
#define MSG_FDB_IS_METAL "IS_METAL"

#define MSG_DET_OK "DET_OK"
#define MSG_DET_NOT_OK "DET_NOT_OK"
#define MSG_HOLD_OK "HOLD_OK"
#define MSG_HOLD_NOT_OK "HOLD_NOT_OK"
#define MSG_METAL "METAL"
#define MSG_NOT_METAL "NOT_METAL"


Gripper gripper;

void setup() {
  gripper.init(GRIPPER_HSERVO_PIN, GRIPPER_VSERVO_PIN, GRIPPER_MSERVO_PIN, GRIPPER_KSERVO_PIN, GRIPPER_MDET, GRIPPER_IR_1, GRIPPER_IR_2);

  Serial.begin(9600);
  Serial.setTimeout(50);
}

void loop() {
  /*
  if (gripper.state == GRIPPER_OPEN && gripper.auto_hold)
  {
    if (gripper.isObjectDetected())
    {
      gripper.auto_hold = false;
      gripper.hold();
    }
  }
  */

  if (Serial.available())
  {
    String msg = Serial.readString();
    msg.trim();
    //Serial.println(msg);

    if (gripper.state == GRIPPER_OPEN && msg == MSG_HOLD)
    {

      Serial.println(MSG_HOLD_OK);
      gripper.hold();
    }
    else if (msg == MSG_AUTO_HOLD)
    {
      gripper.auto_hold = !gripper.auto_hold;
    }
    else if (gripper.state == GRIPPER_CLOSE && msg == MSG_DROP)
    {
      Serial.println(MSG_HOLD_NOT_OK);
      gripper.drop();
    }
    else if (msg == MSG_FDB_IS_DET)
    {
      if (gripper.isObjectDetected())
      {
        Serial.println(MSG_DET_OK);
      }
      else
      {
        Serial.println(MSG_DET_NOT_OK);
      }
    }
    else if (msg == MSG_FDB_IS_HOLD)
    {
      if (gripper.state == GRIPPER_CLOSE)
      {
        Serial.println(MSG_HOLD_OK);
      }
      else
      {
        Serial.println(MSG_HOLD_NOT_OK);
      }
    }
    else if (msg == MSG_FDB_IS_METAL)
    {
      if (gripper.detectMaterial() == true)
      {
        Serial.println(MSG_METAL);
      }
      else
      {
        Serial.println(MSG_NOT_METAL);
      }
    }
  }


}
