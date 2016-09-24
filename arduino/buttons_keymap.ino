
unsigned const int SizeColumns = 3;
unsigned const int SizeRows = 3;



const char * noKey {"no"};
byte columns[SizeColumns] = { 2, 3, 4 }; //fix name of the pins
byte rows[SizeRows] = { 5, 6, 7 };//fix name of the pins

//  Antibounce system variables
unsigned int lastReadTime;
unsigned int bounceTime = 40;//ms

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


//-------------------------------------------------------------------



void setup(){
  
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


void loop() {
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
  ////////////////////////////////////////////////////////////////////
  
  for (short int c = 0; c < SizeColumns; ++c) {
    for (short int r = 0; r < SizeRows; ++r) {
      
    }
  }
  
  
}
