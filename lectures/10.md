Lab questions?

Iterators
=========

---

- Provide a construct to yeild successive items
- Also called enumerators

---

```python
for i in range(10):
  print(i)
```

---

```python
for i in [1,2,3]:
  print(i)
```

---

```python
for character in "Hello, World!":
  print(character)
```

"True" Iterators
----------------

- Many languages provide a way to iterate over objects
- A true iterator provides a way to iterate without storing intermediate data structures

---

```python
# Never creates a list of items in memory
for i in range(10):
  print(i)

# Creates a list of items in memory, then iterates over them
for i in [0,1,2,3,4,5,6,7,8,9]:
  print(i)
```

Python Iterator
---------------

- Includes an `__iter__` method that returns an iterator
- Includes a `__next__` method that returns the next item

Duck Typing
-----------

- We can identify the type of an object by its properities
- If it walks like a duck and quacks like a duck, it is a duck
- We can implement and iterator without inhereting from an iterator class

---

Python `range` [implementation](https://replit.com/@jncraton/range#main.py).

Generators
----------

- Provide a generalized construct for creating iterators
- We can `yield` successive values

---

```python
def squares():
  i = 1
  while(True):
    yield i*i
    i += 1

results = squares()
for i in range(20):
  print(next(results))
```

---

```python
def primes():
  current = 2

  while True:
    if is_prime(current):
      yield current
    current += 1
```
