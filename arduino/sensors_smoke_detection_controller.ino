
/*

  Value Variable  |  Sending string
                  |
      s1Val       |  "S2_*"
      s2Val       |  "S0_*"
      s3Val       |  "GAS_1" - NEW (Smoke Sensor)
      s4Val       |  "S3_*"
      s5Val       |  "S4_*" - NEW (From living room to bedroom)
      s6Val       |  "S1_*"


*/

/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/

/*     VARIABLES FOR SMOKE DETECTORS    */

int s3SmokeSensor = A2; 

uint8_t ssVal = 0;
uint8_t ssOldVal = 0;

boolean isSmokeSending = false;



/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/

/*  VARIABLES FOR IR DETECTORS */


int s1CabinetToLRoom = A0;  // From CABINET -> To LIVING ROOM. Free - 500-700; Detection - 50-150.
int s2LRoomToCabinet = A1;  // From LIVING ROOM -> To CABINET. Free - 500-550; Detection - 100-150.
//  int s3 = A2; 
int s4BedroomToLRoom = A3;  // From BEDROOM -> To LIVING ROOM. Free - 130-150; Detection - 60-100.
int s5LRoomToCorridor = A4; // From LIVING ROOM -> To CORRIDOR. 
int s6LRoomToBedroom = A5; // From LIVING ROOM -> To BEDROOM. Free - 650-750; Detection - 100-200.

const uint8_t s1Threshold = 250;
const uint8_t s2Threshold = 250;
const uint8_t s3Threshold = 100; // ?
const uint8_t s4Threshold = 100; // ?
const uint8_t s5Threshold = 150;
const uint8_t s6Threshold = 200;

uint8_t s1Val = 0;
uint8_t s2Val = 0;
//  uint8_t s3Val = 0;
uint8_t s4Val = 0;
uint8_t s5Val = 0;
uint8_t s6Val = 0;

uint8_t s1OldVal = 0;
uint8_t s2OldVal = 0;
//  uint8_t s3OldVal = 0;
uint8_t s4OldVal = 0;
uint8_t s5OldVal = 0;
uint8_t s6OldVal = 0;

//  Is sending flag - blocks repeating sending, 
//  when data is already sent and analog value is still < THRESHOLD
boolean isSending1 = false;
boolean isSending2 = false;
//  boolean isSending3 = false;
boolean isSending4 = false;
boolean isSending5 = false;
boolean isSending6 = false;


const uint8_t DIFFERENCE = 50;

/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/
/* --------------------------------------------------------------------------------------------------------------------*/

/*  VARIABLE FOR BUTTONS */

unsigned const int SizeColumns = 3;
unsigned const int SizeRows = 3;



const char * noKey {"no"};
byte columns[SizeColumns] = { 2, 3, 4 }; //fix name of the pins
byte rows[SizeRows] = { 5, 6, 7 };//fix name of the pins

//  Antibounce system variables
unsigned int lastReadTime;
unsigned int bounceTime = 400;//ms

const unsigned short int delay_key_press = 50;

//-------------------------------------------------------------------

//  Messages to send
char keymap[][SizeRows][SizeColumns] = {
  { "B1", "B2", "B3" },
  { "B4", "B5", "B6" },
  { "B7", "B8", "B9" }
};

//  Current button states
boolean current_state[SizeRows][SizeColumns] = {
  { LOW, LOW, LOW },
  { LOW, LOW, LOW },
  { LOW, LOW, LOW }
};

//  Last button states
boolean last_state[SizeRows][SizeColumns] = {
  { LOW, LOW, LOW },
  { LOW, LOW, LOW },
  { LOW, LOW, LOW } 
};

/*--------------------------------------------------------------------------------------*/

void setup() {
  Serial.begin(9600);
  
  lastReadTime = millis();
  
  for(int j = 0; j < SizeColumns; j++){
    pinMode(columns[j],OUTPUT); // Setting pins for input
    //digitalWrite(columns[j], LOW);
  }
  
  for (int i = 0; i < SizeRows; i++){
    pinMode(rows[i], INPUT); // Setting pins for input
    digitalWrite(rows[i], HIGH);
  }
}



