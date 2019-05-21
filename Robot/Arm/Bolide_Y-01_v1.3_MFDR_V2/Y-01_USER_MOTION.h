#ifndef Y-01_USER_MOTION_H
#define Y-01_USER_MOTION_H
#include <avr/pgmspace.h>
#define Adjustment_index false
#define Avoidance_index false

//===== User Default Sequence ======
const PROGMEM uint16_t DefaultPose1[] = {18, 263, 759, 372, 650, 467, 555, 373, 650, 512, 512, 339, 684, 269, 754, 633, 390, 512, 512};
const PROGMEM uint16_t DefaultPose2[] = {18, 263, 759, 512, 512, 467, 555, 373, 650, 512, 512, 339, 684, 269, 754, 633, 390, 512, 512};
const PROGMEM transition_t DefaultInitial[] = {{0, 2} , {DefaultPose2, 500}, {DefaultPose1, 400}};
const PROGMEM uint16_t NonePose[] = {18, 263, 759, 372, 650, 467, 555, 373, 650, 512, 512, 339, 684, 269, 754, 633, 390, 512, 512};
const PROGMEM transition_t None[] = {{0, 1} , {NonePose, 400}};

//===== User Define Pose ======
//因火流星有18個馬達，而我們機器人手臂只使用6個馬達，故只需輸入前6個數值即可，後面用不到的數值以1000取代
const PROGMEM uint16_t PlatTake_0[] = {18, 491, 540, 740, 596, 749, 542, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};  //
const PROGMEM uint16_t Push_0[] = {18, 396, 640, 520, 707, 786, 509, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};      // 將手臂舉高(按按鈕動作1)
const PROGMEM uint16_t Push_1[] = {18, 400, 629, 507, 505, 786, 507, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};      // 往下按壓(按按鈕動作2)
const PROGMEM uint16_t Put_0[] = {18, 492, 540, 741, 523, 752, 542, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};       // 手臂前端夾著往左轉
const PROGMEM uint16_t Put_1[] = {18, 487, 543, 739, 521, 631, 643, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};       // 手臂前端鬆開
const PROGMEM uint16_t Put_2[] = {18, 488, 542, 739, 754, 631, 643, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};       // 手臂前端鬆開後往上抬(避免撞到物品)
const PROGMEM uint16_t Relax[] = {18, 489, 535, 797, 809, 785, 508, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};       // 開機時預設休息動作
const PROGMEM uint16_t Take_0[] = {18, 482, 542, 498, 523, 655, 651, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};      // 手臂往前張開
const PROGMEM uint16_t Take_1[] = {18, 489, 542, 499, 522, 749, 540, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};      // 手臂往前閉合

//===== User Define Sequence ======
//這邊是延續上方 User Define Pose 設定的組合動作
//第一格填入從第幾個動作到第幾個 EX {0,2} 代表從index[0]到index[2]
//第二格開始填入上面所設定的動作，以及執行時間( 1000 代表 1秒 )
const PROGMEM transition_t U_init[] = {{0, 2} , {Push_0, 500} , {Relax, 500}};  // 預設動作(開機時動作)
const PROGMEM transition_t Push[] = {{0, 2} , {Push_0, 1000} , {Push_1, 200}};  // 按壓電梯動作
const PROGMEM transition_t Take[] = {{0, 3} , {Push_0, 1000} , {Take_0, 1000} , {Take_1, 1000}};   // 從前方取物動作
const PROGMEM transition_t Put[] = {{0, 4} , {Take_1, 1000} , {Take_0, 1000} , {Push_0, 1000}, {Relax, 1000}};       // 將手上物品放於前方動作
const PROGMEM transition_t PlatPut[] = {{0, 4} , {Put_0, 1000} , {Put_1, 1000} , {Put_2, 1000} , {Relax, 1000}};     // 將手上物品放於托盤動作
const PROGMEM transition_t PlatTake[] = {{0, 5} , {Put_2, 700} , {Put_1, 700} , {Put_0, 1000} , {PlatTake_0, 500}};  // 從托盤上方取物動作
const PROGMEM transition_t RelaxPose[] = {{0, 1} , {Relax, 1000}};  //回休息動作

////==== User Sequence Setup ====////
//這邊是延續上方 User Define Sequence 組合動作，將其設定為動作 1、2、3......
#define ActionNo_1   U_init
#define ActionNo_2   Push
#define ActionNo_3   Take
#define ActionNo_4   Put
#define ActionNo_5   PlatPut
#define ActionNo_6   PlatTake
#define ActionNo_7   RelaxPose

////==== Robot Button Control & Remote Control ====////
//這邊是遙控按鈕控制用的，我們沒有用到
#define RB_1   1
#define RB_2   2
#define RB_3   3
#define RB_4   4
#define RCU_LJU   1
#define RCU_LJD   2
#define RCU_LJL   3
#define RCU_LJR   4
#define RCU_L1   22
#define RCU_L2   17
#define RCU_L3   35
#define RCU_R1   20
#define RCU_R2   21
#define RCU_R3   32
#define RCU_RJU   44
#define RCU_RJD   43
#define RCU_RJL   5
#define RCU_RJR   6

#endif

