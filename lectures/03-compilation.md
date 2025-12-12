Compilation and Interpretation 1.4
==================================

Compilation
-----------

Code is converted to machine code or another executable form

---

![Three stage compiler architecture](https://upload.wikimedia.org/wikipedia/commons/c/cc/Compiler_design.svg)

Interpretation
--------------

- Code is executed by another program
- Python REPL example
- JS browser REPL example

Compilation and Interpretation
------------------------------

- JITs (e.g. JS)
- Compiled languages with runtimes (e.g. Go)
- VM bytecode (e.g. Java)

C Compilation Steps
--------------------

1. Preprocessing
2. Compilation
3. Assembly
4. Linking

Viewing Intermediate Output
---------------------------

```sh
gcc hello.c -save-temps -o hello
```

1. Preprocessor - hello.i
2. Compilation - hello.s
3. Assembly - hello.o
4. Linking - hello

Preprocessor Output
-------------------

`hello.i` is plain text C code and can be inspected.

Compiler Output
---------------

`hello.s` is plain text Assembly and can be inspected

Assembler Output
----------------

- hello.o is x64 machine code
- It can be viewed in a hex editor e.g. `hexedit hello.o`
- We can also view it's content using `objdump -d hello.o`

Linker Output
-------------

- `hello` is x64 machine code
- It can be viewed in a hex editor e.g. `hexedit hello`
- We can also view it's content using `objdump -d hello`

make
----

`make` is a build automation tool

makefiles
---------

Contain a set of directives that instruct make how to create a target.

Example makefile
----------------

```makefile
all: double.txt

double.txt: original.txt
  cat $< $< > $@
```

Lab 1 Solution
--------------
