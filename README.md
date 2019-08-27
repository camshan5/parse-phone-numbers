# Parse Phone Numbers - Flask Application

This is a simple application that parses and formats phone numbers.
Multiple phone numbers can be included in the textbox at any given time.

If there are multiple phone numbers in the form when the data is submitted, they will be assigned
to the same user from the username field

#### Program Use Case:
The application assigns phone numbers to a user and stores the information in a database,
in addition to displaying the data on the screen. This could be useful when
parsing, for example, a e-mail signature where you want to assign
all associated numbers found with the user.

Example Data:
>Cameron Shannon - 
>Email: cameron.shannon@gmail.com - 
>Cell: 832 845-8198 -
>Work: 805.490.7239 -

The above will return both phone numbers in the same format.

---
## Project Setup Using Docker

Build the image inside the project root &rarr; `parse-phone-numbers`

```bash
$ docker-compose up —build
```
Note:
add `-d` flag is used to run the containers in the background

---
#### Testing

To run the python tests use the following command:
```bash
$ docker-compose exec users python manage.py test
```
---

#### Database Config

Apply the model to the database:
```bash
$ docker-compose exec users python manage.py recreate_db
```


Confirm the database is configured properly:

```bash
$ docker-compose exec users-db psql -U postgres


psql (11.2)
Type "help" for help.

postgres=# \c users_dev
You are now connected to database "users_dev" as user "postgres".

users_dev=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

users_dev=# \q
```

If you are running a new database, test out the seed data command:

```bash
$ docker-compose exec users python manage.py seed_db`
```

Navigate to http://localhost:5001/ to view the application running.

Test connection, navigate to: http://localhost:5001/users/ping
