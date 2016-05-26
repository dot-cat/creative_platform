/*
Materials are took from "Exploring Arduino"
*/

//LCD text with incrementing number
//Include the library code:

#include <LiquidCrystal.h>
#include <math.h>

//Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);


//Number of Light Sensors on analog pins
const uint8_t l_EntranceToOffice = 0; //  Entrance to office
const uint8_t l_EntranceToBedroom = 1; //  Entrance to bedroom
const uint8_t l_ExitFromOffice = 2; //  Exit from office
const uint8_t l_ExitFromBedroom = 3; //  Exit from bedroom
//  Предназначения этих аналоговых входов пока что не определены
const uint8_t LIGHT4 = 4;
const uint8_t LIGHT5 = 5;


//  variables to hold current analog reading
uint8_t v_ToOffice = 0; 
uint8_t v_ToBedroom = 0;
uint8_t v_FromOffice = 0;
uint8_t v_FromBedroom = 0;
uint8_t value4 = 0;
uint8_t value5 = 0;
//  variables to hold last analog reading
uint8_t v_old_ToOffice = 0;
uint8_t v_old_ToBedroom = 0;
uint8_t v_old_FromOffice = 0;
uint8_t v_old_FromBedroom = 0;
uint8_t old_value4 = 0;
uint8_t old_value5 = 0;

//  Is sending flag - blocks repeating sending, 
//  when data is already sent and analog value is still < THRESHOLD
boolean isSending0 = false;
boolean isSending1 = false;
boolean isSending2 = false;
boolean isSending3 = false;
boolean isSending4 = false;
boolean isSending5 = false;

typedef unsigned short int USHORT;
const uint8_t DIFFERENCE = 30;
const uint8_t THRESHOLD = 500;

//  Buffer for displaying data on lcd screen
char buf[4];

/*--------------------------------------------------------------------*/

// Variables for buttons


//  Buttons ports
const uint8_t button[6] = {
  8, 9, 10, 11, 12, 13
};

//  Current button states
boolean current_state[6] = {
  LOW, LOW, LOW, LOW, LOW, LOW
};

//  Last button states
boolean last_state[6] = {
  LOW, LOW, LOW, LOW, LOW, LOW
};

//  Strings to send
char buttonString[][6] = {
  "B1",
  "B2",
  "B3",
  "B4",
  "B5",
  "B6"
};


/*--------------------------------------------------------------------------*/

//  Function that defines how many '0' print before integer in 4-digit representation
char & GetBufByValue(const int & _val)
{
  if (_val < 1000 && _val > 99) {
    sprintf(buf, "0%d", _val);
  } else if (_val < 100 && _val > 9){
    sprintf(buf, "00%d", _val);
  } else if (_val < 10) {
    sprintf(buf, "000%d", _val);
  }
  return *buf;
}

//  Function to display raw analog 8-bit input data
//  by position for 4-digit places
void PrintByIndex(int _place, int _value) {
  lcd.setCursor(_place * 5 % 15, (_place) / 3);
  *buf = GetBufByValue(_value);
  lcd.print(buf);
}

//  Overloaded function to display 4-character string by position
void PrintByIndex(int _place, const char * _value) {
  lcd.setCursor(_place * 5 % 15, (_place) / 3);
  lcd.print(_value);
}


///////////////////////////////////////////////////////////


void setup()
{
  Serial.begin(9600);
  for (USHORT i = 0; i < 6; ++i) {
    pinMode(button[i], INPUT);
  }
  //Set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  //  Set lcd to default values
  lcd.setCursor(0,0);
  lcd.print("---- ---- ----  ");
  lcd.setCursor(0,1);
  lcd.print("---- ---- ----  ");

  
}

boolean debounce(boolean _current, boolean _last, uint8_t _port) {
  boolean current = digitalRead(_port); //Read the button state
  if (_last != _current) {
    delay(5); //wait 5ms                          
    _current = digitalRead(_port); //read it again
  }
  return current; //return the current value
}

