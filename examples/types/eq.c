#include <stdio.h>

typedef struct ContainerA {
  int inner;
} ContainerA;

typedef struct ContainerB{
  int inner;
} ContainerB;

void increment(ContainerB* container) {
  container->inner += 1;
}

int main() {
  ContainerA container = {0};
  increment(&container);

  printf("Number %d\n", container.inner);
}
