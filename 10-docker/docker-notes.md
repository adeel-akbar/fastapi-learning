# Docker Notes

## What is Docker?

Docker packages an application together with the environment and dependencies it needs so that it can run consistently on different machines.

Instead of manually setting up Python, dependencies, and other application requirements on every machine, we can build a Docker image and run a container from that image.

---

## Docker Image vs Container

### Image

A Docker image is the prepared package used to create containers.

It can contain:

- Python/runtime
- Installed dependencies
- Application code
- Instructions for starting the application

An image is built from a Dockerfile.

```text
Dockerfile → Image
```

### Container

A container is a running instance of an image.

```text
Dockerfile → Image → Container
```

One image can be used to create multiple containers.

---

## Base Image

A base image is an existing Docker image used as the starting foundation for our own image.

For example:

```dockerfile
FROM python:3.14.7
```

Instead of installing and configuring Python from scratch, we start with an official Python image and add our application's dependencies, code, and startup instructions on top of it.

```text
Python Base Image
       ↓
Dependencies
       ↓
Application Code
       ↓
Startup Instructions
       ↓
Our FastAPI Image
```

---

## Dockerfile

A `Dockerfile` is a set of instructions Docker uses to build an image.

Basic FastAPI Dockerfile:

```dockerfile
FROM python:3.14.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `FROM`

```dockerfile
FROM python:3.14.7
```

Defines the base image.

Instead of creating an environment with Python from scratch, we start from an existing official Python image.

The Python version should normally be a version that the application is known to work with.

---

### `WORKDIR`

```dockerfile
WORKDIR /usr/src/app
```

Sets the working directory inside the image/container.

The Dockerfile instructions that follow operate relative to this directory.

It is similar to changing into a directory with `cd`.

The path is chosen by us. `/usr/src/app` is simply the location being used for the application inside the container.

---

### `COPY requirements.txt ./`

```dockerfile
COPY requirements.txt ./
```

Copies `requirements.txt` from our project into the current working directory inside the image.

Because our working directory is:

```text
/usr/src/app
```

the file will be copied there.

---

### `RUN`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

`RUN` executes a command while Docker is building the image.

Here, pip installs all Python dependencies listed in `requirements.txt`.

`--no-cache-dir` tells pip not to keep its downloaded package cache after installation, avoiding unnecessary files in the image.

---

## Cache

A cache stores something that was previously downloaded, calculated, or built so it can potentially be reused instead of doing the same work again.

For example, pip can keep downloaded packages in its cache:

```text
Download package
      ↓
Install package
      ↓
Keep downloaded package in cache
```

Using:

```bash
pip install --no-cache-dir
```

tells pip not to keep those downloaded package files after installation.

Docker also has its own build cache, which is separate from pip's cache.

---

### `COPY . .`

```dockerfile
COPY . .
```

Copies the project files from the current build context into the current working directory inside the image.

The first `.` represents the source.

The second `.` represents the destination.

```text
COPY source destination
COPY   .       .
```

Conceptually:

```text
Local Project
     ↓
COPY . .
     ↓
/usr/src/app inside image
```

---

### `CMD`

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Defines the command that runs when a container is started from the image.

For our FastAPI application, this starts Uvicorn.

```text
Container starts
      ↓
CMD runs
      ↓
Uvicorn starts
      ↓
FastAPI starts
```

`--host 0.0.0.0` allows Uvicorn to listen on the container's network interfaces so traffic forwarded into the container can reach the application.

`--port 8000` tells Uvicorn to listen on port `8000` inside the container.

---

## Building a Docker Image

To build the FastAPI image:

```bash
docker build -t fastapi-social-api .
```

### `docker build`

Builds a Docker image using the Dockerfile.

### `-t fastapi-social-api`

Gives the image a tag/name:

```text
fastapi-social-api
```

### `.`

The final `.` tells Docker to use the current directory as the build context.

The build context contains the files Docker can access while building the image, such as:

```text
Dockerfile
requirements.txt
app/
alembic/
...
```

Overall:

```text
Dockerfile + Project Files
          ↓
      docker build
          ↓
        Image
```

---

## Docker Hub

Docker Hub is a registry used to store and distribute Docker images.

Official images such as Python and PostgreSQL can be pulled from Docker Hub.

For example:

```text
Docker Hub
    ↓