void loop()
{
  //  Опрос кнопок с использованием антидребезговой системы
  for (USHORT i = 0; i < 6; ++i) {
    current_state[i] = debounce(current_state[i], last_state[i], button[i]);
    if (last_state[i] == LOW && current_state[i] == HIGH)
      Serial.print(buttonString[i]);
  }
  
  /*---------------------------------------------------------------------------------------*/
  // Реализация опроса фотосенсоров

  v_ToOffice = analogRead(l_EntranceToOffice);  
  v_ToBedroom = analogRead(l_EntranceToBedroom);
  v_FromOffice = analogRead(l_ExitFromOffice);
  v_FromBedroom = analogRead(l_ExitFromBedroom);
  value4 = analogRead(LIGHT4);
  value5 = analogRead(LIGHT5);

  //  Обработка полученных данных с фотосенсоров
  if (abs(v_ToOffice - v_old_ToOffice) > DIFFERENCE) {
    if (v_ToOffice < THRESHOLD) {
      if (!isSending0) {
        //  Sending string "S0_1" to Raspberry via UART
        //  "S0_1" means that sensor behind the office detected movement (1 like "On")
        Serial.print("S0_1");
        //  Set sending flag to true to omit repeating sendings of the same string
        isSending0 = true;
        //  Print sending value on the lcd screen
        PrintByIndex(0, "S0_1");
      }
    } else {
      //  If value of analog is more than THRESHOLD
      //  and detected state was sent - then send "S0_0" once.
      if (isSending0) {
        Serial.print("S0_0");
        PrintByIndex(0, "S0_0");
        isSending0 = false;
      }
    }
  }
  if (abs(v_ToBedroom - v_old_ToBedroom) > DIFFERENCE) {
    if (v_ToBedroom < THRESHOLD) {
      if (!isSending1) {
        Serial.print("S1_1");
        isSending1 = true;
        //  Print '1' on the lcd display in place 1 if detection is seen
        PrintByIndex(1, "S1_1");
      }
    } else {
      if (isSending1) {
        Serial.print("S1_0");
        PrintByIndex(1, "S1_0");
        isSending1 = false;
      }
    }
  }
  if (abs(v_FromOffice - v_old_FromOffice) > DIFFERENCE) {
    if (v_FromOffice < THRESHOLD) {
      if (!isSending2) {
        Serial.print("S2_1");
        isSending2 = true;
        PrintByIndex(2, "S2_1");
      }
      
    } else {
      Serial.print("S2_0");
      PrintByIndex(2, "S2_0");
      isSending2 = false;
    }
  }
  if (abs(v_FromBedroom - v_old_FromBedroom) > DIFFERENCE) {
    if (v_FromBedroom < THRESHOLD) {
      if (!isSending3) {
        Serial.print("S3_1");
        isSending3 = true;
        PrintByIndex(3, "S3_1");
      }
    } else {
      Serial.print("S3_0");
      PrintByIndex(3, "S3_0");
      isSending3 = false;
    }
  }
  if (abs(value4 - old_value4) > DIFFERENCE) {
    if (value4 < THRESHOLD) {
      if (!isSending3) {
        Serial.print("S4_1");
        isSending4 = true;
        PrintByIndex(4, "S4_1");
      }
    } else {
      Serial.print("S4_0");
      PrintByIndex(4, "S4_0");
      isSending4 = false;
    }
  }
  if (abs(value5 - old_value5) > DIFFERENCE) {
    if (value5 < THRESHOLD) {
      Serial.print("S5_1");
       isSending5 = true;
       PrintByIndex(5, "S5_1");
    } else {
      Serial.print("S5_0");
      PrintByIndex(5, "S5_0");
      isSending5 = false;
    }
  }
  
  v_ToOffice = v_old_ToOffice;
  v_old_ToBedroom = v_ToBedroom;
  v_old_FromOffice = v_FromOffice;
  v_old_FromBedroom = v_FromBedroom;
  old_value4 = value4;
  old_value5 = value5;

  //  Ask sensors every 100 miliseconds
  delay(100);
}
