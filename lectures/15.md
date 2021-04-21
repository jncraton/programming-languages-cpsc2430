Declarative Languages
=====================

Declarative Programming
-----------------------

We express the logic of our program without specifying its control flow

---

- Declarative - Focuses on the what
- Imperative - Focuses on the how

Examples
--------

- Logic langauges
- Purely functional languages
- Query langauges
- Domain specific languages

Logic Programming
-----------------

- Uses formal logic to solve problems
- Programs are made up of facts and rules
- Logic languages are covered in detail in Chapter 12

---

```prolog
factorial(0,1). 

factorial(N,F) :-  
   N>0, 
   N1 is N-1, 
   factorial(N1,F1), 
   F is N * F1.
```

Query Lanugages
---------------

- You've likely already encountered SQL
- This languages allows us to frame requests for data in terms of the data we want, not how it will be retrieved

---

```python
users = [(1, 'Alice'), (2, 'Bob')]
messages = [(1, 'Hey'), (2, 'Hi'), (1, 'Bye')]

for (msguser, text) in messages:
  for (userid, name) in users:
    if userid == msguser:
      print(f"{name}: {text}")
```

---

```sql
/* Create users */
create table users (
  userid integer primary key,
  name text
);
insert into users values 
  (1,'Alice'), 
  (2,'Bob'),
  (3,'Carol'),
  (4,'Dan'),
  (5,'Eve'),
  (6,'Frank');

/* Create chat message */
create table messages (
  userid integer,
  content text
);
insert into messages values 
  (2,'Does anyone know how modify a record in a SQL DB?'),
  (6,'Everyone knows how to do this'),
  (3,'Have you tried `UPDATE`?'),
  (2,'Nope. What does that do?'),
  (3,'It updates a record in a SQL DB...'),
  (2,'Oh cool. I will try that.'),
  (3,'Good luck!'),
  (5,'wat up, nerds!'),
  (4,'Is there any way to link records between two tables?'),
  (6,'Of course there is'),
  (1,'I think that you are looking for a `JOIN`'),
  (4,'Ah. Thanks!'),
  (1,'No problem.');

select "
  Display messages in order";
select userid, content 
  from messages;


select "
  Display messages with usernames";

select name, content 
  from messages 
  natural join users;

select "
  Display messages with usernames in reverse order";

select name, content 
  from messages 
  natural join users
  order by messages.rowid desc;

select "
  Show Dan's messages using a `where` clause";

select name, content 
  from messages 
  natural join users
  where name='Dan';

select "
  Show query plan (imperative program to complete query)";
explain query plan
select name, content 
  from messages 
  natural join users
  where name='Dan';

select "
  Create indexes to improve query plan";
create index messages_userid_idx on messages(userid);
create index users_name_idx on users(name);

select "
  Show new query plan";
explain query plan
select name, content 
  from messages 
  natural join users
  where name='Dan';


select "
  Change Dan's name to Dave";

update users
  set name = 'Dave'
  where name = 'Dan';

select name, content 
  from messages 
  natural join users;

select "
  Delete Eve's messages";

delete from messages
  where userid = (
    select userid 
    from users 
    where name = 'Eve'
  );

select name, content 
  from messages 
  natural join users;


/* 
Lab Excercises 

You should be able to complete these using the same techniqes
as above, but you if need a place to start to refresh you SQL
knowledge, you may want to start with an overview like this:

https://en.wikipedia.org/wiki/SQL_syntax#Queries
*/

select "
  Display messages with usernames sorted by username";

select "
  Change Alice's name to Abby";

select "
  Add a new message";

select "
  Delete Frank's messages";

/* 
You have nothing to do after this point

We just show all messages here so you can easily see your changes
*/

select "
  Final message list";
select name, content 
  from messages 
  natural join users;
```

Domain Specific Languages
-------------------------

Make
----

- The language that you've used to create makefiles is declarative
- You aren't telling make what to do to build your program
- You are providing a list of targets and their dependencies, and make determines how to resolve the dependencies

---

```make
all: main

main: main.c
  gcc main.c -o main
```

CSS
---

- Declarative DSL used to provide style information
- Describes what style an element should have without specifying how to apply it.

---

```css
body {
  max-width:960px;
}
h1 {
  font-size:36px;
}
nav {
  background-color:blue;
}
```


Hardware Description Languages
------------------------------

Language used to describe the behavior of electronic circuits.

---

```vhdl
entity adder is
       port (i0, i1 : in std_logic; ci : in std_logic; s : out std_logic; co : out std_logic);
     end adder;
     
     architecture rtl of adder is
     begin
        s <= (i0 xor i1 xor ci) after 35 ps;
        co <= (i0 and i1) or (i0 and ci) or (i1 and ci) after 70 ps;
     end rtl;
```
