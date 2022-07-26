create role vlp with login password 'vlp';
create database vlp with owner = vlp encoding = 'UTF8' connection limit = -1;
alter database vlp set time zone 'Europe/Moscow';
grant all on database vlp to vlp;
revoke all on database vlp from public;
revoke create on schema public from public;