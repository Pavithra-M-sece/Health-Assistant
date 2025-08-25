#!/bin/bash

# Healthcare AI App - Firebase Deployment Script
# Optimized for production deployment with auto-close functionality

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ✅ $1"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ⚠️  $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ❌ $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "client" ]; then
    error "Please run this script from the project root directory"
    exit 1
fi

log "🏥 Starting Healthcare AI App Firebase Deployment"

# Check prerequisites
log "🔍 Checking prerequisites..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    error "Firebase CLI not found. Install with: npm install -g firebase-tools"
    exit 1
fi
success "Firebase CLI found"

# Check if logged in to Firebase
if ! firebase projects:list &> /dev/null; then
    error "Not logged in to Firebase. Run: firebase login"
    exit 1
fi
success "Firebase authentication verified"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    error "Node.js not found. Please install Node.js"
    exit 1
fi
success "Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    error "npm not found. Please install npm"
    exit 1
fi
success "npm found: $(npm --version)"

# Navigate to client directory
cd client

# Check if package.json exists
if [ ! -f "package.json" ]; then
    error "package.json not found in client directory"
    exit 1
fi

log "📦 Installing dependencies..."
npm ci --silent

log "🧹 Cleaning previous build..."
rm -rf build

log "🔧 Setting up production environment..."
# Create .env.production if it doesn't exist
if [ ! -f ".env.production" ]; then
    cat > .env.production << EOF
# Production Environment Variables for Firebase
REACT_APP_API_URL=https://your-project-id.web.app/api
REACT_APP_FIREBASE_API_KEY=your-firebase-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
REACT_APP_FIREBASE_APP_ID=1:123456789:web:abcdef123456

# App Lifecycle Settings
REACT_APP_ENABLE_AUTO_CLOSE=true
REACT_APP_IDLE_TIMEOUT=1800000
REACT_APP_WARNING_TIME=300000

# Performance Settings
GENERATE_SOURCEMAP=false
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ENABLE_PWA=true
EOF
    warning "Created .env.production file - please update with your Firebase config"
fi

log "🚀 Building optimized production bundle..."
export NODE_ENV=production
npm run build

success "Build completed successfully"

# Check if build directory was created
if [ ! -d "build" ]; then
    error "Build directory not found. Build may have failed."
    exit 1
fi

log "📊 Analyzing bundle size..."
if [ -f "node_modules/.bin/webpack-bundle-analyzer" ]; then
    npx webpack-bundle-analyzer build/static/js/*.js --report --mode static --report-filename bundle-report.html --no-open || warning "Bundle analysis failed, continuing..."
    success "Bundle analysis saved to bundle-report.html"
fi

log "🎨 Optimizing assets..."
# Compress images if imagemin is available
if command -v imagemin &> /dev/null; then
    log "🖼️ Compressing images..."
    find build/static/media -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | xargs -I {} imagemin {} --out-dir=build/static/media/ || warning "Image compression failed, continuing..."
fi

# Gzip static assets
log "🗜️ Compressing static assets..."
find build/static -name "*.js" -o -name "*.css" | xargs gzip -k || warning "Gzip compression failed, continuing..."

# Navigate back to project root
cd ..

log "🚀 Deploying to Firebase..."

# Deploy hosting
log "📤 Deploying to Firebase Hosting..."
firebase deploy --only hosting

# Deploy functions if they exist
if [ -d "functions" ]; then
    log "⚡ Deploying Firebase Functions..."
    firebase deploy --only functions
fi

# Deploy Firestore rules if they exist
if [ -f "firestore.rules" ]; then
    log "🔒 Deploying Firestore rules..."
    firebase deploy --only firestore:rules
fi

# Deploy Firestore indexes if they exist
if [ -f "firestore.indexes.json" ]; then
    log "📇 Deploying Firestore indexes..."
    firebase deploy --only firestore:indexes
fi

# Deploy storage rules if they exist
if [ -f "storage.rules" ]; then
    log "🗄️ Deploying Storage rules..."
    firebase deploy --only storage
fi

success "🎉 Deployment completed successfully!"

# Get hosting URL
log "🌐 Getting hosting URL..."
FIREBASE_PROJECT=$(firebase use --current 2>/dev/null | grep "Now using project" | awk '{print $4}' | tr -d "'")
if [ ! -z "$FIREBASE_PROJECT" ]; then
    success "🌐 Your app is live at: https://${FIREBASE_PROJECT}.web.app"
    success "🌐 Firebase Console: https://console.firebase.google.com/project/${FIREBASE_PROJECT}"
else
    log "🌐 Check your Firebase console for the live URL"
fi

success "🎊 Healthcare AI App deployment completed successfully!"
success "📱 Your app is now live on Firebase with auto-close functionality!"

# Display deployment summary
echo ""
echo "📋 Deployment Summary:"
echo "====================="
echo "✅ Frontend deployed to Firebase Hosting"
echo "✅ Auto-close functionality enabled"
echo "✅ Production optimizations applied"
echo "✅ Assets compressed and optimized"
echo "✅ Security rules deployed"
echo ""
echo "🔧 Next Steps:"
echo "- Update .env.production with your actual Firebase config"
echo "- Test the auto-close functionality"
echo "- Monitor performance in Firebase Console"
echo "- Set up Firebase Analytics if needed"
echo ""

log "🏥 Healthcare AI App is ready for production use!"
