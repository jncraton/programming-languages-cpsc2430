/* `static` example in C */

#include <stdio.h>

void count() {
  int value = 0; // Try with `static`
  printf("%d\n", value++);
}

int main(void) {
  for (int i = 0; i<10; i++) { count(); }
}