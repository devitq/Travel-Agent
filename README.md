# ✈️ Travel agent bot

This bot will help you organise and plan your travels.

## ⚙️ Technologies

### Python

Python is used successfully in thousands of real-world business applications around the world, including many large and mission critical systems.

### aiogram

aiogram is a modern and fully asynchronous framework for Telegram Bot API using asyncio and aiohttp.

### SQLAlchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

### PostgreSQL

PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

## 🛠️ Local development & testing

### Clone repository with git

```bash
git clone https://github.com/Central-University-IT-prod/backend-devitq.git
```

### Navigate to the project directory

```bash
cd backend-devitq
```

### Create virtual enviroment & activate it

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Linux

```bash
python -m venv venv
source venv/bin/activate
```

### Install dev requirements

```bash
pip install -r requirements/dev.txt
```

### Setup .env file

#### Windows

```cmd
copy template.env .env
```

#### Linux

```bash
cp template.env .env
```

And replace all default values with actual values

### Apply migrations with alembic

```bash
alembic -c app/alembic.ini upgrade head
```

### Run bot in development mode

```bash
python -m app
```

## 🚀 Deploying

Our app uses docker compose for production deployment.

### Clone repository with git

```bash
git clone https://github.com/Central-University-IT-prod/backend-devitq.git
```

### Navigate to the project directory

```bash
cd backend-devitq
```

### Setup .env file

#### Windows

```cmd
copy template.env .env
```

#### Linux

```bash
cp template.env .env
```

And replace all default values with actual values

### Pull actual docker images

```bash
docker compose pull
```

### Start containers (in detached mode)

```bash
docker compose up -d
```

## Notes

Set this in .env file when using docker compose:

```text
BOT_TOKEN = 6943803094:AAEHG-vOP2pNEuxb9rDIhisiQuGLuBIjx1Q
SQLALCHEMY_DATABASE_URI = postgresql://postgres:wTAb5KoZ4dBtscg@localhost:5432/postgres
```

I thought up the architecture of the project myself, I won't mind feedback on it)
