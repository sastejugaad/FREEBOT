#include <WiFi.h> // Include the WiFi library to connect to the internet
#include <AsyncUDP.h> // Include the AsyncUDP library to send and receive UDP packets
#include <Arduino.h> // Include the Arduino library to use the Arduino functions
#include "DataParser.h" // Include the DataParser library to parse the CSV data

const char* ssid = "Askey5100-02B0"; // The name of the WiFi network you want to connect to
const char* password = "HHLUnKLKQW"; // The password of the WiFi network

DataParser dataParser; // Create an instance of DataParse

const int udpPort = 12345; // Change this to the desired UDP port

int in1=27; // The pin number for the first input of the left motor driver
int in2=26; // The pin number for the second input of the left motor driver
int ena=14; // The pin number for the enable pin of the left motor driver
int in3=25; // The pin number for the first input of the right motor driver
int in4=33; // The pin number for the second input of the right motor driver
int enb=32; // The pin number for the enable pin of the right motor driver

int DataIndex; // A variable to store the index of the data field
int Speed = 50; // A variable to store the speed value
int Right_speed = 0; // A variable to store the right motor speed value
int Left_speed = 0; // A variable to store the left motor speed value

AsyncUDP udp; // Create an instance of AsyncUDP

void setup() {
  Serial.begin(115200); // Start the serial communication at 115200 baud rate
  pinMode(in1, OUTPUT); // Set the in1 pin as an output
  pinMode(in2, OUTPUT); // Set the in2 pin as an output
  pinMode(ena, OUTPUT); // Set the ena pin as an output
  pinMode(in3, OUTPUT); // Set the in3 pin as an output
  pinMode(in4, OUTPUT); // Set the in4 pin as an output
  pinMode(enb, OUTPUT); // Set the enb pin as an output
  //analogWriteResolution(8); // 8-bit resolution for analogWrite function
  WiFi.begin(ssid, password); // Connect to the WiFi network using the ssid and password
  
  while (WiFi.status() != WL_CONNECTED) { // Wait until the WiFi connection is established
    delay(1000); // Wait for 1 second
    Serial.println("Connecting to WiFi..."); // Print a message on the serial monitor
  }
  
  Serial.println("Connected to WiFi"); // Print a message on the serial monitor
  
  if(udp.listen(udpPort)) { // Start listening on the UDP port
    Serial.print("UDP Listening on IP: "); // Print a message on the serial monitor
    Serial.println(WiFi.localIP()); // Print the IP address of the device on the serial monitor
    udp.onPacket( [](AsyncUDPPacket packet) { // Define a callback function to handle incoming UDP packets
      // Print the received packet data for verification
      //Serial.print("Received Data"); // Print a message on the serial monitor
      //Serial.println((char*)packet.data()); // Print the packet data as a string on the serial monitor
      // Parse the CSV data into separate command arrays
      String IncomingData = (char*)packet.data(); // Convert the packet data to a string and store it in a variable
      dataParser.parseData(IncomingData, ',');//Pass data and deliminator 

       /*Seprate and print the commands
       for (int i = 0; i < dataParser.getFieldCount(); i++) {
          Serial.print("Field ");
          Serial.print(i);
          Serial.print(": ");
          Serial.println(dataParser.getField(i));
      }*/
        Speed = (dataParser.getField(1)).toInt(); // Convert the second field of the data to an integer and store it in the Speed variable
       Left_speed = Speed; // Set the Left_speed variable to the same value as the Speed variable
       Right_speed = Speed; // Set the Right_speed variable to the same value as the Speed variable

    });
  }
}

void loop() {
  // Your main loop code here
     
  if(dataParser.getField(0) == "f") // If the first field of the data is "f"
 {
  forward(Left_speed, Right_speed); // Call the forward function with the Left_speed and Right_speed values
  Serial.println("fwd"); // Print a message on the serial monitor
 }
 if(dataParser.getField(0) == "b") // If the first field of the data is "b"
 {
  backward(Left_speed, Right_speed); // Call the backward function with the Left_speed and Right_speed values
  Serial.println("bck"); // Print a message on the serial monitor
 }
 if(dataParser.getField(0) == "l") // If the first field of the data is "l"
 {
  left(Left_speed, Right_speed); // Call the left function with the Left_speed and Right_speed values
  Serial.println("left"); // Print a message on the serial monitor
 }
 if(dataParser.getField(0) == "r") // If the first field of the data is "r"
 {
  right(Left_speed, Right_speed); // Call the right function with the Left_speed and Right_speed values
  Serial.println("right"); // Print a message on the serial monitor
 }
 if(dataParser.getField(0) == "s") // If the first field of the data is "s"
 {
  Stop(); // Call the Stop function
}
}
void forward(int left_speed, int right_speed) { // Define a function to move the robot forward
  digitalWrite(in1, HIGH); // Set the in1 pin to HIGH
  digitalWrite(in2, LOW); // Set the in2 pin to LOW
  digitalWrite(in3, HIGH); // Set the in3 pin to HIGH
  digitalWrite(in4, LOW); // Set the in4 pin to LOW
  analogWrite(ena, left_speed); // Set the ena pin to the left_speed value
  analogWrite(enb, right_speed); // Set the enb pin to the right_speed value
}
void backward(int left_speed, int right_speed) { // Define a function to move the robot backward
  digitalWrite(in1, LOW); // Set the in1 pin to LOW
  digitalWrite(in2, HIGH); // Set the in2 pin to HIGH
  digitalWrite(in3, LOW); // Set the in3 pin to LOW
  digitalWrite(in4, HIGH); // Set the in4 pin to HIGH
  analogWrite(ena, left_speed); // Set the ena pin to the left_speed value
  analogWrite(enb, right_speed); // Set the enb pin to the right_speed value
}
void left(int left_speed, int right_speed) { // Define a function to turn the robot left
  digitalWrite(in1, HIGH); // Set the in1 pin to HIGH
  digitalWrite(in2, LOW); // Set the in2 pin to LOW
  digitalWrite(in3, LOW); // Set the in3 pin to LOW
  digitalWrite(in4, HIGH); // Set the in4 pin to HIGH
  analogWrite(ena, left_speed); // Set the ena pin to the left_speed value
  analogWrite(enb, right_speed); // Set the enb pin to the right_speed value
  //delay(10); // Wait for 10 milliseconds
}
void right(int left_speed, int right_speed) { // Define a function to turn the robot right
  digitalWrite(in1, LOW); // Set the in1 pin to LOW
  digitalWrite(in2, HIGH); // Set the in2 pin to HIGH
  digitalWrite(in3, HIGH); // Set the in3 pin to HIGH
  digitalWrite(in4, LOW); // Set the in4 pin to LOW
  analogWrite(ena, left_speed); // Set the ena pin to the left_speed value
  analogWrite(enb, right_speed); // Set the enb pin to the right_speed value
}
void motor_speed(int Right_Speed,int Left_Speed) // Define a function to set the motor speed values
{
Left_speed = Left_Speed; // Set the Left_speed variable to the Left_Speed parameter
Right_speed = Right_Speed; // Set the Right_speed variable to the Right_Speed parameter
}
void Stop() { // Define a function to stop the robot
  digitalWrite(in1, LOW); // Set the in1 pin to LOW
  digitalWrite(in2, LOW); // Set the in2 pin to LOW
  digitalWrite(in3, LOW); // Set the in3 pin to LOW
  digitalWrite(in4, LOW); // Set the in4 pin to LOW
  analogWrite(ena, 0); // Set the ena pin to 0
  analogWrite(enb, 0); // Set the enb pin to 0
}
