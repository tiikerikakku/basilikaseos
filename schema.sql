drop table if exists users, messages;

create table users (
  id serial primary key,
  nick text unique check(coalesce(nick, '') != ''),
  secret text not null
);

create table messages (
  id serial primary key,
  msg text check(coalesce(msg, '') != ''),
  sender int references users not null,
  receiver int references users not null
);
