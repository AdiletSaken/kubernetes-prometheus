CREATE DATABASE myapp;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'passwd';
GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;

CREATE TABLE students(id INT PRIMARY KEY, name VARCHAR(20));

INSERT INTO students(id, name) VALUES(1, 'Student1');
INSERT INTO students(id, name) VALUES(2, 'Student2');
