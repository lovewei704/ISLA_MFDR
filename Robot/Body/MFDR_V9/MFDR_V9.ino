  //#include "MeOrion.h"
#include "MeShield.h"
#include <Wire.h>
#include <SoftwareSerial.h>

MeEncoderNew motor1(0x09, SLOT1);   //  Motor1 at slot1
MeEncoderNew motor2(0x09, SLOT2);   //  motor2 at slot2
MeEncoderNew motor3(0x0a, SLOT1);   //  Motor3 at slot1
MeEncoderNew motor4(0x0a, SLOT2);   //  motor4 at slot2
double motorPos1 = 0;   //萬象輪馬達1預設值
double motorPos2 = 0;   //萬象輪馬達2預設值
double motorPos3 = 0;   //萬象輪馬達3預設值
double motorPos4 = 0;   //萬象輪馬達4預設值

MePort servo_port(PORT_3);    // servo at port3
Servo myservo1;  // create servo object to control a servo
Servo myservo2;  // create servo object to control another servo
int16_t servo1pin =  servo_port.pin1();   //attaches the servo on PORT_3 SLOT1 to the servo object
int16_t servo2pin =  servo_port.pin2();   //attaches the servo on PORT_3 SLOT2 to the servo object
int servo_position = 93; // 托盤位置預設值
int servo_target = 93;   // 托盤目標位置預設值
int servo_move = 5;      // 托盤每次移動預設值


MeUltrasonicSensor leftFD(PORT_4);    //超音波感測器port設定
MeUltrasonicSensor rightFD(PORT_6);   //超音波感測器port設定
double leftFrontDis = 0;      //  左前方超音波感測器預設值
double rightFrontDis = 0;     //  右前方超音波感測器預設值
double aveDis = 0;            //  左右前超音波平均距離預設值


MeUltrasonicSensor leftD(PORT_7);   //超音波感測器port設定
MeUltrasonicSensor rightD(PORT_8);  //超音波感測器port設定
int leftDis = 0;    //左邊超音波感測器數值
int rightDis = 0;   //右邊超音波感測器數值


MeStepper stepper1(PORT_9);  //升降伺服馬達port9
MeStepper stepper2(PORT_10); //升降伺服馬達port10

MeBluetooth BT(PORT_5);    //藍芽模組port5
unsigned char table[8] = {0};  //儲存藍芽送過來的8個指令碼。

//開頭設定
void setup()
{
  Serial.begin(115200);

  motor1.begin();  // motor1 begin
  motor2.begin();  // motor2 begin
  motor3.begin();  // motor3 begin
  motor4.begin();  // motor4 begin

  motor1.setCurrentPosition(0);  //設定萬象輪馬達1位置為0
  motor2.setCurrentPosition(0);  //設定萬象輪馬達2位置為0
  motor3.setCurrentPosition(0);  //設定萬象輪馬達3位置為0
  motor4.setCurrentPosition(0);  //設定萬象輪馬達4位置為0

  myservo1.attach(servo1pin);  // attaches the servo on servopin1
  myservo2.attach(servo2pin);  // attaches the servo on servopin2

  stepper1.setMaxSpeed(2500);     //升降馬達1最大速度
  stepper1.setAcceleration(20000);//升降馬達1加速度
  stepper2.setMaxSpeed(2500);     //升降馬達2最大速度
  stepper2.setAcceleration(20000);//升降馬達2加速度

  BT.begin(115200); //藍芽鮑率
}
//不斷執行
void loop()
{
  leftFrontDis = leftFD.distanceCm(500);  //左前超音波感測器距離
  rightFrontDis = rightFD.distanceCm(500);//右前超音波感測器距離
  aveDis = (leftFrontDis + rightFrontDis) / 2; // 左右前方超音波感測器距離平均值

  int readdata = 0, i = 0, count = 0;

  if (BT.available()) //藍芽接收訊號
  {
    while ((readdata = BT.read()) != (int) - 1) //依序讀取紀錄每筆資料
    {
      table[count] = readdata;
      count++;
      delay(1);
    }
    parseJoystick((unsigned char*)table);  // 將收到的資料整個傳至parseJoystick
  }
  else
  {
    delay(100);
  }
}

