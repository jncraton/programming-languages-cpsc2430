#include <iostream>

template <typename Type>
Type get_min (Type a, Type b) {
   return a < b ? a:b;
}

int main () {
   std::cout << get_min(2, 1) << std::endl;
   std::cout << get_min("hello", "world") << std::endl;
}