Official Python Image
    ↓
Our Dockerfile
    ↓
Our FastAPI Image
```

We can also push our own application images to a registry and later pull them onto another machine or server.

---

## Port Mapping

A container has its own network environment.

Docker can map a port on the host machine to a port inside a container.

For example:

```text
8000:8000
```

means:

```text
Host Machine
Port 8000
    ↓
Docker Port Mapping
    ↓
Container
Port 8000
    ↓
FastAPI
```

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

The ports do not have to be the same.

For example:

```text
4000:8000
```

means:

```text
Browser
   ↓
localhost:4000
   ↓
Host port 4000
   ↓
Docker
   ↓
Container port 8000
   ↓
FastAPI
```

Docker knows which container should receive the traffic based on the configured port mapping.

---

## Volumes

Containers are designed to be replaceable.

If PostgreSQL stores important database data only inside its container and that container is removed, we do not want to lose that data.

A Docker volume provides persistent storage whose lifecycle is separate from a particular container.

```text
PostgreSQL Container
        ↓
      Volume
        ↓
Persistent Database Data
```

If the PostgreSQL container is removed:

```text
PostgreSQL Container ❌

Volume ✅
Database Data ✅
```

A new PostgreSQL container can then use the same volume and access the existing data.

A volume is not the database itself. It provides persistent storage for the files PostgreSQL uses to store the database.

---

## Bind Mounts

A bind mount connects a file or directory on the host machine to a location inside a container.

This is especially useful during development.

Without a bind mount:

```text
Change local code
      ↓
Container still has old copied code
      ↓
Image may need to be rebuilt
```

With a bind mount:

```text
Local Project Directory
          ↕
      Bind Mount
          ↕
Directory Inside Container
```

Changes made to the local source code become visible inside the container.

This allows us to develop without rebuilding the Docker image every time we change our application code.

---

## Environment Variables

Containers have their own environment.

Environment variables available on the host machine are not automatically available inside a container.

Our FastAPI application may need variables such as:

```text
DATABASE_HOSTNAME
DATABASE_PORT
DATABASE_PASSWORD
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

These variables need to be provided to the container.

Conceptually:

```text
Environment Variables
        ↓
FastAPI Container
        ↓
Pydantic BaseSettings
        ↓
FastAPI Application
```

---

## Docker Networking

Our FastAPI application and PostgreSQL database can run in separate containers.

```text
FastAPI Container

PostgreSQL Container
```

These containers need a way to communicate.

Docker Compose can place them on the same Docker network.

Containers on that network can communicate using their service names.

For example, if the PostgreSQL service is named:

```text
postgres
```

the FastAPI application can use:

```text
DATABASE_HOSTNAME=postgres
```

instead of:

```text
DATABASE_HOSTNAME=localhost
```

This is important because inside the FastAPI container:

```text
localhost
```

refers to the FastAPI container itself, not the PostgreSQL container.

Conceptually:

```text
       Docker Network

FastAPI Container
       |
       | postgres
       ↓
PostgreSQL Container
```

---

## Docker Compose

Docker Compose is used to define and manage applications that use multiple containers.

For our application, we have two main services:

```text
Docker Compose
      |
      ├── FastAPI Container
      |
      └── PostgreSQL Container
```

Instead of manually creating and configuring each container separately, Docker Compose allows us to define the entire application in a YAML file.

Our development Compose file is:

```text
docker-compose.yml
```

Modern Docker Compose does not require the old:

```yaml
version: "3"
```

field, so the file can begin directly with:

```yaml
services:
```

---

## Services

A service represents one part of the application that runs in a container.

For our application:

```yaml
services:
  api:
    ...

  postgres:
    ...
```

We chose the service names:

```text
api
postgres
```

`api` represents our FastAPI application.

`postgres` represents our PostgreSQL database.

Service names are also important for Docker networking. Containers in the same Compose application can communicate using their service names.

---

## FastAPI Service

Our FastAPI service is:

```yaml
api:
  build: .
  ports:
    - "8000:8000"
  volumes:
    - ./:/usr/src/app
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  env_file:
    - .env.docker
  depends_on:
    postgres:
      condition: service_healthy
```

### `build: .`

```yaml
build: .
```

Tells Docker Compose to build the image using the Dockerfile in the current directory.

Conceptually:

```text
docker compose up
        ↓
Compose sees build: .
        ↓
Finds Dockerfile
        ↓
Builds FastAPI image
        ↓
Creates FastAPI container
```

---

## Port Mapping in Compose

```yaml
ports:
  - "8000:8000"
```

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

Therefore:

```text
localhost:8000
      ↓
Host port 8000
      ↓
Docker
      ↓
FastAPI container port 8000
      ↓
Uvicorn
```

---

## Development Bind Mount

```yaml
volumes:
  - ./:/usr/src/app
```

This is a bind mount.

```text
./
```

represents our local project directory.

```text
/usr/src/app
```

is the application directory inside the container.

Therefore:

```text
Local Project
      ↕
Bind Mount
      ↕
/usr/src/app inside container
```

Changes made to our local code become immediately visible inside the container.

This is mainly useful during development.

---

## Development Command

```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The `command` in Compose overrides the default `CMD` from the Dockerfile for this service.

Our Dockerfile contains the normal startup command, while the development Compose file adds:

```text
--reload
```

This allows Uvicorn to automatically reload when application files change.

The bind mount and `--reload` work together:

```text
Change code locally
      ↓
Bind mount makes change visible
      ↓
Uvicorn detects change
      ↓
Application reloads
```

`--reload` is useful during development and should normally not be used in production.

---

## Docker Environment File

Our normal application uses Pydantic Settings with:

```python
model_config = SettingsConfigDict(env_file=".env")
```

For Docker development, we use a separate:

```text
.env.docker
```

file.

Compose provides it to the container using:

```yaml
env_file:
  - .env.docker
```

This injects the values from `.env.docker` into the container's environment.

Environment variables already provided to the process take priority over values Pydantic would otherwise load from `.env`.

Therefore our Python application does not need to change.

Conceptually:

```text
Normal local execution

.env
  ↓
Pydantic Settings
  ↓
FastAPI
```

and:

```text
Docker execution

.env.docker
      ↓
Docker Compose
      ↓
Container Environment
      ↓
Pydantic Settings
      ↓
FastAPI
```

---

## Docker Database URL

Our FastAPI application uses a complete database URL.

Outside Docker, PostgreSQL may be accessed through:

```text
localhost
```

But inside the FastAPI container:

```text
localhost
```

refers to the FastAPI container itself.

Because our PostgreSQL Compose service is called:

```text
postgres
```

our Docker database URL uses `postgres` as the hostname.

Example structure:

```text
postgresql://USER:PASSWORD@postgres:5432/DATABASE
```

Breakdown:

```text
postgresql:// USER : PASSWORD @ HOST : PORT / DATABASE
```

The hostname:

```text
postgres
```

works because Docker Compose places the services on a network where services can find each other by service name.

---

## PostgreSQL Service

Our PostgreSQL service is:

```yaml
postgres:
  image: postgres:18
  env_file:
    - .env.docker
  volumes:
    - postgres_data:/var/lib/postgresql
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
    interval: 5s
    timeout: 5s
    retries: 5
```

---

## PostgreSQL Image

```yaml
image: postgres:18
```

Unlike our FastAPI service, we do not need to build PostgreSQL ourselves.

We use the official PostgreSQL image.

```text
FastAPI
→ Our Dockerfile
→ Our custom image

PostgreSQL
→ Official postgres image
→ postgres:18
```

Specifying:

```text
:18
```

pins the PostgreSQL major version instead of relying on an unspecified/default image tag.

---

## PostgreSQL Environment Variables

The official PostgreSQL Docker image understands special environment variables such as:

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

These variables are defined by the PostgreSQL Docker image and are used when initializing a new PostgreSQL database.

For example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=some_password
POSTGRES_DB=social_api
```

means PostgreSQL is initialized with:

```text
User     → postgres
Password → some_password
Database → social_api
```

FastAPI must then use matching credentials in its database URL:

```text
postgresql://postgres:some_password@postgres:5432/social_api
```

Therefore:

```text
POSTGRES_USER ────────┐
POSTGRES_PASSWORD ────┼──→ DATABASE_URL
POSTGRES_DB ──────────┘
```

The values themselves are chosen/configured by us for the environment.

They should not be hardcoded into a Compose file committed to Git.

---

## `.env.docker`

Our `.env.docker` contains the configuration needed by the Dockerized application.

Conceptually:

