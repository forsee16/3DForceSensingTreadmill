
float analogValA = 0; //Reading with loadA on the load cell
float loadA = 0.0; //  (Kg,lbs..) //Known load placed on the load cell
float analogValB = 4.82; // Reading with loadB on the load cell
float loadB = 200.0; //  (Kg,lbs..) // Known load placed on the load cell


int time_step = 30; // reading every .025.s
long time = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Raw analog to digital conversion
  int sensorValue = analogRead(A0); //If you wanted more sensors in read more values uncomment analog readers below

  // Convert sensorValue into digital voltage

  //If we were actually reading data from 3 dimensions

  
  // Only reading data from 1 dimension so we use this currently
  float voltage = sensorValue * (10.0 / 1023.0);
  float averageVoltage = 0.99*averageVoltage + .01*voltage;

  
  

  //Check to see if it is time to print again.
  if(millis() > time + time_step){
    // For 1 dimension
    float load = analogToLoad(voltage);

    // For 3 dimensions

    
    // Print the current load (one dimension)
    /*Serial.print("Voltage:");*/Serial.println(load);
    //Serial.println(load);//Serial.print(",");Serial.println(time);


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

