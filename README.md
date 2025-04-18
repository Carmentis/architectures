# Docker Compose Infrastructure

This repository contains `docker-compose.yml` files used to launch and manage a group of Docker containers for building
and maintaining infrastructure. The setup is designed to simplify the orchestration of multiple services, making it
easier to manage dependencies and scale your infrastructure.

## List of architectures
We describe below what you can deploy. Indeed, depending on your need, not all services will be interesting.
For example, a developer wanting to test our product should be able to run the full Carmentis ecosystem 
locally. On the other side, a developer wanting to develop its own application only needs a sub-part of the 
ecosystem, the other elements being maintained by Carmentis.  Only few combinations of servers are relevant, and to make
the deployment more easy, we have developed this repository listing meaningful architectures.

In this repository, each folder represents an *architecture*, the list of embedded services for each  architecture
being presented below:

| Folder name              | Node | Operator | Explorer | Exchange | Email Oracle | File-Sign |
|--------------------------|------|---------|----------|----------|--------------|-----------|
| `standard` (recommended) |  Yes | Yes     |          |          |              |           |
| `operator`               |      | Yes     |          |          |              |           |
| `full-infrastructure`    | Yes  | Yes     | Yes      | Yes      | Yes          | Yes       |


## Deploy an architecture

1. **Download the repository** and **select the architecture** you want based on your need. 
For the sake of clarity, suppose we want to deploy a `standard` architecture.
2. **Configure the .env** file based on the configuration and own infrastructure.
3. **Launch the architecture** using docker-compose.

We provide you the required command
```shell
ENV=standard
cp $ENV/docker-compose.yml && docker-compose up
```

To launch the architecture in a detached way, use the following `docker-compose up -d` command. To down the architecture, use
the following `docker-compose down` command.


## Prerequisites

- [Docker](https://www.docker.com/) installed on your system.
- [Docker Compose](https://docs.docker.com/compose/) installed.

Ensure that Docker and Docker Compose are properly installed and configured before proceeding.


### Additional Docker Compose Commands
We recall some basics of docker-compose commands:

- View running containers:
  ```bash
  docker-compose ps
  ```

- Check logs for a specific container:
  ```bash
  docker-compose logs <service-name>
  ```

- Rebuild containers after making changes:
  ```bash
  docker-compose up --build -d
  ```