void loop () {
  
  delay(50);
  
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  
  /*        BUTTONS INTERFACE   */
  
  
  if ( (millis() - lastReadTime) > bounceTime ) {
    
    //Если время с начала работы программы минус
    //последнее считаннове время больше 30мс(bounceTime)
    
    for(int c = 0; c < SizeColumns; c++)
    {
      //pinMode(columns[c], OUTPUT);
      digitalWrite(columns[c], LOW);
      //опрашиваем горизонтальные дорожки 
      for(int r = 0; r < SizeRows; r++)
      {
        if(digitalRead(rows[r]) == LOW)
        {
          if (current_state[r][c] == LOW) {
            Serial.println(keymap[r][c]);
          }
          current_state[r][c] = HIGH;
          
          //если у нас на горизонтальной дорожке
          //будет значение 1 то запоминаем позиию
          //foundKey = keymap[r][c];
          //strcpy(foundKey, keymap[r][c]);
          // И отправляем её в Serial
          //Serial.println(foundKey);
        }  else {
          current_state[r][c] = LOW;
        }
      }
      
      digitalWrite(columns[c], HIGH);
      //pinMode(columns[c], INPUT);
      
    }
    lastReadTime = millis();
  }
  
  /*     END OF BUTTONS INTERFACE      */
  
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  
  /*     IR DETECTORS        */  
  
  s1Val = analogRead(s1CabinetToLRoom);
  s2Val = analogRead(s2LRoomToCabinet);
  //  s3Val = analogRead(s3);
  s4Val = analogRead(s4BedroomToLRoom);
  s5Val = analogRead(s5LRoomToCorridor);
  s6Val = analogRead(s6LRoomToBedroom);
  
  //  From Cabinet to Living Room
  if (abs(s1Val - s1OldVal) > DIFFERENCE) {
    if (s1Val < s1Threshold) {
      if (!isSending1) {
        Serial.println("S2_1");
        isSending1 = true;
      }
    } else {
      if (isSending1) {
        Serial.println("S2_0");
        isSending1 = false;
      }
    }
  }
  
  //  From Living Room to Cabinet
  if (abs(s2Val - s2OldVal) > DIFFERENCE) {
    if (s2Val < s2Threshold) {
      if (!isSending2) {
        Serial.println("S0_1");
        isSending2 = true;
      }
    } else {
      if (isSending2) {
        Serial.println("S0_0");
        isSending2 = false;
      }
    }
  }
  
  //  From ... (s3)
  //  Watch down at smoke detection
  // ...
  //////////////////////////////////
  
  
  //  From Bedroom to Living Room
  if (abs(s4Val - s4OldVal) > DIFFERENCE) {
    if (s4Val < s4Threshold) {
      if (!isSending4) {
        Serial.println("S3_1");
        isSending4 = true;
      }
    } else {
      if (isSending4) {
        Serial.println("S3_0");
        isSending4 = false;
      }
    }
  }
  
  //  From Living Room to Corridor
  if (abs(s5Val - s5OldVal) > DIFFERENCE) {
    if (s5Val < s5Threshold) {
      if (!isSending5) {
        Serial.println("S4_1");
        isSending5 = true;
      }
    } else {
      if (isSending5) {
        Serial.println("S4_0");
        isSending5 = false;
      }
    }
  }
  
  //  From Living Room to Bedroom
  if (abs(s6Val - s6OldVal) > DIFFERENCE) {
    if (s6Val < s6Threshold) {
      if (!isSending6) {
        Serial.println("S1_1");
        isSending6 = true;
      }
    } else {
      if (isSending6) {
        Serial.println("S1_0");
        isSending6 = false;
      }
    }
  }
  
  s1OldVal = s1Val;
  s2OldVal = s2Val;
  //  s3OldVal = s3Val;
  s4OldVal = s4Val;
  s5OldVal = s5Val;
  s6OldVal = s6Val;
  
  /*      END OF IR DETECTORS      */
  
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  /*--------------------------------------------------------------------------------------------------*/
  
  /*      SMOKE DETECTION          */
  
  ssVal = analogRead(s3SmokeSensor);
  Serial.println(ssVal);
  delay(1000);
  if (ssVal > 90) {
    if (!isSmokeSending) {
      Serial.println("GAS_1");
      isSmokeSending = true;
    }
  } else {
    if (isSmokeSending) {
      Serial.println("GAS_0");
      isSmokeSending = false;
    }
  }
  

  
}
