# Python-Flask & Graphene-SQLAlchemy(GraphQL) & Flask-GraphQL-Auth(JWTAuthentication) Example Project


## Installing Requirements
Use Virtualenv and install the packages.
```
pip install -r requirements.txt
```
## Running Flask Server
Go to the root dir and run the below line in the terminal.
```
python app.py
```
## Creating a new Database
Create a database(Used MySQL)
```
database.py

# Replace 'mysql://root:password@localhost/db_name' with your path to database

engine = create_engine('mysql://root:password@localhost/db_name', convert_unicode=True)

```
## Testing GraphQL
Go to http://localhost:5000/graphql to use queries & mutations 

```
for testing queries and mutations please check the query format mentioned in queries.txt
```

```
check Flask-GraphQL-Auth documentation for more information on JWT Authentication used in the project.

```
