Type Systems
============

---

Chapters 7 & 8

---

Purpose
-------

1. Provide implicit context for operations
2. Limit the set of valid operations
3. Explicit types can make code easier to read
4. Types known at compile time can drive performance optimizations

Constructs with Types
---------------------

- Anything with a value
    - Constants
    - Variables
    - Parameters
    - Literals

A type system
-------------

1. A mechanism to define types
2. Set of rules for
    - Type equivalence
    - Type compatibility
    - Type inference

Type Checking
-------------

- The process of ensuring that language type rules are followed
- Violations are *type clashes*

Strong Typing
-------------

A language enforces valid types and operations

Static Typing
-------------

A language is strongly typed and rules are enforced at compile time

Example Languages
-----------------

- Javascript - weak/dynamic
- Python - strong/dynamic
- C - weak/static (types can be coerced)
- Java - strong/static

JavaScript
---------

- Weakly typed
- Dynamically typed

---

```js
// None of these are runtime errors
"Six" * 6 // NaN
true * 6 // 6
[1,2] * 6 // NaN
(() => 0) * 6 // NaN
```

---

```js
// Results can be different than we might expect
1 + 2 + 3 // 6
1.0 + 2 + 3 // 6
1 + "2" + 3 // '123'
1 + 2 + "3" // '33'
1 - "2" + 3 // 2
1 + true // 2
```

Python
------

- Strongly typed
- Dynamically typed

---

```python
# We don't need to declare types explicitly
name = "Prof Craton" # Name is a string
# We will get errors for invalid types
score = name + 1 # TypeError
```

C
-----

- Weakly typed
- Statically typed

---

```c
// This program will not compile
#include <stdio.h>

int main(void) {
  int num = 2; // int type is required

  printf(num); // type error (needs format string)
}
```

---

```c
// This program will likely
#include <stdio.h>

int main(void) {
  int num = 2; // int type is required

  printf((char*)num); // type error (needs format string)
}
```

Polymorphism
------------

- We can design code to work with different types
- This can be achieved in C++ using generics (templates)

---

```c++
#include <iostream>

template <typename Type>
Type get_min (Type a, Type b) { 
   return a < b ? a:b; 
}

int main () {
   std::cout << get_min(2, 1) << std::endl; 
   std::cout << get_min("hello", "world") << std::endl;
}
```

Null
----

- We often want a way to specify something other than the regular return value
- e.g. popping from and empty stack, dividing by zero, etc
- *null* is one option, but it can be used differently in different contexts

Rust Option
-----------

> Type Option represents an optional value: every Option is either Some and contains a value, or None, and does not. Option types are very common in Rust code

