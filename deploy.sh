#!/bin/bash

# Healthcare Assistant App - Production Deployment Script
# This script sets up the application for production deployment

set -e  # Exit on any error

echo "🚀 Healthcare Assistant App - Production Deployment"
echo "=================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm nginx git curl

# Create application directory
APP_DIR="/opt/healthcare-assistant"
echo "📁 Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or copy application files
if [ -d ".git" ]; then
    echo "📋 Copying application files..."
    cp -r . $APP_DIR/
else
    echo "📋 Application files already in place"
fi

cd $APP_DIR

# Create Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd ai_service
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd server
npm install --production
cd ..

cd client
npm install --production
npm run build
cd ..

# Create systemd service files
echo "⚙️  Creating systemd services..."

# Backend service
sudo tee /etc/systemd/system/healthcare-backend.service > /dev/null <<EOF
[Unit]
Description=Healthcare Assistant Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR/server
ExecStart=/usr/bin/node index.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=5000

[Install]
WantedBy=multi-user.target
EOF

# AI service
sudo tee /etc/systemd/system/healthcare-ai.service > /dev/null <<EOF
[Unit]
Description=Healthcare Assistant AI Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR/ai_service
ExecStart=$APP_DIR/venv/bin/python new_backend.py
Restart=always
RestartSec=10
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Nginx configuration
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/healthcare-assistant > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root $APP_DIR/client/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # AI Service
    location /ai/ {
        proxy_pass http://localhost:5000/ai/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/healthcare-assistant /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Reload systemd and start services
echo "🔄 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable healthcare-backend
sudo systemctl enable healthcare-ai
sudo systemctl start healthcare-backend
sudo systemctl start healthcare-ai
sudo systemctl restart nginx

# Create management script
echo "📝 Creating management script..."
tee $APP_DIR/manage.sh > /dev/null <<EOF
#!/bin/bash

case "\$1" in
    start)
        sudo systemctl start healthcare-backend
        sudo systemctl start healthcare-ai
        sudo systemctl start nginx
        echo "✅ Services started"
        ;;
    stop)
        sudo systemctl stop healthcare-backend
        sudo systemctl stop healthcare-ai
        sudo systemctl stop nginx
        echo "🛑 Services stopped"
        ;;
    restart)
        sudo systemctl restart healthcare-backend
        sudo systemctl restart healthcare-ai
        sudo systemctl restart nginx
        echo "🔄 Services restarted"
        ;;
    status)
        sudo systemctl status healthcare-backend
        sudo systemctl status healthcare-ai
        sudo systemctl status nginx
        ;;
    logs)
        sudo journalctl -u healthcare-backend -f
        ;;
    *)
        echo "Usage: \$0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
EOF

chmod +x $APP_DIR/manage.sh

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📍 Application URLs:"
echo "   • Frontend: http://$(hostname -I | awk '{print $1}')"
echo "   • Backend API: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "🔧 Management commands:"
echo "   • Start services: $APP_DIR/manage.sh start"
echo "   • Stop services:  $APP_DIR/manage.sh stop"
echo "   • Restart services: $APP_DIR/manage.sh restart"
echo "   • Check status: $APP_DIR/manage.sh status"
echo "   • View logs: $APP_DIR/manage.sh logs"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your domain name in Nginx if needed"
echo "   2. Set up SSL certificates with Let's Encrypt"
echo "   3. Configure firewall rules"
echo "   4. Set up monitoring and backups" 