const int MOVE = 1;       //定義MOVE為數字1
const int TURN = 2;       //定義TURN為數字2
const int SERVO = 3;      //定義SERVO為數字3
const int STEPPER = 4;    //定義STEPPER為數字4
const int HORIZONTAL = 5; //定義HORIZONTAL為數字5
const int FRONTULTRA = 6; //定義FORNTULTRA為數字6
const int ELEVATOR = 7;   //定義ELEVATOR為數字7

void parseJoystick(unsigned char *buf)
{
  //限制若第一筆資料不為128則不能進入此函式
  if (buf[0] == 128) {
    /*
       table[2]
       MOVE = 1
       TURN = 2
       SERVO = 3
       STEPPER = 4
       HORIZONTAL = 5
       FRONTULTRA = 6
       ELEVATOR = 7
    */
    /*
       table[3]
       負數 = 0
       正數 = 1
    */

    if (table[2] == MOVE)  //table[2] = 1 代表移動
    {
      if (table[6] == 0) //table[6] 代表是否要避障
      {
        if (table[3] == 0) MoveCM(-table[5], true); // table[3] = 0 代表 table[5] 為負數，table[5]代表移動公分
        if (table[3] == 1) MoveCM(table[5], true);  // table[3] = 1 代表 table[5] 為正數，table[5]代表移動公分
      }
      else
      {
        if (table[3] == 0) MoveCM(-table[5], false); // table[3] = 0 代表 table[5] 為負數，table[5]代表移動公分
        if (table[3] == 1) MoveCM(table[5], false);  // table[3] = 1 代表 table[5] 為正數，table[5]代表移動公分
      }
    }
    else if (table[2] == TURN) //table[2] = 2 代表旋轉
    {
      if (table[3] == 0)RotateAngle(-table[5]); // table[3] = 0 代表 table[5] 為負數，table[5]代表轉動角度
      if (table[3] == 1)RotateAngle(table[5]);  // table[3] = 1 代表 table[5] 為正數，table[5]代表轉動角度
    }
    else if (table[2] == SERVO) // table[2] = 3 代表托盤轉動
    {
      ServoMove(table[5]); // table[5]代表轉動角度
    }
    else if (table[2] == STEPPER) // table[2] = 4 代表升降步進馬達移動
    {
      if (table[3] == 0)StepperMoveCM(-table[5]); // table[3] = 0 代表 table[5] 為負數，table[5]代表移動公分
      if (table[3] == 1)StepperMoveCM(table[5]);  // table[3] = 1 代表 table[5] 為正數，table[5]代表移動公分
    }
    else if (table[2] == HORIZONTAL) // table[2] = 5 代表水平移動
    {
      if (table[3] == 0)Horizontal(-table[5]); // table[3] = 0 代表 table[5] 為負數，table[5]代表移動公分
      if (table[3] == 1)Horizontal(table[5]);  // table[3] = 1 代表 table[5] 為正數，table[5]代表移動公分
    }
    else if (table[2] == FRONTULTRA) // table[2] = 6 代表前方超音波算距離移動
    {
      FrontUltra(table[5]); // table[5]代表距離公分
    }
    else if (table[2] == ELEVATOR) // table[2] = 7 代表進電梯
    {
      Elevator(table[5]); // table[5]代表前進公分
    }
  }
}

