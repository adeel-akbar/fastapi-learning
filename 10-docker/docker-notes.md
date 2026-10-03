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

For our application, we will have:

```text
Docker Compose
      |
      ├── FastAPI Container
      |
      └── PostgreSQL Container
```

Instead of manually starting and configuring each container separately, Docker Compose allows their configuration to be defined together.

Docker Compose will be covered next.