```env
DATABASE_URL=postgresql://USER:PASSWORD@postgres:5432/DATABASE

ALGORITHM=...
TOKEN_EXPIRY_TIME=...
KEY=...

POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
```

The FastAPI application uses:

```text
DATABASE_URL
ALGORITHM
TOKEN_EXPIRY_TIME
KEY
```

The official PostgreSQL image uses:

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

Both services can receive the same environment file, while each application uses only the variables it understands.

Because this file contains secrets, it should not be committed to Git.

---

## `.dockerignore`

Our Dockerfile contains:

```dockerfile
COPY . .
```

Without exclusions, Docker could copy unnecessary or sensitive project files into the image.

`.dockerignore` tells Docker which files/directories should be excluded from the build context.

Example:

```text
.env
.env.*
.venv/
venv/
__pycache__/
*.pyc
.git/
.gitignore
.pytest_cache/
```

### `.env`

Prevents the normal environment file and its secrets from being copied into the image.

### `.env.*`

Matches files such as:

```text
.env.docker
.env.production
.env.development
.env.local
```

`.env.*` does not match the plain `.env` file, which is why both patterns are included:

```text
.env
.env.*
```

### `.venv/` and `venv/`

Local Python virtual environments are not needed inside the Docker image.

The container has its own Python environment and installs dependencies using `requirements.txt`.

### `__pycache__/` and `*.pyc`

Exclude generated Python bytecode/cache files.

### `.git/`

The application's Git repository history is not needed inside the running image.

### `.gitignore`

Git's ignore configuration is not needed by the running application.

### `.pytest_cache/`

Generated pytest cache files do not need to be included in the application image.

---

## `.gitignore` vs `.dockerignore`

These solve different problems.

```text
.gitignore
     ↓
Controls what Git tracks
     ↓
Protects files from being committed/pushed
```

```text
.dockerignore
     ↓
Controls what Docker includes in build context
     ↓
Protects files from being copied into the image
```

Putting `.env` in `.gitignore` does NOT automatically prevent Docker from copying it.

Therefore sensitive environment files should be protected appropriately from both Git and Docker builds.

---

## PostgreSQL Named Volume

Containers are replaceable, so PostgreSQL data should not depend on one particular container.

We attach a named volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql
```

and declare it at the bottom of the Compose file:

```yaml
volumes:
  postgres_data:
```

Conceptually:

```text
PostgreSQL Container
        ↓
/var/lib/postgresql
        ↓
postgres_data
        ↓
Persistent Database Files
```

If the PostgreSQL container is removed and recreated:

```text
Old Postgres Container ❌

postgres_data ✅

New Postgres Container ✅
        ↓
same volume
        ↓
existing database data
```

### PostgreSQL 18 Note

For PostgreSQL 18+, the Docker image uses a version-specific data layout.

Therefore we mount:

```text
/var/lib/postgresql
```

rather than the older commonly used:

```text
/var/lib/postgresql/data
```

This is important when using the PostgreSQL 18 Docker image.

---

## PostgreSQL Healthcheck

Starting a PostgreSQL container does not necessarily mean PostgreSQL is immediately ready to accept connections.

Therefore we use:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
  interval: 5s
  timeout: 5s
  retries: 5
```

`pg_isready` is a PostgreSQL utility that checks whether PostgreSQL is ready to accept connections.

Conceptually:

```text
Postgres container starts
        ↓
PostgreSQL initializes
        ↓
Healthcheck runs
        ↓
pg_isready
        ↓
PostgreSQL ready
        ↓
Container becomes healthy
```

`interval: 5s`

means Docker performs the check every 5 seconds.

`timeout: 5s`

means one check can wait up to 5 seconds.

`retries: 5`

means Docker allows several failed checks before considering the service unhealthy.

A Docker healthcheck is not the same thing as application/unit testing. It is used to determine whether a service is operational/ready.

---

## Environment Variables Inside Healthcheck

The healthcheck contains:

```text
$$POSTGRES_USER
$$POSTGRES_DB
```

Inside a Linux shell:

```text
$POSTGRES_USER
```

means:

> Get the value of the `POSTGRES_USER` environment variable.

In a Compose file, `$` also has meaning to Compose.

Using:

```text
$$POSTGRES_USER
```

escapes the `$` for Compose so that the variable can be evaluated later inside the container.

