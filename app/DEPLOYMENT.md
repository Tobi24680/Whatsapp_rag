# Docker Deployment Guide

## Prerequisites
- Docker installed on your machine
- Docker Compose installed

## Quick Start

### 1. Prepare Your Environment File
Make sure your `.env` file contains:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
OPENAI_API_KEY=your_openai_api_key
```

### 2. Build and Run with Docker Compose (Easiest)
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 3. Or Build and Run with Docker Commands
```bash
# Build the image
docker build -t whatsapp-rag-bot .

# Run the container
docker run -d \
  --name whatsapp-rag-bot \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.env:/app/.env \
  whatsapp-rag-bot

# View logs
docker logs -f whatsapp-rag-bot

# Stop the container
docker stop whatsapp-rag-bot
docker rm whatsapp-rag-bot
```

## Testing

Once running, test the API:
```bash
curl http://localhost:8000/
```

Expected response: `{"status":"ok"}`

## Exposing to Internet (for Twilio Webhook)

You have several options:

### Option 1: ngrok (Free & Easy for Testing)
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
```
Copy the HTTPS URL and set it in Twilio Console:
`https://your-ngrok-url.ngrok.io/whatsapp`

### Option 2: Deploy to Cloud (Production)

**Render.com (Free Tier Available)**
1. Push your code to GitHub
2. Create new Web Service on Render
3. Connect your repo
4. Set environment variables
5. Deploy

**Railway.app (Free Tier Available)**
1. Push your code to GitHub
2. Create new project on Railway
3. Connect your repo
4. Add environment variables
5. Deploy

**DigitalOcean App Platform**
1. Push to GitHub
2. Create new App
3. Configure environment variables
4. Deploy

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

### Port already in use
Change port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Permission issues with data folder
```bash
# Create data directories with correct permissions
mkdir -p data/uploads data/vector_db
chmod -R 777 data/
```

## Update Your Application

```bash
# Stop container
docker-compose down

# Rebuild with latest code
docker-compose build --no-cache

# Start again
docker-compose up -d
```

## Production Considerations

1. **Use a reverse proxy** (nginx) for HTTPS
2. **Set up proper logging** with log rotation
3. **Monitor container health**
4. **Backup the data/ folder regularly**
5. **Use Docker secrets** for sensitive environment variables
6. **Set resource limits** in docker-compose.yml

## Setting Up Twilio Webhook

1. Go to Twilio Console → Messaging → WhatsApp Sandbox
2. Set webhook URL: `https://your-domain.com/whatsapp`
3. Method: POST
4. Save configuration

## Monitoring

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats whatsapp-rag-bot

# Access container shell
docker-compose exec whatsapp-rag whatsapp-rag bash
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove image
docker rmi whatsapp-rag-bot

# Clean up all unused Docker resources
docker system prune -a
```
