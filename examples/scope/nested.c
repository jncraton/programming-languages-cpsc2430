#include <stdio.h>

int main(void) {
  char* level = "Grandparent";
  {
    printf("%s\n", level);
    {
      char* level = "Local";

      printf("%s\n", level);
    }
  }
}
