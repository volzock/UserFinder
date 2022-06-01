### UserFinder

# these script can help you with database

```
docker pull postgres
docker run -e POSTGRES_PASSWORD=1234 -p 5432:5432 postgres
```

for viewing the current state of database use pgadmin

Аfter successfully starting the database and installing the required dependencies run

```
python main.py
```
