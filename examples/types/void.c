#include <stdio.h>

typedef struct {
  int inner;
} ContainerA;

typedef struct {
  int inner;
} ContainerB;

// Use void to accept any pointer
void increment(void* container) {
  // Cast pointer to ContainerB type
  ((ContainerB*)container)->inner += 1;
}

int main() {
  ContainerA container = {0};
  increment(&container);

  printf("Number %d\n", container.inner);
}