[docs](https://doc.rust-lang.org/std/option/)

---

```rust
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

fn main() {
  match divide(2.0, 1.0) {
      Some(x) => println!("Result: {}", x),
      None    => println!("Cannot divide by 0"),
  }
}
```

Classification of Types
----------------------

- Booleans
- Numerics
- Enums
- Subrange
- Composite

Enums
-----

Introduced in Pascal:

```pascal
type weekday = (sun, mon, tue, wed, thu, fri, sat);
```

Subrange
--------

Also introduced in Pascal:

```pascal
type score = 0..100;
```

Composite Types
---------------

- Records (structs) - introduced by COBOL
- Arrays
- Sets
- Lists
- Files


Composite Types
---------------

Records (structs)
-----------------

- Allows different types to be stored and accessed together
- Individual *fields* are typically accessed using `.` notation.

Struct Packing
--------------

On most systems, the layout of items in a struct can change the storage space requirements due to alignment constraints.

---

```c
#include <stdio.h>

int main(void) {
  typedef struct {
    char id;
    int hp;
    char weapon;
  } actor1;

  typedef struct {
    char id;
    char weapon;
    int hp;
  } actor2;

  printf("%lu %lu\n", sizeof(actor1), sizeof(actor2));
}
```

Arrays
------

- Used to group a number of items of the same type

Strings
-------

- Most typically an array of characters

Sets
----

- Store an arbitrary number of *distinct* values of the same type

```python
print({1,2,3}) # {1, 2, 3}
print({1,2,3,3,2,1}) # {1, 2, 3}
```

Lists
-----

- Hold a number of elements of the same type
- Typically differ from arrays in their allocation mechanism
- Lists will scale dynamically while arrays are fixed

---

Have you ever needed to write code to remove duplicate elements from a list?

> The difference between a bad programmer and a good one is whether they consider their code or their data structures more important. Bad programmers worry about the code. Good programmers worry about data structures and their relationships.
> - Linus Torvald

Homogeneous types
----------------

- Languages may differ in whether they allow different types to be used in certain composite types (e.g. lists and sets)
- ML and Haskell are homogeneous, many others are heterogeneous

Type Checking
-------------

- Type equivalence - Types are the same
- Type compatibility - Types can be used interchangeably
- Type Inference - Determining types automatically

Type Equivalence
----------------

- Structural equivalence - based on content
- Name equivalence - based on lexical occurrence of type definitions

---

```c
#include <stdio.h>

typedef struct {
  int inner;
} ContainerA;

typedef struct {
  int inner;
} ContainerB;

// Needs to be:
//typedef ContainerA ContainerB;

void increment(ContainerB* container) {
  container->inner += 1;
}

int main() {
  ContainerA container = {0};
  increment(&container);

  printf("Number %d\n", container.inner);
}
```

Type Compatibility
------------------

- Types don't need to always be fully equivalent to be used
- *Coercion* is used to convert from one type to another

---

```python
print(1 + 2) # 3
print(1 + 2.0) # 3.0
print(1 / 2) # 0.5 in Python 3, 0 in Python 2
```

Universal Reference Types
-------------------------

- Most languages provide a universal reference that can point to any object
- Examples in include `void` in C, `Object` in Java, and `object` in C#

---

Let's revisit our previous C container example to use void.

---

```c
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
```

Type Inference
--------------

- We can determine types without specifying them

```c
1 + 2 // int
1.0 + 2.0 // float
```

---

C++ provides the `auto` keyword to infer types

```c++
#include <iostream>

int main() {
  // Type automatically determined
  auto pi = 3.14;

  std::cout << pi << "\n";
}
```

---

Some languages are statically typed while having very powerful type inference such that explicit types are rarely required. Examples are ML, Haskell, and Rust.

---

```rust
fn main() {
    let elem = 5u8;
    // The compiler knows that `elem` has type u8

    let mut vec = Vec::new();
    // The compiler doesn't yet know the exact type of `vec`
    // It just knows that it's a vector (`Vec<_>`)

    vec.push(elem);
    // Aha! Now the compiler knows that 
    // `vec` is a vector of `u8`s (`Vec<u8>`)

    println!("{:?}", vec);
}
```

Equality Testing
----------------

- How do we know if you two values are equal?
- Compare values
- Compare references

---

```js
a = {} // Empty object
b = {} // Another empty object
a == b // `false` because they aren't the same empty object
```

Shallow vs Deep Compare
-----------------------

- Shallow - We check to see if references point to the same object
- Deep - We check to see if objects hold the same values

---

```c
#include <stdio.h>

void main(void) {
  char * a = malloc(6);
  char * b = malloc(4);
  strcpy(a, "Alice");
  strcpy(b, "Bob");

  // Shallow compare
  printf("%d\n", a == b); // False
  printf("%d\n", a == a); // True

  // Undefined behavior, typical results provided
  printf("%d\n", a == "Alice"); // False
  printf("%d\n", a != "Bob"); // True

  // Deep compare
  printf("%d\n", strcmp(a, a) == 0); // True
  printf("%d\n", strcmp(a, b) == 0); // False
  printf("%d\n", strcmp(a, "Alice") == 0); // True

}
```
