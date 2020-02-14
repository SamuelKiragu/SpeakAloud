CREATE TABLE users
  (Username VARCHAR(10) PRIMARY KEY,
  Email VARCHAR UNIQUE NOT NULL,
  Password VARCHAR(20) NOT NULL,
  DateCreated TIMESTAMP NOT NULL);

CREATE TABLE books
 (isbn VARCHAR(15) PRIMARY KEY,
  title VARCHAR(50) NOT NULL,
  author VARCHAR(30) NOT NULL,
  year VARCHAR(4) NOT NULL);

CREATE TYPE rating AS ENUM('1','2','3','4','5')

CREATE TABLE reviews
  (Username VARCHAR(10) REFERENCES users(Username),
  isbn VARCHAR(15) REFERENCES books(isbn),
  bookrating rating NOT NULL,
  comment VARCHAR(350),
  dateposted DATE NOT NULL DEFAULT CURRENT_DATE)
