// This program will likely crash
#include <stdio.h>

int main(void) {
  long int num = 2; // int type is required

  printf((char*)num); // type error (needs format string)
}