Conceptually:

```text
Compose file
$$POSTGRES_USER
        ↓
Docker Compose
        ↓
$POSTGRES_USER
        ↓
Container shell
        ↓
Value of POSTGRES_USER
```

This is different from Compose interpolation such as:

```text
${POSTGRES_USER}
```

where Compose itself substitutes the value while processing the Compose configuration.

---

## `depends_on`

Our API depends on PostgreSQL:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

This tells Compose not to start the API service until the PostgreSQL service passes its healthcheck.

Without readiness checking:

```text
Postgres container starts
        ↓
PostgreSQL still initializing
        ↓
FastAPI starts
        ↓
FastAPI tries database connection
        ↓
Connection may fail
```

With the healthcheck:

```text
Postgres container starts
        ↓
PostgreSQL initializes
        ↓
Healthcheck succeeds
        ↓
Postgres becomes healthy
        ↓
FastAPI starts
```

---

## Complete Development Compose Structure

Our development setup is conceptually:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./:/usr/src/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    env_file:
      - .env.docker
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:18
    env_file:
      - .env.docker
    volumes:
      - postgres_data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

This is a development-oriented configuration because it uses:

```text
Bind mount
--reload
Local PostgreSQL container
```

---

## Alembic with Docker

Creating a fresh PostgreSQL container/database does not automatically create our application's tables.

PostgreSQL provides the database server, while Alembic manages our application's database schema.

After starting a fresh database, migrations can be applied from the running API container:

```bash
docker compose exec api alembic upgrade head
```

Breakdown:

```text
docker compose exec
→ execute a command inside a running Compose service

api
→ execute it inside the API container

alembic upgrade head
→ apply all migrations to the latest revision
```

Conceptually:

```text
API Container
      ↓
Alembic
      ↓
DATABASE_URL
      ↓
Postgres Container
      ↓
Create/update application tables
```

Without applying the migrations, FastAPI may successfully connect to PostgreSQL but fail with errors such as:

```text
relation "users" does not exist
```

because the database exists but the application's tables have not yet been created.

---

## Essential Docker Compose Commands

### Start Services

```bash
docker compose up
```

Starts the Compose services and keeps the terminal attached to their logs.

---

### Start and Build

```bash
docker compose up --build
```

Builds/rebuilds the required image and then starts the services.

Useful after changes that affect the image, such as:

```text
Dockerfile
requirements.txt
```

---

### Detached Mode

```bash
docker compose up -d
```

`-d` means detached mode.

The containers run in the background and the terminal becomes available again.

Options can also be combined:

```bash
docker compose up -d --build
```

---

### View Running Compose Services

```bash
docker compose ps
```

Shows the containers/services belonging to the Compose application and their current status.

---

### View Logs

```bash
docker compose logs
```

Shows logs from the Compose services.

Follow logs continuously:

```bash
docker compose logs -f
```

View logs from one service:

```bash
docker compose logs api
```

or:

```bash
docker compose logs postgres
```

---

### Execute Commands Inside a Container

```bash
docker compose exec api COMMAND
```

For example:

```bash
docker compose exec api alembic upgrade head
```

We can also open a shell inside the API container:

```bash
docker compose exec api bash
```

To leave the shell:

```bash
exit
```

---

### Stop and Remove Compose Containers

```bash
docker compose down
```

Stops and removes the Compose containers and network.

Named volumes remain.

Therefore:

```text
docker compose down

Containers ❌
Compose network ❌
postgres_data ✅
Database data ✅
```

---

### Remove Containers and Volumes

```bash
docker compose down -v
```

The `-v` option also removes named volumes.

Therefore:

```text
docker compose down -v

Containers ❌
Compose network ❌
postgres_data ❌
Database data ❌
```

This should be used carefully when the volume contains important database data.

---

## Development vs Production Compose

Our current Compose configuration is designed for development.

Development commonly benefits from:

```text
Bind mounts
Automatic reload
Local development database
Development environment variables
```

Production usually differs:

```text
No source-code bind mount
No --reload
Code comes from the built image
Production environment/secrets
Stable image/version
Production database configuration
```

Docker does not require every project to have exactly two Compose files.

Separate development and production configurations are useful when the environments need different behavior.

For this project, we are keeping:

```text
docker-compose.yml
```

as the development configuration and will create a separate production configuration.

---
