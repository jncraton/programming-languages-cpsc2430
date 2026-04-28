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
