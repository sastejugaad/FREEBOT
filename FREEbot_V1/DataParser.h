#ifndef DataParser_h
#define DataParser_h

#include <Arduino.h>

class DataParser {
public:
  DataParser();
  void parseData(const char* data, char delimiter);
  void parseData(const String& data, char delimiter);
  String getField(int index);
  int getFieldCount();
  
private:
  char _delimiter;
  String _fields[50]; // Adjust the array size as needed
  int _fieldCount;
};

#endif
