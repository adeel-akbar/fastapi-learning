# FastAPI Learning

My practice repo while learning FastAPI, PostgreSQL, and Python backend development.

This repository documents my learning journey through concepts, practice exercises, API development, and projects.

## Progress

- [x] FastAPI Basics
- [x] HTTP, Postman & Pydantic
- [x] CRUD & API Features
- [x] PostgreSQL & SQL
- [x] Database with Python
- [ ] SQLAlchemy & ORM
- [ ] Users & Authentication
- [ ] Relationships & Advanced Queries
- [ ] Alembic & API Configuration
- [ ] Deployment
- [ ] Docker
- [ ] Testing
- [ ] CI/CD

## Learning Log

### Chapter 1 — FastAPI Basics

- Learned FastAPI fundamentals
- Created GET and POST endpoints
- Learned how request bodies work
- Used Postman to send HTTP requests
- Learned Pydantic models and schema validation
- Practiced optional fields and default values

### Chapter 2 — CRUD & API Features

- Created a basic posts API
- Implemented GET all posts
- Implemented GET a single post by ID
- Implemented POST to create posts
- Implemented PUT to update posts
- Implemented DELETE to delete posts
- Learned HTTP status codes
- Learned how to handle errors with `HTTPException`
- Used FastAPI automatic API documentation
- Organized the application using a Python package
- Tested API endpoints using Postman

### Chapter 3 — PostgreSQL & SQL

- Learned database fundamentals and why databases are used in backend applications
- Learned PostgreSQL and database schemas/tables
- Practiced working with PostgreSQL through pgAdmin
- Learned basic SQL queries
- Practiced filtering data using `WHERE`
- Learned SQL operators
- Used `IN` and `LIKE`
- Practiced ordering results with `ORDER BY`
- Learned `LIMIT` and `OFFSET`
- Practiced modifying data using SQL

### Chapter 4 — Database with Python

- Connected Python to PostgreSQL using Psycopg
- Learned how database connections and cursors work
- Executed SQL queries from Python
- Retrieved database records using `fetchone()` and `fetchall()`
- Used `dict_row` to return database rows as dictionaries
- Used environment variables for database credentials
- Implemented database-backed GET, POST, PUT, and DELETE endpoints
- Used parameterized SQL queries
- Learned how to commit database changes
- Handled missing records with `HTTPException`
- Connected the FastAPI API to a PostgreSQL database

## Postman

Postman collections used to test the API endpoints are included in the `postman/` directory.
