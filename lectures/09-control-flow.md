Control Flow
============

---

Chapter 6

---

Control Flow
------------

Dictates the order of program execution

Unstructured Flow
-----------------

- Control flow is achieved using low-level constructs such as conditional branches and gotos
- Common in assembly languages and some other early languages

---

```fortran
if (A .lt. B) goto 10
...

10 ...
```

Structured Flow
---------------

- Gotos begin to be considered evil in the 60s
- We seek better tools to solve control flow problems
- Examples include `if`, `then`, `else` and `for`

Multi-level Returns
-------------------

- One "advantage" of goto is that it can jump anywhere in a program, not simply return to the caller
- Sometimes we want to jump outside of our immediate context, and multilevel returns can allow this

Exceptions
----------

- Exception handling is one example of a non-local return
- Execution moves from the point where the exception was raised to the point where the exception is handled

---

```python
def assert_positive(num):
  if num <= 0:
    raise ValueError

def assert_all_positive(nums):
  for n in nums:
    assert_positive(n)

try:
  assert_all_positive([1,2,3,-1])
except ValueError:
  print('All numbers are not positive')
```

Sequencing
----------

- Core to imperative programming
- Determines order of side effects such as assignment

Compound Statement
------------------

- An ordered list of statements that can be used where statements are expected
- Sometimes called *blocks*

Selection
---------

- Provide a way to select one set of statements based on a condition
- e.g. `if` or `switch`

Short-circuit Evaluation
------------------------

- Most modern languages will skip evaluating unneeded arguments in boolean expressions
- This creates more efficient programs
- This can be used for control flow

---

```js
function check_value(obj) {
  if (obj && obj.val) { // Confirms that obj is defined
    console.log('Value is set')
  } else {
    console.log('Value is unset')
  }
}

check_value()
check_value({'val':1})
```

Switch Statements
-----------------

- More efficient in hardware than nested conditionals
- Creates a jump table that transfers execution in a single instruction

---

```c
#include <stdio.h>

void count_down(int n) {
  switch (n) {
    case 3:
      printf("Three\n");
    case 2:
      printf("Two\n");
    case 1:
      printf("One\n");
  }
}

int main(void) {
  count_down(3);
}
```

Iteration
---------

- Allows computers to perform the same task repeatedly
- Makes computers useful for more than fixed-size tasks
- Without some mechanism of iteration or recursion, runtime is linearly coupled to program size

Logically Controlled Loops
--------------------------

- Run a block of code multiple times
- A condition may be used to stop execution
- May be pre-test, post-test, or midtest
- Post-test is most common

---

```c
#include <stdio.h>

int main(void) {
  printf("Press 'q' to quit\n");
  while (getchar() != 'q') {
    printf("Not quitting\n");
  }
  printf("Quitting\n");
}
```

Enumeration-Controlled Loops
----------------------------

- Executed once for every value in a finite set
- e.g. `for` loop

---

```fortran
do i = 1, 10, 2
  ...
```

```c
for (int i = 1; i < 10; i+=2) {
  ...
```

```python
for i in range(1, 10, 2):
  ...
```

For loop code generation
------------------------

```asm
mov first, r1
mov step, r2
mov last, r3
body:
  # Loop body
  # Increment loop counter
  add r1, r2
check:
  # Check loop condition
  cmp r1, r3
  jl body
```

Semantic Complications
----------------------

- Many languages e.g. C allow complex expressions in for loop control conditions
- Machine code for `for` loops must often be more complex, as loop count can't be easily predicted

Recursion
---------

- We can use nested function calls to perform tasks repeatedly
- This can be more readable than iterative solutions
- This can be less performant than iterative solutions

---

```python
def prime_factors(num):
  for i in range(2, num + 1):
    if not num % i:
      return [i] + prime_factors(int(num/i))

  return []

print(prime_factors(780))
```

Recursive optimizations
-----------------------

- Some compilers will optimize recursion into iteration removing the need for new stack frames
- In this case, recursion is very efficient
- Tail recursion makes optimization simpler

---

```python
def factorial(n):
  if n == 1: return n

  return n * factorial(n-1)

print(factorial(5))
```

---

Tail-recursive version:

```python
def factorial(n, accum=1):
  if n == 1: return accum

  return factorial(n-1, n*accum)

print(factorial(5))
```

Tail Recursion
--------------

- No computation takes place after the recursive call
- Can be computed using constant space
- Can be optimized to simple iteration
- [More info](https://cs.stackexchange.com/a/7822/44408)
