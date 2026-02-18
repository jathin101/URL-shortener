# URL Shortener

A high-performance URL shortener built with FastAPI, PostgreSQL, Redis, and Nginx.

## Architecture

```
┌─────────┐      ┌───────────┐      ┌──────────────┐
│ Client  │─────▶│   Nginx   │─────▶│  FastAPI App │
└─────────┘      │  (Port 80)│      │  (Port 8000) │
                 └───────────┘      └──────┬───────┘
                                           │
                      ┌────────────────────|
                      │                    │                    
                      ▼                    ▼
                ┌──────────┐         ┌─────────┐
                │PostgreSQL│         │  Redis  │
                │(Port 5432)│         │(Port 6379)│
                └──────────┘         └─────────┘
```

## Features

- **FastAPI** - High-performance async Python web framework
- **PostgreSQL** - Persistent URL storage
- **Redis** - 24-hour caching for fast redirects
- **Nginx** - Reverse proxy
- **Rate Limiting** - 100 requests/minute per IP
- **Auto-generated API docs** - Swagger UI at `/docs`

## Quick Start

```bash
# Start all services
docker-compose up -d

# Check health
curl http://localhost/health

# Stop services
docker-compose down
```

## API Endpoints

### 1. Health Check
```bash
GET http://localhost/health
```

### 2. Create Short URL
```bash
POST http://localhost/shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url"
}

# Response
{
  "short_url": "http://localhost/abc123"
}
```

### 3. Redirect to Original URL
```bash
GET http://localhost/{short_code}
# Returns 302 redirect to original URL
```

### 4. Get URL Info (JSON)
```bash
GET http://localhost/{short_code}?format=json

# Response
{
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url",
  "cached": true
}
```

### 5. API Documentation
- Swagger UI: `http://localhost:80/docs`

## Testing with Thunder Client (VS Code)

1. **Health Check**: `GET http://localhost/health`
2. **Create URL**: `POST http://localhost/shorten` with JSON body `{"url": "https://github.com"}`
3. **Get Info**: `GET http://localhost/abc123?format=json`
4. **Test Redirect**: `GET http://localhost/abc123`

## Configuration

Environment variables (`.env` file):

```bash
# Database
POSTGRES_USER=urluser
POSTGRES_PASSWORD=urlpass
POSTGRES_DB=urlshortener

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Application
BASE_URL=http://localhost
```

## Database Schema

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(8) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Docker Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop and remove all (preserves data)
docker-compose down

# Stop and remove all (deletes data)
docker-compose down -v
```

## Troubleshooting

```bash
# Check logs
docker-compose logs app

# Test database
docker exec -it url-shortener-postgres psql -U urluser -d urlshortener -c "\dt"

# Test Redis
docker exec -it url-shortener-redis redis-cli ping

# View cached URLs
docker exec -it url-shortener-redis redis-cli KEYS "url:*"
```

## Project Structure

```
url-shortener/
├── app/
│   ├── src/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── redis_client.py
│   │   ├── shortener.py
│   │   └── routers/
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/nginx.conf
├── postgres/init.sql
├── docker-compose.yml
└── README.md
```

## License

MIT License

