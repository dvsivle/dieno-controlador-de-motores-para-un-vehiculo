#include <Ticker.h>

#define pin_v1 A0
#define pin_c1 A1
#define pin_v2 A2
#define pin_c2 A3

const int pin_led=13;
const int pin_sp1=9;
const int pin_sp2=10;
String num;

int value_velo1=300;
int value_corr1=300;
int value_velo2=300;


String sp1;
String sp2;


void fnSensores(){
  int velo1;
  int corr1;
  int velo2;

  velo1 = analogRead(pin_v1);
  corr1 = analogRead(pin_c1);
  velo2 = analogRead(pin_v2);


  if (velo1 != value_velo1){
    value_velo1=velo1;
    Serial.println("velo1:" + String(value_velo1));
    Serial.println("corr1:" + String(value_corr1));  
  }  
  if (corr1 != value_corr1){
    value_corr1=corr1;
    Serial.println("corr1:" + String(value_corr1));  
  } 
  
  if (velo2 != value_velo2){
    value_velo2=velo2;
    Serial.println("velo2:" + String(value_velo2));  
  }  
 
}
Ticker ticSensores(fnSensores,500);




void setup()
{
  Serial.begin(9600);
  pinMode(pin_sp1, OUTPUT);
  pinMode(pin_sp2, OUTPUT);
  pinMode(pin_led, OUTPUT);
  analogWrite(pin_sp1,0);
  analogWrite(pin_sp2,126); 
  digitalWrite(pin_led,LOW); 
  
  ticSensores.start();
}


void loop(){
  
  while(Serial.available())
  {
    num = Serial.readString();
    // SP:nn,nn
  }


    int ps = num.indexOf(':');
    String stp= num.substring(0,ps);
    String sp_val= num.substring(ps+1);
    int ps2 = sp_val.indexOf(';');
  
 
    //new
    if (sp_val.startsWith("-")) 
    {
      digitalWrite(pin_led,HIGH); 
      sp1= sp_val.substring(1,ps2);
      sp2= sp_val.substring(ps2+2) ;
      
    }
    else 
    {
      digitalWrite(pin_led,LOW);
      sp1= sp_val.substring(0,ps2);
      sp2= sp_val.substring(ps2+1);
 
    }
    //end
    
    int voltaje1=sp1.toInt();
    int voltaje2=sp2.toInt();

    if (stp.equals("SP"))
    {
      analogWrite(pin_sp1,voltaje1); 
      analogWrite(pin_sp2,voltaje2); 
    }
 
    ticSensores.update();
}
