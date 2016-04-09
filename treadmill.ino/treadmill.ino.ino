
float analogValA = 301.0; //Reading with loadA on the load cell
float loadA = 0.0; //  (Kg,lbs..) //Known load placed on the load cell
float analogValB = 302.0; // Reading with loadB on the load cell
float loadB = 80.0; //  (Kg,lbs..) // Known load placed on the load cell


int time_step = 20 ; // reading every .02.s
long time = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // Raw analog to digital conversion
  int sensorValue = analogRead(A0);
  // Convert sensorValue into digital voltage
  float voltage = sensorValue * (5.0 / 1023.0);
  float averageVoltage = 0.99*averageVoltage + .01*voltage;
  
  

  //Check to see if it is time to print again.
  if(millis() > time + time_step){
    float load = analogToLoad(averageVoltage);

    // Print the current load
    Serial.print(load);Serial.print(",");Serial.println(time);
    time = millis();
  }
}

// Changes the values of   
float analogToLoad(float analogVal){
    float load = mapFloat(analogVal, analogValA, analogValB, loadA, loadB);
    return load;
}

float mapFloat(float x, float in_min, float in_max, float out_min, float out_max){
  return(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

