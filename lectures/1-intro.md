Course Overview
===============

Introduction
------------

- 1.1 - 1.3 Why programming languages?
- 1.4 - 1.6 Compilation vs Interpretation

Foundations
-----------

- 2.1 - 2.2 Lexing (aka Tokenizing, Scanning)
- 2.3 - 2.5 Parsing - ASTs, Language Hierarchy
- 3.1 - 3.2 Binding and Lifetime
- 3.3 - 3.6 Scope and Closures
- 5 - Target Machine Architecture

Language Design
---------------

- 6 - Control Flow
- 7 - Type systems
- 8 - Composite Types
- 9 - Subroutines and Control Abstraction

Programming Paradigms
---------------------

- 10 - Object Oriented Programming (Python)
- 11 - Functional Programming (JS)
- 12 - Declarative Programming (SQL)

Introduction
============

History of Programming
----------------------

---

![A Bombe used for Enigma decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Wartime_picture_of_a_Bletchley_Park_Bombe.jpg/541px-Wartime_picture_of_a_Bletchley_Park_Bombe.jpg)

---

["Programming" scene from The Imitation Game](https://www.youtube.com/watch?v=pmEXNaWFGYQ&t=262s)

---

![Punch card with Fortran statement](https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/FortranCardPROJ039.agr.jpg/1024px-FortranCardPROJ039.agr.jpg)

Why Languages?
--------------

---

!["Hello World" binary](figures/bin-hello.png)

---

```
objdump -d hello
```

```asm
hello:     file format elf64-x86-64

Disassembly of section .text:

00000000004000d4 <.text>:
  4000d4:	48 c7 c0 01 00 00 00 	mov    $0x1,%rax
  4000db:	48 c7 c7 01 00 00 00 	mov    $0x1,%rdi
  4000e2:	48 c7 c6 02 01 40 00 	mov    $0x400102,%rsi
  4000e9:	48 c7 c2 0e 00 00 00 	mov    $0xe,%rdx
  4000f0:	0f 05                	syscall 
  4000f2:	48 c7 c0 3c 00 00 00 	mov    $0x3c,%rax
  4000f9:	48 c7 c7 00 00 00 00 	mov    $0x0,%rdi
  400100:	0f 05                	syscall 
```

mov $0x1, %rax
-------------

### 48 c7 c0 01 00 00 00 	

- 48 - [REX prefix](https://wiki.osdev.org/X86-64_Instruction_Encoding)
- c7 - [mov instruction](http://ref.x86asm.net/coder64.html#xC7)
- c0 - register rax
- 01 00 00 00 - immediate value

---

![Memory hierarchy](https://upload.wikimedia.org/wikipedia/commons/0/0c/ComputerMemoryHierarchy.svg)

16 x64 Registers
-------------

- RAX
- RBX
- RCX
- RDX
- RSI
- RDI
- RSP - Stack Pointer
- RBP - Base Pointer
- R8 - R15
