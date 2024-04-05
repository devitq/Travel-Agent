![banner](/img/banner.png)

# ✈️ Travel agent bot

This bot will help you organise and plan your travels.

**Link:** [@itq_travel_agent_bot](https://t.me/@itq_travel_agent_bot/)

## ER Diagram

![ER Diagram](/img/ER.png)

[live preview](https://dbdiagram.io/d/Travel-agent-65f5a7c0ae072629ce2bd716)

## ⚙️ Technologies

### [Python](https://python.org/)

Python is used successfully in thousands of real-world business applications around the world, including many large and mission critical systems.

*Version: 3.12*

### [aiogram](https://aiogram.dev/)

aiogram is a modern and fully asynchronous framework for Telegram Bot API using asyncio and aiohttp.

*Version: 3.4*

### [SQLAlchemy](https://www.sqlalchemy.org/)

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

*Version: 2*

### [PostgreSQL](https://www.postgresql.org/)

PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

In project used as the main database.

*Version: 16.2*

### [Redis](https://redis.io/)

The in-memory data store used by millions of developers as a cache, vector database, document database, streaming engine, and message broker.

In project redis used as storage for states.

*Version: 7.2*

## 🤝 Integrations

### [OpenStreetMap API](https://wiki.openstreetmap.org/wiki/API)

OpenStreetMap is built by a community of mappers that contribute and maintain data about roads, trails, cafés, railway stations, and much more, all over the world.

In the project, the interaction with OpenStreetMap API is implemented using geopy lib.

### [GraphHopper](https://www.graphhopper.com/)

Service for conveniently building routes between points on the map. The user can view the route of a trip through webview that appears when clicking on the inline button.

### [OpenTripMap API](https://dev.opentripmap.org/product)

This API used to get nearby sights for location.

### [Open Weather Map API](https://openweathermap.org/)

API to easily get current weather in specified location.

## 🖥️ Demonstration

### Registration

![Registration](/img/gifs/Registration.gif)

The first step is, of cource, registration. User needs to fill in some information about himself before using the bot:

1. Username* - used to indeficate users and for interacting between users.
2. Age* - age of user
3. Sex*
4. Bio - Short info about yourself
5. Location* - City and country where user lives
6. Date joined - Fills automaticly

`*` - required

### Profile

![Profile](/img/gifs/Profile.gif)

User can edit and view it's profile anytime.

### Travels creation and editing

![TravelCreationAndEdit](/img/gifs/TravelCreationAndEdit.gif)

User can create, view, edit and delete travel:

1. Title* - title of travel, ex: Anapa 2010
2. Description - description of travel, could be None

`*` - required

### Locations creation and editing

![LocationCreationAndEditing](/img/gifs/LocationCreationAndEditing.gif)

User can create and delete locations

1. Location*
2. Date start* - Start of an activity in location(in UTC)
3. Date end* - End of an activity in location(in UTC)

`*` - required

### Planning routes

![RoutePlanning](/img/gifs/RoutePlanning.gif)

User can plan routes between locations he specified

### Notes creation and editing

![NoteCreationAndEditing](/img/gifs/NoteCreationAndEditing.gif)

User can create note(it could be file or photo) and edit it

### Getting nearby sights and weather of location

![GettingWeatherAndNearbySights](/img/gifs/GettingWeatherAndNearbySights.gif)

User can get location nearby sights(in 2 km radius) and get detailed description of sight.
Alsoo user can get current weather in location

There are also lots of small features and cool things that could be discovered while using the bot

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

### Generate new migrations(if needed)

```bash
alembic -c app/alembic.ini revision --autogenerate
```

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

**Structure**:

```bash
travel_agent /
    postgres (starts at 5432 port in your local network)
    redis (starts at 6379 port in your local network)
    app
    pgadmin (starts at 5050 port in your local network)
```

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
docker compose up -d --build
```
