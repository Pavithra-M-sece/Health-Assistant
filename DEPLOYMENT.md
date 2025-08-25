# Healthcare Assistant App - Deployment Guide

This guide covers multiple deployment options for the Healthcare Assistant App.

## 🚀 Quick Start

### Option 1: Simple Development Setup
```bash
# Run the main startup script
python start_app.py
```

### Option 2: Docker Deployment (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Production Server Deployment
```bash
# Linux/Ubuntu
chmod +x deploy.sh
./deploy.sh

# Windows
deploy.bat
```

## 📋 Prerequisites

### For All Deployments
- Python 3.7+
- Node.js 16+
- npm or yarn

### For Docker Deployment
- Docker
- Docker Compose

### For Production Server
- Ubuntu 20.04+ (for Linux deployment)
- Windows Server 2019+ (for Windows deployment)
- Administrator/root access

## 🔧 Detailed Deployment Methods

### 1. Development Environment

#### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd Project

# Install dependencies
cd server && npm install && cd ..
cd client && npm install && cd ..
cd ai_service && pip install -r requirements.txt && cd ..

# Start all services
python start_app.py
```

#### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- AI Service: http://localhost:5000

### 2. Docker Deployment

#### Single Container
```bash
# Build the image
docker build -t healthcare-assistant .

# Run the container
docker run -p 3000:3000 -p 5000:5000 healthcare-assistant
```

#### Multi-Service with Docker Compose
```bash
# Start all services
docker-compose up -d

# View service status
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

#### Docker Services
- **Frontend**: React app on port 3000
- **Backend**: Node.js API on port 5000
- **AI Service**: Python Flask service on port 5001
- **Nginx**: Reverse proxy on port 80
- **MongoDB**: Database on port 27017

### 3. Production Server Deployment

#### Linux/Ubuntu Server
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
- Install system dependencies
- Create application directory
- Set up Python virtual environment
- Install Node.js dependencies
- Create systemd services
- Configure Nginx
- Start all services

#### Windows Server
```cmd
# Run as Administrator
deploy.bat
```

The script will:
- Install dependencies
- Create application directory
- Set up Python virtual environment
- Install Node.js dependencies
- Create Windows services
- Start all services

#### Management Commands
```bash
# Linux
sudo systemctl start healthcare-backend
sudo systemctl start healthcare-ai
sudo systemctl restart nginx

# Windows
sc start HealthcareBackend
sc start HealthcareAI

# Or use the management script
./manage.sh start    # Linux
manage.bat start     # Windows
```

### 4. Cloud Deployment

#### AWS EC2
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Clone repository
git clone <repository-url>
cd Project

# Run deployment script
chmod +x deploy.sh
./deploy.sh
```

#### Google Cloud Platform
```bash
# Connect to your GCP instance
gcloud compute ssh your-instance-name

# Follow the same steps as AWS EC2
```

#### Azure
```bash
# Connect to your Azure VM
ssh username@your-vm-ip

# Follow the same steps as AWS EC2
```

## 🔒 Security Configuration

### Environment Variables
Create `.env` files for sensitive configuration:

```bash
# .env (root directory)
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb://localhost:27017/healthcare
JWT_SECRET=your-secret-key

# ai_service/.env
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
```

### SSL/HTTPS Setup
```bash
# Install Certbot (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration
```bash
# Ubuntu UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Or with iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 📊 Monitoring and Logs

### View Logs
```bash
# Docker
docker-compose logs -f [service-name]

# Linux systemd
sudo journalctl -u healthcare-backend -f
sudo journalctl -u healthcare-ai -f

# Windows
Get-EventLog -LogName Application -Source "Healthcare*"
```

### Health Checks
```bash
# Check service status
curl http://localhost:5000/health
curl http://localhost:5001/ai

# Docker health checks
docker-compose ps
```

### Performance Monitoring
```bash
# Monitor system resources
htop
iotop
nethogs

# Monitor application metrics
curl http://localhost:5000/metrics
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild Docker containers
docker-compose down
docker-compose up -d --build

# Or restart services
sudo systemctl restart healthcare-backend
sudo systemctl restart healthcare-ai
```

### Backup Database
```bash
# MongoDB backup
mongodump --db healthcare --out /backup/$(date +%Y%m%d)

# Restore
mongorestore --db healthcare /backup/20231201/healthcare/
```

### Database Migration
```bash
# Run migrations
cd server
npm run migrate

# Or manually
node scripts/migrate.js
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
sudo lsof -i :5000
sudo netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER /opt/healthcare-assistant
sudo chmod +x /opt/healthcare-assistant/manage.sh
```

#### Service Won't Start
```bash
# Check service status
sudo systemctl status healthcare-backend
sudo systemctl status healthcare-ai

# View detailed logs
sudo journalctl -u healthcare-backend -n 50
```

#### Docker Issues
```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Rebuild from scratch
docker-compose down -v
docker-compose up -d --build
```

### Performance Issues
```bash
# Check resource usage
docker stats
htop

# Optimize Node.js
export NODE_OPTIONS="--max-old-space-size=4096"

# Optimize Python
export PYTHONUNBUFFERED=1
```

## 📞 Support

For deployment issues:
1. Check the logs: `docker-compose logs` or `sudo journalctl`
2. Verify prerequisites are installed
3. Check firewall and network configuration
4. Review environment variables
5. Ensure sufficient system resources

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Systemd Service Management](https://systemd.io/)
- [MongoDB Deployment](https://docs.mongodb.com/manual/deployment/) 