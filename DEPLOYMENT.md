# Production Deployment Guide for Director

This guide provides comprehensive instructions for deploying the Director application with voice chat to production environments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Database Setup](#database-setup)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Security Hardening](#security-hardening)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying to production, verify the following:

- [ ] All environment variables are configured securely
- [ ] Database migrations have been tested
- [ ] API keys for all integrations are valid
- [ ] SSL/TLS certificates are obtained
- [ ] Frontend and backend builds are tested locally
- [ ] Docker images are built and tested
- [ ] All dependencies are pinned to specific versions
- [ ] Error handling and logging are properly configured
- [ ] Rate limiting is enabled
- [ ] CORS is restricted to production domains only
- [ ] Database backups are configured
- [ ] Monitoring and alerting are set up

---

## Environment Configuration

### 1. Backend Environment Variables

Create a `.env.production` file in the backend directory:

```bash
# Application Environment
SERVER_ENV=production
SERVER_DEBUG=False
SERVER_TESTING=False
SERVER_SECRET_KEY=<strong-random-secret-key>
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Database Configuration
SERVER_DB_TYPE=postgres  # or sqlite for small deployments
DATABASE_URL=postgresql://user:password@db-host:5432/director_prod

# API Keys and Services
OPENAI_API_KEY=sk-...
VIDEO_DB_API_KEY=...
ELEVENLABS_API_KEY=...

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Voice Configuration
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800  # 50MB

# Security
JWT_SECRET=<strong-random-secret>
JWT_EXPIRY=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/director/backend.log

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=...
SMTP_PASSWORD=...
ADMIN_EMAIL=admin@yourdomain.com
```

### 2. Frontend Environment Variables

Create a `.env.production` file in the frontend directory:

```bash
VITE_APP_BACKEND_URL=https://api.yourdomain.com
VITE_PORT=3000
VITE_OPEN_BROWSER=false

# Analytics
VITE_ANALYTICS_ID=...
```

### 3. Generate Secret Keys

Generate secure random keys:

```bash
# On Linux/Mac
openssl rand -base64 32

# For multiple keys, run the command multiple times
```

---

## Database Setup

### PostgreSQL (Recommended for Production)

#### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### 2. Create Database and User

```sql
-- Connect to PostgreSQL
sudo -u postgres psql

-- Create production database
CREATE DATABASE director_prod;

-- Create production user
CREATE USER director_prod WITH ENCRYPTED PASSWORD 'strong_password_here';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE director_prod TO director_prod;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO director_prod;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO director_prod;

-- Exit
\q
```

#### 3. Configure PostgreSQL for Production

Edit `/etc/postgresql/*/main/postgresql.conf`:

```conf
# Connection settings
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB

# WAL (Write-Ahead Logging) settings
wal_level = replica
max_wal_senders = 3

# Query planning
random_page_cost = 1.1
effective_io_concurrency = 200
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

#### 4. Initialize Database

```bash
cd backend
source venv/bin/activate
python director/db/postgres/initialize.py
```

### SQLite (Small Deployments)

For deployments with low traffic, SQLite is acceptable:

```bash
cd backend
source venv/bin/activate
python director/db/sqlite/initialize.py
```

---

## Docker Deployment

### 1. Build Docker Images

#### Backend Image

```bash
cd backend
docker build -t director-backend:latest \
  --build-arg ENVIRONMENT=production \
  -f Dockerfile .
```

#### Frontend Image

```bash
cd frontend
docker build -t director-frontend:latest \
  --build-arg ENVIRONMENT=production \
  -f Dockerfile .
```

### 2. Push to Registry

```bash
# For Docker Hub
docker tag director-backend:latest your-username/director-backend:latest
docker push your-username/director-backend:latest

docker tag director-frontend:latest your-username/director-frontend:latest
docker push your-username/director-frontend:latest

# For AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com

docker tag director-backend:latest <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/director-backend:latest
docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/director-backend:latest
```

### 3. Docker Compose for Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: director-postgres
    environment:
      POSTGRES_DB: director_prod
      POSTGRES_USER: director_prod
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U director_prod"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    image: director-backend:latest
    container_name: director-backend
    environment:
      SERVER_ENV: production
      SERVER_HOST: 0.0.0.0
      SERVER_PORT: 8000
      SERVER_DB_TYPE: postgres
      DATABASE_URL: postgresql://director_prod:${DB_PASSWORD}@postgres:5432/director_prod
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      VIDEO_DB_API_KEY: ${VIDEO_DB_API_KEY}
      ELEVENLABS_API_KEY: ${ELEVENLABS_API_KEY}
      CORS_ORIGINS: https://yourdomain.com
      SERVER_SECRET_KEY: ${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/var/log/director
      - ./audio_responses:/app/audio_responses
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/config/check"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: director-frontend:latest
    container_name: director-frontend
    environment:
      VITE_APP_BACKEND_URL: https://api.yourdomain.com
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl/certs:/etc/nginx/certs:ro
    restart: always
    depends_on:
      - backend

volumes:
  postgres_data:

networks:
  default:
    name: director-network
```

### 4. Run with Docker Compose

```bash
# Create .env file with production values
cp .env.example .env.production

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Stop services
docker-compose -f docker-compose.prod.yml down
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: EC2 with Docker

1. **Launch EC2 Instance**

```bash
# Ubuntu 22.04 LTS recommended
# Instance type: t3.large or larger
# Security group: Allow ports 80, 443, 8000
```

2. **Install Docker and Docker Compose**

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

3. **Deploy**

```bash
git clone <repository>
cd director
docker-compose -f docker-compose.prod.yml up -d
```

#### Option 2: RDS for Database

```bash
# Create RDS PostgreSQL instance in AWS Console
# Security group: Allow inbound from EC2 security group

# Connection string format:
postgresql://director_prod:password@director-db.xxxx.us-east-1.rds.amazonaws.com:5432/director_prod
```

### Heroku Deployment

1. **Install Heroku CLI**

```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. **Create Procfile**

```
web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT director.entrypoint.api.server:app
worker: cd backend && celery -A director.tasks worker
```

3. **Deploy**

```bash
heroku create your-app-name
git push heroku main
heroku config:set SERVER_ENV=production
heroku config:set OPENAI_API_KEY=sk-...
heroku open /voice
```

### Vercel Deployment (Frontend Only)

1. **Build Frontend**

```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**

```bash
npm i -g vercel
vercel --prod
```

---

## Security Hardening

### 1. HTTPS/TLS Configuration

#### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

#### Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Proxy to backend
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy to frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 2. Rate Limiting

Add to backend configuration:

```python
# backend/director/entrypoint/api/middleware.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# In create_app():
limiter.init_app(app)

# Apply to endpoints:
@app.route('/voice/transcribe', methods=['POST'])
@limiter.limit("10 per minute")
def transcribe_audio():
    pass
```

### 3. API Authentication

Implement JWT-based authentication:

```python
# backend/director/utils/auth.py
from functools import wraps
import jwt

def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Missing authorization token'}, 401
        try:
            payload = jwt.decode(token.split(' ')[1], app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = payload
        except:
            return {'error': 'Invalid token'}, 401
        return f(*args, **kwargs)
    return decorated_function

# Usage:
@app.route('/voice/chat', methods=['POST'])
@require_token
def voice_chat():
    user_id = request.user['user_id']
    # Process request
```

### 4. Input Validation

```python
# Validate audio file size
MAX_AUDIO_SIZE = 52428800  # 50MB

@app.route('/voice/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    if file.size > MAX_AUDIO_SIZE:
        return {'error': 'File too large'}, 413
    
    # Check MIME type
    if file.content_type not in ['audio/wav', 'audio/mp3', 'audio/ogg']:
        return {'error': 'Invalid audio format'}, 400
```

---

## Monitoring and Logging

### 1. Application Logging

Configure logging in backend:

```python
# backend/director/entrypoint/api/server.py
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.FileHandler('/var/log/director/app.log')
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

### 2. Monitoring with Prometheus

```python
# backend/director/entrypoint/api/metrics.py
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
request_count = Counter('director_requests_total', 'Total requests')
request_duration = Histogram('director_request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        request_duration.observe(duration)
    request_count.inc()
    return response

# Expose metrics endpoint
start_http_server(8001)
```

### 3. Error Tracking with Sentry

```python
# backend/requirements.txt
sentry-sdk==1.45.0

# backend/director/entrypoint/api/server.py
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("SERVER_ENV"),
    traces_sample_rate=0.1
)
```

---

## Backup and Recovery

### 1. Database Backups

```bash
# Backup PostgreSQL
pg_dump -h localhost -U director_prod director_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql -h localhost -U director_prod director_prod < backup_20240101_120000.sql

# Automated daily backups with cron
0 2 * * * pg_dump -h localhost -U director_prod director_prod | gzip > /backups/backup_$(date +\%Y\%m\%d).sql.gz

# Cleanup old backups (keep last 30 days)
0 3 * * * find /backups -name "backup_*.sql.gz" -mtime +30 -delete
```

### 2. Audio Files Backup

```bash
# Backup audio responses
tar -czf audio_backup_$(date +%Y%m%d).tar.gz audio_responses/

# S3 backup
aws s3 sync audio_responses/ s3://your-bucket/audio_responses/
```

---

## Performance Optimization

### 1. Frontend Optimization

```javascript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import compression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    vue(),
    compression({
      algorithm: 'brotli',
      ext: '.br',
    })
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'voice': ['./src/components/AudioRecorder.vue', './src/components/VoicePlayback.vue']
        }
      }
    },
    minify: 'terser',
    sourcemap: false
  }
})
```

### 2. Backend Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'RedisCache'})

@app.route('/agent')
@cache.cached(timeout=300)
def get_agents():
    # This endpoint result will be cached for 5 minutes
    pass
```

### 3. CDN Configuration

Use a CDN (CloudFlare, AWS CloudFront) for:
- Static assets
- Audio files
- API responses

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check connection
psql -h db-host -U director_prod -d director_prod -c "SELECT 1"

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql.log
```

#### 2. Audio Processing Failures

```bash
# Check API keys
echo $OPENAI_API_KEY
echo $ELEVENLABS_API_KEY

# Test transcription endpoint
curl -X POST -F "file=@audio.wav" http://localhost:8000/voice/transcribe
```

#### 3. Memory Issues

```bash
# Monitor memory usage
docker stats director-backend

# Adjust container limits
docker update --memory 2g director-backend
```

#### 4. Slow Response Times

```bash
# Enable query logging
SET log_statement = 'all';

# Profile backend
python -m cProfile -s cumulative director/entrypoint/api/server.py
```

---

## Rollback Procedure

If issues occur after deployment:

```bash
# Get previous image tag
docker images director-backend

# Revert to previous version
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d director-backend:previous-tag

# Database rollback
pg_restore -d director_prod backup_20240101_120000.sql.gz
```

---

## Support and Resources

- Documentation: `/docs`
- Issue Tracker: https://github.com/Gokul2580/dir/issues
- Discord: [Community link]
- Email: support@yourdomain.com

---

**Last Updated**: 2024
**Maintained By**: Your Team
