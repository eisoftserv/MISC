# Project 1

Web Programming with Python and JavaScript


## About My Project1


I've installed Python 3.8 - the current version of the distributable, and I've prepared the test database on Heroku, on a free-tier Postgres resource.

I've added two environment variables to my operating system (Windows 10 Pro):
* DATABASE_URL - for direct access to the test database
* GOODREADS_KEY - my Goodreads key - for pulling review data about a given book

I've used raw SQL queries against my test database, and I've implemented full text search as per the project's requirements in this way:
* defined the "isbn" field as varchar
* employed the "position" scalar funtion in the "where" clause
* haven't configured case-insensitive search

I've resolved the user input data validation problem by writing custom helper functions - they are included in the application.py source file.

The user interface includes minimal CSS styling (media rules, some sizing, positioning and colors), and it's based on the "mobile-first" concept.

I've included the "requests" module in "requirements.txt", as it was not part of the Python distributable, and I was in need to add it to my local environment with "pip".


## Files and Folders

* **static** standard folder
    * app.css - stylesheet
    * back.png, blogger.png, logo.png, logout.png, twitter.png - images used on the website
* **templates** standard folder for jinja2 templates
    * dashboard.html - for searching and displaying search results (books)
    * detail.html - for displaying details and review list for a given book, and for submitting user's review on the same
    * door.html - for user "login" and "signup" operations
    * layout.html - the master template for the website
    * problem.html - for custom error handling
* application.py - flask source code (middleware)
* books.csv - sample data received for the project
* import.py - source code for uploading the sample data (it contains the code for importing the data into my already existing test database, and respectively for displaying the table and index structure of my test database). Below I'm listing the SQL DDL commands I've used for creating my test database.
* README.md - the current file
* requirements.txt - modules needed by the project (for the "pip" utility)


# My Postgres Tables

## users

- id      sequence
- name    varchar(100) UNIQUE
- pwd     varchar(50)
- stamp   timestamp

### SQL DDL command

"create table users (id serial primary key, name varchar(100) UNIQUE not null, pwd varchar(50) not null, stamp timestamp default NOW());"


## books

- id          sequence
- isbn        varchar(50) UNIQUE
- title       varchar(200)
- author      varchar(200)
- year        integer
- revtot      integer
- revcoumt    integer

### SQL DDL commands

- "create table books (id serial primary key, isbn varchar(50) UNIQUE not null, title varchar(200) not null,  author varchar(200) not null, year integer default 0, revtot integer default 0, revcount integer default 0);"
- "create index books_title on books (title);"
- "create index books_author on books (author);"


## reviews

- id      sequence
- idbook  integer
- iduser  integer
- comment varchar(1000)
- stamp   timestamp

### SQL DDL commands

- "create table reviews (id serial primary key, idbook integer default 0, iduser integer default 0, rating integer default 0, comment varchar(1000) not null, stamp timestamp default NOW());"
- "create index reviews_idbook on reviews (idbook);"
- "create index reviews_iduser on reviews (iduser);"

