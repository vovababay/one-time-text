# One Time Text API

A simple FastAPI-based application for creating one-time text links. The text is stored temporarily using different caching backends (memory, Redis, or Memcached) and automatically expires after a specified duration.

## Features

- Create a one-time link for your text with configurable expiration time.
- Support for different cache backends:
  - Memory (default)
  - Redis
  - Memcached
- Docker support for seamless deployment.
- Easy to run locally with Python.

---

## Installation

### 1. Running with Docker Compose

Edit a `docker-compose.yml` file with the following content:

```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CACHE_BACKEND=redis
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

Run the following commands:

```bash
docker-compose up --build
```

The application will be accessible at `http://localhost:8000`.

### 2. Running with Docker (without Compose)

#### a) Using Redis:

Start a Redis container:

```bash
docker run -d --name redis-container -p 6379:6379 redis:alpine
```

Build and run the application:

```bash
docker build -t one-time-text .
docker run -d --name one-time-text --env CACHE_BACKEND=redis --env REDIS_HOST=host.docker.internal -p 8000:8000 one-time-text
```

#### b) Using Memcached:

Start a Memcached container:

```bash
docker run -d --name memcached-container -p 11211:11211 memcached:alpine
```

Build and run the application:

```bash
docker build -t one-time-text .
docker run -d --name one-time-text --env CACHE_BACKEND=memcached --env MEMCACHED_HOST=host.docker.internal -p 8000:8000 one-time-text
```

---

### 3. Running Locally with Python

#### Prerequisites:
- Python 3.11+
- Install dependencies:

```bash
pip install -r requirements.txt
```

#### Run the Application

Start the application with the desired backend:

- **Memory (default):**

```bash
CACHE_BACKEND=memory python main.py
```

- **Redis:**

```bash
CACHE_BACKEND=redis REDIS_HOST=localhost REDIS_PORT=6379 python main.py
```

- **Memcached:**

```bash
CACHE_BACKEND=memcached MEMCACHED_HOST=localhost MEMCACHED_PORT=11211 python main.py
```

The application will be accessible at `http://127.0.0.1:8000`.

---

## Environment Variables

| Variable            | Description                          | Default       |
|---------------------|--------------------------------------|---------------|
| `CACHE_BACKEND`     | Cache backend to use (`memory`, `redis`, `memcached`) | `memory`      |
| `REDIS_HOST`        | Redis server hostname                | `localhost`   |
| `REDIS_PORT`        | Redis server port                    | `6379`        |
| `REDIS_PASSWORD`    | Redis server password (optional)     | None          |
| `MEMCACHED_HOST`    | Memcached server hostname            | `localhost`   |
| `MEMCACHED_PORT`    | Memcached server port                | `11211`       |

---

## Endpoints

1. **GET `/`**  
   Displays the homepage for creating a one-time text link.
2. **GET `/get/{id}`**  
   Displays the page to receive the text.
3. **POST `/api/create`**  
   Creates a one-time text link with a specific duration.
4. Example cURL request:
   ```bash
   curl -X POST --location 'http://0.0.0.0:8000/api/create/' --header 'Content-Type: application/json' --data '{"text":"test","duration":1}'
   ```
4. **GET `/api/get/{id}`**  
   Retrieves the text if the link is valid.
    ```bash
   curl --location 'http://0.0.0.0:8000/api/get/{id}'
   ```
   



---

## Notes

- Default cache backend is `memory` if no `CACHE_BACKEND` is specified.
- Ensure that Redis or Memcached is running if you select these backends.
- Adjust `ttl` values in the code as per your requirements.

