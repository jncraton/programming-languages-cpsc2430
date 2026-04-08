#include <stdio.h>

void increment(int* i) {
  // This will change the callers value
  *i = *i + 1;
}

int main(void) {
  int i = 0;
  increment(&i);
  printf("%d\n", i);
}
