
float analogValA = 301.0; //Reading with loadA on the load cell
float loadA = 0.0; //  (Kg,lbs..) //Known load placed on the load cell
float analogValB = 302.0; // Reading with loadB on the load cell
float loadB = 80.0; //  (Kg,lbs..) // Known load placed on the load cell


int time_step = 25; // reading every .025.s
long time = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // Raw analog to digital conversion
  int sensorValue = analogRead(A0); //If you wanted more sensors in read more values uncomment analog readers below
  /*
  int sensorValue2 = analogRead(A1); // -z direction
  int sensorValue3 = analogRead(A2); // +x direction
  int sensorValue4 = analogRead(A3); // -x direction
  int sensorValue5 = analogRead(A4); // +y direction
  int sensorValue6 = analogRead(A5); // -y direction
  */
  // Convert sensorValue into digital voltage

  //If we were actually reading data from 3 dimensions
  /*
  float avgZ = (sensorValue + sensorValue2)/2;
  float avgX = (sensorValue3 + sensorValue4)/2;
  float avgY = (sensorValue5 + sensorValue6)/2;
  
  float zVolt = avgZ *(5.0 /1023.0);
  float xVolt = avgX * (5.0 / 1023.0);
  float yVolt = avgY * (5.0 / 1023.0);
  float averageZVolt = 0.99*averageZVolt + .01*zVolt;
  float averageXVolt = 0.99*averageXVolt + .01*xVolt;
  float averageYVolt = 0.99*averageYVolt + .01*yVolt;
  */
  
  // Only reading data from 1 dimension so we use this currently
  float voltage = sensorValue * (5.0 / 1023.0);
  float averageVoltage = 0.99*averageVoltage + .01*voltage;

  
  

  //Check to see if it is time to print again.
  if(millis() > time + time_step){
    // For 1 dimension
    float load = analogToLoad(averageVoltage);

    // For 3 dimensions
    /*
    float loadZ = analogToLoad(averageZVolt);
    float loadX = analogToLoad(averageXVolt);
    float loadY = analogToLoad(averageYVolt);
    */
    
    // Print the current load (one dimension)
    Serial.print(load);Serial.print(",");Serial.println(time);

    /*
    //Print the current load (3 dimension)
    Serial.print(loadX);
    Serial.print(",");
    Serial.print(loadY);
    Serial.print(",");
    Serial.print(loadZ);
    Serial.print(",");
    Serial.println(time);
    */
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

