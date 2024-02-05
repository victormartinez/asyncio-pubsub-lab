# Asyncio Pubsub Lab

I've created this repository to investigate how DB connections behave under the stack of SQLAlchemy 2, asyncio and Pubsub.


## Setup Environment

Given you have Python properly installed with poetry:


1. Create .env from env.sample

2. Start Pubsub

```
make pubsub_build
make pubsub_up
make pubsub_create_topic
make pubsub_create_subscription
make pubsub_up
```

3. Start poetry

```
poetry install
poetry shell
```

4. Start database

```
make db_up
make db_upgrade
```


## Setup DB connection

`task.py` file connects to database, you have 4 options:

```python

async_session as async_session,
async_session_null as async_session_null,
session_factory,
session_null_factory,

```

So you can use:

```python

async for db_session in session_factory():

# OR

async for db_session in session_null_factory():

# OR

async with async_session() as db_session:

# OR

async with async_session_null() as db_session:

```


## Start Producer/Consumer

```
make pubsub_producer

make run_task
```

## Access Database Stats

[http://localhost:8080](http://localhost:8080)