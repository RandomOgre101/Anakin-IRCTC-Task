# Anakin-IRCTC-Task

#### Rishikeshav Ravichandran
#### rishi.r1804@gmail.com

#### Loon Video Demonstration of code: https://www.loom.com/share/f65b741b6b844f038b0c705a7cda7851?sid=78ba0ba7-f2d0-4d85-8cfb-e44008ba79ff

### Techstack:
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)

### The SQL queries are done with SQLAlchemy and all documented in detail with comments within the source code files

### To set up and run the project:
- First clone the repository:
```
git clone https://github.com/RandomOgre101/Anakin-IRCTC-Task
```
- Now go to the folder .
```
cd Anakin-IRCTC-Task
```
- Run this command in terminal
```
docker compose up
```
- This will automatically build and run the containers

## Note 
- If there is an error in your Docker compose build, please try the below command:
```
docker compose build --no-cache
```

### To run tests:
- Run the command
```
pytest -s tests\testing.py
```

## Handling the race condition:
"If more than 1 user simultaneously tries to book seats, only either one of the users should be able to book"

I utilized SQLAlchemy's functions for this purpose, first a database transaction is started and then the train data is queried along with the with_for_update() function. This locks the row until the transaction is done so only one person will be able to book the seats for that train. If any error during booking, the transaction is rolled back else if all is well, it is committed.
