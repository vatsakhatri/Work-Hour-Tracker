# Work-Hour Tracker 
- Start Date: 20-06-2024
- Created by : Vatsa Khatri


## Introduction


In this documentation, we will create APIs that manages a users Working hours based on the punch IN-OUT time.



## ***Backend Configuration***


### Install dependencies


#### Adding the packages into the requirements file:


```
📁 requirements.txt -----

fastapi
uvicorn
requests
```


#### Executing the installation command again to install the modified libraries in the project


```pip3 install -r requirements.txt```




### Alembic setup (Migrations)
```
cd work_hour
alembic init alembic
```
- this will create a alembic folder and 📁 alembic.ini , below are the changes to be done   
- 
    ```
    📁 alembic.ini ----- 
    
    sqlalchemy.url =mysql+pymysql://root:<password>@localhost:3306
    /<dbname>
    
    
    📁 alembi/env.py ----- 
    
    from models import Base
    target_metadata = Base.metadata
    
    ```


```
alembic revision --autogenerate -m "creat table"
alembic upgrade head
```


### Commands to run
```
cd work_hour
uvicorn main:app --relaod
```

## Services


- ### UserService

    - File path: `work_hour/UserService.py`
    - `create_user()` : check if a user exist if not create a new user with the password hashed
    - `get_user_by_username()` : query the db with username and return user


- ### AuthService
    - File path: `work_hour/AuthService.py`
    - `authenticate_user()` : check if the user exists before sending the jwt.
    - `create_jwt()` : create a paylaod with the given username and expiry and sign it with your `secret_key`
    - `get_user_by_token()` : given a jwt, from payload we get username and query the db for that user and return it .
    - `get_user_byheader()` : used to extract the jwt from request header and get_user_by_token.

- ### PunchService
    - `punch_in() && punch_out()` : given a user_id extracted from jwt create a entry in Timestamp table of required type.
    - `get_user_working_hours()`: given a user & day return the total working hours 
    
    
