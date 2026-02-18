# Production-Ready URL Shortener

A containerized URL shortener built with **FastAPI**, featuring integrated caching and rate limiting.

---

## 🛠 Tech Stack
- **FastAPI** – Backend API
- **PostgreSQL** – Persistent storage
- **Redis** – 24h caching
- **Nginx** – Reverse proxy
- **Docker Compose** – Orchestration

---

## 🏗 Architecture
Client → Nginx → FastAPI → (PostgreSQL + Redis)

---

## ✨ Features
- Create and redirect short URLs
- Redis caching (24h TTL)
- Rate limiting (100 req/min/IP)
- Health checks
- Non-root containers
- Production-ready Docker setup

---

## 📋 Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

---

## 🚀 Quick Start

### 1️⃣ Setup Environment
cp .env.example .env
(Edit values if needed)

### 2️⃣ Start Services
docker-compose up -d

### 3️⃣ Verify
docker-compose ps
curl http://localhost/health

**Expected Response:**
{
  "status": "healthy",
  "database": "healthy",
  "redis": "healthy"
}

---

## 🌐 Exposed Service
| Service | URL |
| :--- | :--- |
| API | http://localhost |

---

## 🛣 API Endpoints

### ✅ Health Check
curl http://localhost/health

### 🔗 Create Short URL
curl -X POST http://localhost/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url/path"}'

**Response:**
{
  "short_url": "http://localhost/abc123"
}

### Example

### 🔗 Create Short URL
curl -X POST http://localhost/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com"}'

**Response:**
{
  "short_url": "http://localhost/PO5Ea1"
}


**Status Codes:**
- 200 – Success
- 400 – Invalid URL
- 429 – Rate limit exceeded

### ↪ Redirect to Original URL
Follow redirect:
curl -L http://localhost/abc123

View redirect header only:
curl -I http://localhost/abc123

### 📄 Get URL Info (JSON instead of redirect)
curl http://localhost/abc123?format=json

**Response:**
{
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url/path",
  "will_redirect_to": "https://example.com/very/long/url/path",
  "cached": true
}

---

## 🧪 Testing Commands

### Basic Test
SHORT_URL=$(curl -s -X POST http://localhost/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}' | jq -r '.short_url')
echo "Created short URL: $SHORT_URL"
SHORT_CODE=$(echo $SHORT_URL | sed 's/.*\///')
curl -I http://localhost/$SHORT_CODE
curl http://localhost/$SHORT_CODE?format=json

### Cache Performance Test
echo "First request (cache miss):"
time curl -s http://localhost/$SHORT_CODE?format=json
echo "Second request (cache hit):"
time curl -s http://localhost/$SHORT_CODE?format=json

### Rate Limiting Test
for i in {1..105}; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)
  echo "Request $i: HTTP $HTTP_CODE"
done
(Expected: Last requests return 429)

### Load Test (Create Multiple URLs)
for i in {1..10}; do
  curl -X POST http://localhost/shorten \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://example.com/page$i\"}"
  echo ""
done

---

## 🛑 Maintenance

### View Logs
docker-compose logs
docker-compose logs -f
docker-compose logs app
docker-compose logs postgres
docker-compose logs redis
docker-compose logs nginx

### Restart
docker-compose restart
docker-compose restart app

### Stop
docker-compose down

### Remove volumes (delete data)
docker-compose down -v

---

## 📂 Project Structure
app/            # FastAPI application
nginx/          # Reverse proxy config
postgres/       # DB init scripts
docker-compose.yml
.env.example