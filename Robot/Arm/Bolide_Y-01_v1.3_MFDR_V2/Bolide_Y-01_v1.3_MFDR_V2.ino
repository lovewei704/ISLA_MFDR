//Include Library
#include <BOLIDE_Player.h>
#include <A1_16.h>
#include <EEPROM.h>
#include <Wire.h>
#include "BOLIDE_Y-01_Board.h"
#include "Y-01_Mask_Definition.h"
#include "Y-01_USER_MOTION.h"

//== Declare Global Parameters ==
//Normal Operation Pararmeter
BOLIDE_Player XYZrobot;
unsigned char table[8] = {0};
static float ax, ay, az;
static int I2C_Address = 0x3B >> 1;
static int distance;
static int SN_packet[9] = {0}, SN_packet_index = 0, inByte = 0;
static int packet[7], LED_mode, g_packet[8], ir_packet[4], ir_msb, ir_lsb, ir_rowdata;
static boolean torque_release = false;
//Motion Editor Parameter
static boolean packet_timeout_status = false;
static boolean seq_trigger = false, seq_loop_trigger = false;
static int seq_pSeqCnt = 0xFF, SeqPos = 0x00;
static int poses[max_pose_index][MAX_SERVOS];      // poses [index][servo_id-1], check for the motion index!!
static int pose_index[max_pose_index];
sp_trans_t sequence[max_seq_index];// sequence

//========================= Set up =======================================
void setup() {
  //Configure all basic setting
  Serial.begin(115200);
  XYZrobot.setup(115200, 18); //Configure A1-16 servo motor
  Serial2.begin(115200); //Configure BT board
  Timer_Task_Setup();
  _enable_timer4();

  //Start motion
  Initial_Pose_Setup();
  delay(1000);
}
//========================= Main =======================================
void loop() {
  int readdata = 0, i = 0, count = 0;

  if (Serial2.available() > 0) //從藍芽接收到資料後執行
  {
    while ((readdata = Serial2.read()) != (int) - 1) //將訊息資料依序放入陣列中
    {
      table[count] = readdata;
      //Serial.println(table[count]);
      count++;
      delay(1);
    }
    
    if (table[0] == 255) // 若藍芽第一筆資料為255則執行
    {
      if (table[3] == 1)   Action(1);    //若第四筆資料為1則執行機器人內已設定完成的動作(1)
      else if (table[3] == 2)  Action(2);//若第四筆資料為2則執行機器人內已設定完成的動作(2)
      else if (table[3] == 3)  Action(3);//若第四筆資料為3則執行機器人內已設定完成的動作(3)
      else if (table[3] == 4)  Action(4);//若第四筆資料為4則執行機器人內已設定完成的動作(4)
      else if (table[3] == 5)  Action(5);//若第四筆資料為5則執行機器人內已設定完成的動作(5)
      else if (table[3] == 6)  Action(6);//若第四筆資料為6則執行機器人內已設定完成的動作(6)
      else if (table[3] == 7)  Action(7);//若第四筆資料為7則執行機器人內已設定完成的動作(7)
    }
  }
}

//=========================== Function ================================
//== Setup function ==
// Timer Setup
void Timer_Task_Setup(void) {
  //Set Timer3 as a normal timer for LED task
  TCCR3A = 0x00;
  TCCR3B |= _BV(CS32); TCCR3B &= ~_BV(CS31); TCCR3B |= _BV(CS30);
  //Set Timer4 as a normal timer for communcation timeout
  TCCR4A = 0x00;
  TCCR4B |= _BV(CS42); TCCR4B &= ~_BV(CS41); TCCR4B |= _BV(CS40);
  //Set Timer5 as a Fast PWM generator for chest LED driver
  TCCR5A = _BV(COM5A1) | _BV(COM5B1) | _BV(COM5C1) | _BV(WGM51) | _BV(WGM50);
  TCCR5B = _BV(WGM52) | _BV(CS52);
  OCR5A = 0; OCR5B = 0; OCR5C = 0;
}

//Initial Pose Task 開機預設動作
void Initial_Pose_Setup(void) {
  XYZrobot.readPose();
  XYZrobot.playSeq(ActionNo_1);
  while (XYZrobot.playing) XYZrobot.play();
}