// 前後移動
//實際轉 360度 = 30CM
//20170803測 360度 = 31.128CM
void MoveCM(double CM, bool avoid)
{
  double rotate = CM * 360 / 31.128;  // 將公分轉換成馬達應旋轉度數

  motor1.setCurrentPosition(0);   // 馬達1位置設定為0
  motor2.setCurrentPosition(0);   // 馬達2位置設定為0
  motor3.setCurrentPosition(0);   // 馬達3位置設定為0
  motor4.setCurrentPosition(0);   // 馬達4位置設定為0

  motor1.moveTo(-rotate, 25);   //馬達1位置轉至-rotate , 速度為25
  motor2.moveTo(rotate, 25);    //馬達2位置轉至 rotate , 速度為25
  motor3.moveTo(rotate, 25);    //馬達3位置轉至 rotate , 速度為25
  motor4.moveTo(-rotate, 25);   //馬達4位置轉至-rotate , 速度為25

  //迴圈(若其中一個馬達轉至目標度數則離開)
  while (!motor1.isTarPosReached() ||
         !motor2.isTarPosReached() ||
         !motor3.isTarPosReached() ||
         !motor4.isTarPosReached())
  {
    leftDis = leftD.distanceCm(500);        //左邊超音波感測距離
    rightDis = rightD.distanceCm(500);      //右邊超音波感測距離
    leftFrontDis = leftFD.distanceCm(500);  //左前超音波感測器距離
    rightFrontDis = rightFD.distanceCm(500);//右前超音波感測器距離

    if (avoid) //是否要避障
    {
      //左右太近避障
      if (leftDis <= 15) //左邊距離太近向右平移
      {
        KeepPos();
        motor1.move(-50, 25);  // 馬達1轉動-50度, 速度25
        motor2.move(-50, 25);  // 馬達2轉動-50度, 速度25
        motor3.move(50, 25);   // 馬達3轉動 50度, 速度25
        motor4.move(50, 25);   // 馬達4轉動 50度, 速度25
        delay(476); // 等待0.476秒 (計算出轉動50度所需時間)
        SetPos(rotate);
      }
      else if (rightDis <= 15) //右邊距離太近向左平移
      {
        KeepPos();
        motor1.move(50, 25);   // 馬達1轉動 50度, 速度25
        motor2.move(50, 25);   // 馬達2轉動 50度, 速度25
        motor3.move(-50, 25);  // 馬達3轉動-50度, 速度25
        motor4.move(-50, 25);  // 馬達4轉動-50度, 速度25
        delay(476); // 等待0.476秒 (計算出轉動50度所需時間)
        SetPos(rotate);
      }
      else if (rightDis <= 15 && leftDis <= 15 ) //左右距離都很近則停止移動
      {
        KeepPos();
        motor1.runSpeed(0);  // 馬達1轉動速度設定為0
        motor2.runSpeed(0);  // 馬達2轉動速度設定為0
        motor3.runSpeed(0);  // 馬達3轉動速度設定為0
        motor4.runSpeed(0);  // 馬達4轉動速度設定為0
        delay(1000);  // 等待1秒
        SetPos(rotate);
      }

      //前方距離太近避障
      if (leftFrontDis <= 20 || rightFrontDis <= 20)
      {
        KeepPos();
        motor1.runSpeed(0);  // 馬達1轉動速度設定為0
        motor2.runSpeed(0);  // 馬達2轉動速度設定為0
        motor3.runSpeed(0);  // 馬達3轉動速度設定為0
        motor4.runSpeed(0);  // 馬達4轉動速度設定為0
        delay(1000);  // 等待1秒
        SetPos(rotate);
      }
    }
  }
  BT.print("O"); // 完成命令傳送0給樹梅派
}
//紀錄各馬達已轉角度
void KeepPos()
{
  motorPos1 = motor1.getCurrentPosition();  //紀錄馬達1現在角度
  motorPos2 = motor2.getCurrentPosition();  //紀錄馬達2現在角度
  motorPos3 = motor3.getCurrentPosition();  //紀錄馬達3現在角度
  motorPos4 = motor4.getCurrentPosition();  //紀錄馬達4現在角度
}
//設定各馬達角度為記錄已轉角度
void SetPos(double rotate)
{
  motor1.setCurrentPosition(motorPos1);  //設定馬達1為記錄角度
  motor2.setCurrentPosition(motorPos2);  //設定馬達2為記錄角度
  motor3.setCurrentPosition(motorPos3);  //設定馬達3為記錄角度
  motor4.setCurrentPosition(motorPos4);  //設定馬達4為記錄角度

  motor1.moveTo(-rotate, 25);   //馬達1繼續轉動至目標角度
  motor2.moveTo(rotate, 25);    //馬達2繼續轉動至目標角度
  motor3.moveTo(rotate, 25);    //馬達3繼續轉動至目標角度
  motor4.moveTo(-rotate, 25);   //馬達4繼續轉動至目標角度
}
// 左右旋轉
void RotateAngle(double Angle)
{
  double rotate = Angle * 820 / 90;  // 將旋轉角度轉換成馬達應旋轉度數
  motor1.move(-rotate, 25);   //馬達1轉動-rotate度 , 速度為25
  motor2.move(-rotate, 25);   //馬達2轉動-rotate度 , 速度為25
  motor3.move(-rotate, 25);   //馬達3轉動-rotate度 , 速度為25
  motor4.move(-rotate, 25);   //馬達4轉動-rotate度 , 速度為25

  delay((rotate < 0 ? -rotate : rotate) / 820 * 90 * 0.078 * 1000); // 等待轉動rotate度所需時間
  BT.print("O"); // 完成命令傳送0給樹梅派
}
//轉動托盤(伺服馬達)至目標角度
void ServoMove(int servo_target)
{
  (servo_target >= 170 ) ? servo_target = 170 : (servo_target <= 0 ) ? servo_target = 0 : servo_target;  //若角度大於170則設定成170，若小於0則設定成0
  servo_position = myservo2.read();  //讀取當前伺服馬達角度

  //迴圈(若伺服馬達角度等於目標角度則離開)
  while (servo_position != servo_target)
  {
    if ((servo_target - servo_position) >= 0) //目標角度是否大於現在角度 (正方向)
    {
      //若差距大於5則每次移動角度5個單位，若小於5則直接移動至目標角度 (避免轉動太快，每次移動設定角度)
      ((servo_target - servo_position) >= 5) ? myservo2.write(servo_position + servo_move) : myservo2.write(servo_target);
    }
    else  // 目標角度小於現在角度(負方向)
    {
      //若差距大於5則每次移動角度5個單位，若小於5則直接移動至目標角度 (避免轉動太快，每次移動設定角度)
      ((servo_target - servo_position) <= -5) ? myservo2.write(servo_position - servo_move) : myservo2.write(servo_target);
    }
    servo_position = myservo2.read(); //紀錄現在角度
    delay(100); //等待0.1秒
  }
  BT.print("O"); // 完成命令傳送0給樹梅派
}
//升降步進馬達移動
double stp = 1000 / 1.2; // stepper 大約的每公分數值
void StepperMoveCM(double CM)
{
  while (stepper1.distanceToGo() != 0) // 若目標距離不為0則STEPPER移動
  {
    stepper1.run(); // 馬達1移動
    stepper2.run(); // 馬達2移動
  }

  if (CM > 39) //若目標超過39公分則先移動39公分 (超過39公分會溢位 40 * 1000 / 1.2 = 33333 > 32768)
  {
    stepper1.move(39 * stp); //步進馬達1移動39公分
    stepper2.move(-39 * stp);//步進馬達2移動39公分
    StepperMoveCM(CM - 39);  // 呼叫自己繼續移動
  }
  else if (CM < -39) //若目標超過39公分則先移動39公分 (超過39公分會溢位 40 * 1000 / 1.2 = 33333 > 32768)
  {
    stepper1.move(-39 * stp);//步進馬達1移動39公分
    stepper2.move(39 * stp); //步進馬達2移動39公分
    StepperMoveCM(CM + 39); // 呼叫自己繼續移動
  }
  else if (CM == 0) {
    BT.print("O");  // 若數值為0代表完成命令傳送0給樹梅派
  }
  else // 若沒超過39公分則直接移動
  {
    stepper1.move(CM * stp); //步進馬達1移動指定公分
    stepper2.move(-CM * stp);//步進馬達2移動指定公分
    StepperMoveCM(CM - CM);  //呼叫自己數值為0
  }
}
//水平左右移動
void Horizontal(double CM) // Positive + Negative = PONE
{
  // 13.333 = rotate per cm
  double rotate = 13.333 * ((CM < 0) ? (CM - 0.5) : CM);  // 將公分轉換成馬達應旋轉度數

  motor1.setCurrentPosition(0);   // 馬達1位置設定為0
  motor2.setCurrentPosition(0);   // 馬達2位置設定為0
  motor3.setCurrentPosition(0);   // 馬達3位置設定為0
  motor4.setCurrentPosition(0);   // 馬達4位置設定為0

  motor1.moveTo(-rotate, 50);   //馬達1位置轉至-rotate , 速度為50
  motor2.moveTo(-rotate, 50);   //馬達2位置轉至-rotate , 速度為50
  motor3.moveTo(rotate, 50);    //馬達3位置轉至rotate , 速度為50
  motor4.moveTo(rotate, 50);    //馬達4位置轉至rotate , 速度為50

  delay((CM < 0 ?  -CM : CM) * 0.07 * 1000 ); // 等待轉動rotate度所需時間
  BT.print("O"); // 完成命令傳送0給樹梅派
}
//前方超音波判斷距離並移動
void FrontUltra(double CM)
{
  //若CM為0則只與牆壁對齊
  if (CM == 0) {
    Aligned();
    BT.print("O"); // 完成命令傳送0給樹梅派
  }
  else // CM不為0
  {
    //無限迴圈
    while (true)
    {
      Aligned();
      leftFrontDis = leftFD.distanceCm(500);  //左前超音波感測距距離
      rightFrontDis = rightFD.distanceCm(500);//右前超音波感測器距離
      if ((leftFrontDis - CM) >= 1 || (rightFrontDis - CM) >= 1) // 超音波距離與目標距離大於1公分則前進
      {
        motor1.move(-15, 15);   //馬達1轉動-15度 , 速度為15
        motor2.move(15, 15);    //馬達2轉動 15度 , 速度為15
        motor3.move(15, 15);    //馬達3轉動 15度 , 速度為15
        motor4.move(-15, 15);   //馬達4轉動-15度 , 速度為15
      }
      else if ((leftFrontDis - CM ) <= -1 || (rightFrontDis - CM) <= -1) //超音波距離與目標距離小於1公分則後退
      {
        motor1.move(15, 15);    //馬達1轉動 15度 , 速度為15
        motor2.move(-15, 15);   //馬達2轉動-15度 , 速度為15
        motor3.move(-15, 15);   //馬達3轉動-15度 , 速度為15
        motor4.move(15, 15);    //馬達4轉動 15度 , 速度為15
      }
      else
      {
        Aligned();
        BT.print("O"); // 完成命令傳送0給樹梅派
        break;
      }
    }
  }
}
// 與牆壁對齊
void Aligned()
{
  //無限迴圈
  while (true)
  {
    leftFrontDis = leftFD.distanceCm(500);  //左前超音波感測距距離
    rightFrontDis = rightFD.distanceCm(500);//右前超音波感測器距離

    if ((rightFrontDis - leftFrontDis) <= 100 && (rightFrontDis - leftFrontDis) >= -100) //若兩個超音波距離沒有相差1公尺以上
    {
      if (rightFrontDis <= 1 || leftFrontDis <= 1) {} // 數值小於等於1，判定為雜訊，不做動作
      else if ((rightFrontDis - leftFrontDis) > 1) //右邊數值較大，左轉
      {
        motor1.move(15, 15);    //馬達1轉動 15度 , 速度為15
        motor2.move(15, 15);    //馬達2轉動 15度 , 速度為15
        motor3.move(15, 15);    //馬達3轉動 15度 , 速度為15
        motor4.move(15, 15);    //馬達4轉動 15度 , 速度為15
      }
      else if ((leftFrontDis - rightFrontDis) > 1) // 左邊數值較大，右轉
      {
        motor1.move(-15, 15);    //馬達1轉動-15度 , 速度為15
        motor2.move(-15, 15);    //馬達2轉動-15度 , 速度為15
        motor3.move(-15, 15);    //馬達3轉動-15度 , 速度為15
        motor4.move(-15, 15);    //馬達4轉動-15度 , 速度為15
      }
      else // 兩邊誤差小於1則離開迴圈
      {
        break;
      }
    }
    else //相差超過1公尺則直接離開迴圈
    {
      break;
    }
  }
}
//電梯門打開，移動進入電梯
void Elevator(double CM)
{
  //進入此函式前有紀錄平均距離，若新的距離與平均距離相差1公尺以上，代表門打開則離開迴圈
  while ((leftFrontDis - aveDis) <= 100 && (rightFrontDis - aveDis) <= 100)
  {
    leftFrontDis = leftFD.distanceCm(500);  //左前超音波感測距距離
    rightFrontDis = rightFD.distanceCm(500);//右前超音波感測器距離
  }
  MoveCM(CM, false); // 移動公分不避障
  Aligned(); //對齊
}

