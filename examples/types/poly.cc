#include <iostream>
#include <cstring>

template <typename Type>
Type get_min(Type a, Type b) {
  return a < b ? a : b;
}

template <>
const char* get_min<const char*>(const char* a, const char* b) {
  return std::strcmp(a, b) < 0 ? a : b;
}

int main() {
  std::cout << get_min(2, 1) << std::endl;
  std::cout << get_min("hello", "world") << std::endl;
}