//Action Task
void Action(int N) {
  if (N == 1) XYZrobot.playSeq(ActionNo_1);
  else if (N == 2) XYZrobot.playSeq(ActionNo_2);
  else if (N == 3) XYZrobot.playSeq(ActionNo_3);
  else if (N == 4) XYZrobot.playSeq(ActionNo_4);
  else if (N == 5) XYZrobot.playSeq(ActionNo_5);
  else if (N == 6) XYZrobot.playSeq(ActionNo_6);
  else if (N == 7) XYZrobot.playSeq(ActionNo_7);

  while ((XYZrobot.playing) && !(BT_Packet_Task())) {
    XYZrobot.play();
    if (Serial2.available() > 0) {
      if (BT_Packet_Task()) {
        cb_BT();
        break;
      }
    }
  }
  if (torque_release) {
    A1_16_TorqueOff(A1_16_Broadcast_ID);
    torque_release = false;
  }
}

//BT Reading Task
boolean BT_Packet_Task(void) {
  //return torque_relase button status
  static int temp_packet[7] = {0};
  static char _i = 0;
  if (Serial2.available() >= 7) {

    for (_i = 0; _i < 7 ; _i++) {
      if ((temp_packet[_i] = Serial2.read()) == 0) {
        find_header_BT();
        return false;
      }
    }

    for (_i = 0; _i < 7 ; _i++) packet[_i] = temp_packet[_i];

    if (packet[1] == 255 && packet[2] == 1 && packet[3] == 102) {
      torque_release = true;
      return true;
    }
    else {
      torque_release = false;
      return false;
    }
  }
  return false;
}

// Clean BT Buffer
void cb_BT(void) {
  while ((Serial2.read()) != -1);
}
void find_header_BT(void) {
  while (Serial2.available() > 0) {
    if (Serial2.peek() == 0) return;
  }
}

ISR(TIMER3_OVF_vect) {
  static int R = 0, G = 0, B = 0;
  static int _R = 41, _G = 41, _B = 41;
  static boolean blink_LED = true;
  if (LED_mode == 1) {
    if (blink_LED) EYE_LED_BLE;
    else EYE_LED_GRN;
    blink_LED = !blink_LED;
    _reset_timer3(4500);
  }
  else if (LED_mode == 2) {
    if (R < 40) {
      R++;
      OCR5A = pgm_read_word_near(&log_light_40[R]);
    }
    else if (_R > 0) {
      _R--;
      OCR5A = pgm_read_word_near(&log_light_40[_R]);
    }
    else if (G < 40) {
      G++;
      OCR5B = pgm_read_word_near(&log_light_40[G]);
      EYE_LED_BLE;
    }
    else if (_G > 0) {
      _G--;
      OCR5B = pgm_read_word_near(&log_light_40[_G]);
    }
    else if (B < 40) {
      B++;
      OCR5C = pgm_read_word_near(&log_light_40[B]);
      EYE_LED_GRN;
    }
    else if (_B > 0) {
      _B--;
      OCR5C = pgm_read_word_near(&log_light_40[_B]);
    }
    else {
      R = 0; G = 0; B = 0;
      _R = 41; _G = 41; _B = 41;
    }
    _reset_timer3(200);
  }
  else if (LED_mode == 3) {
    if (R < 40) {
      R++;
      OCR5A = pgm_read_word_near(&log_light_40[R]);
    }
    else if (_R > 0) {
      _R--;
      OCR5A = pgm_read_word_near(&log_light_40[_R]);
    }
    else if (G < 40) {
      G++;
      OCR5B = pgm_read_word_near(&log_light_40[G]);
    }
    else if (_G > 0) {
      _G--;
      OCR5B = pgm_read_word_near(&log_light_40[_G]);
    }
    else if (B < 40) {
      B++;
      OCR5C = pgm_read_word_near(&log_light_40[B]);
    }
    else if (_B > 0) {
      _B--;
      OCR5C = pgm_read_word_near(&log_light_40[_B]);
    }
    else {
      R = 0; G = 0; B = 0;
      _R = 41; _G = 41; _B = 41;
    }
    _reset_timer3(200);
  }
}

ISR(TIMER4_OVF_vect) {
  Power_Detection_Task();
  packet_timeout_status = true;
  _reset_timer4(timeout_limit);
}

// Power Detection function
void Power_Detection_Task(void) {
  static double PWR_Voltage;
  PWR_Voltage = analogRead(PWRDET_PIN) * 0.0124;
  if (PWR_Voltage < Power_Voltage_Alarm) tone(BUZZER_PIN, 1000);
}
