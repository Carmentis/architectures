# Docker Compose Infrastructure

This repository contains `docker-compose.yml` files used to launch and manage a group of Docker containers for building
and maintaining infrastructure. The setup is designed to simplify the orchestration of multiple services, making it
easier to manage dependencies and scale your infrastructure.

## Repository structure
We describe below existing infrastructure that you can deploy.

| Folder name                                                                                                                                                                            | Node | Dev-Node | Operator | Workspace | Explorer | Exchange | Email Oracle | File-Sign |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|----------|----------|-----------|----------|-------|--------------|-----------|
| `validator`                                                                                                                                                                            | Yes  |       |       |        |       |       |              |           |
| `standard` <span style="display: inline-block; background-color: #4CAF50; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">recommended</span> | Yes   |       | Yes      | Yes       |       |       |              |           |
| `app-only`                                                                                                                                                                             |    |       |       |        |       |       | Yes          | Yes       |
| `full-infrastructure`                                                                                                                                                                  |      | Yes      | Yes      | Yes       | Yes      | Yes   | Yes          | Yes       |



## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system.
- [Docker Compose](https://docs.docker.com/compose/) installed.

Ensure that Docker and Docker Compose are properly installed and configured before proceeding.

### Usage

First, **download the repository** and **select the architecture** you want based on your need. For the sake of clarity, suppose we want to deploy a
`standard` architecture. Second, **configure the .env** file based on the configuration and own infrastructure. 
Finally, assuming you have a .env file in the root of the repository, **execute the following command** to launch the targeted architecture:
```shell
ENV=standard
cp $ENV/docker-compose.yml && docker-compose up
```

To launch the architecture in a detached way, use the following `docker-compose up -d` command. To down the architecture, use
the following `docker-compose down` command.

### Additional Docker Compose Commands

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
