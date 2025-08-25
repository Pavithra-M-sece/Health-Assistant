# 🏥 Healthcare Assistant App

A modern healthcare application with AI-powered symptom analysis, medicine management, and doctor consultations.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 14+
- MongoDB
- npm

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd healthcare-assistant-app
```

2. **Install dependencies**
```bash
# Install backend dependencies
cd server
npm install
cd ..

# Install frontend dependencies
cd client
npm install
cd ..

# Install AI service dependencies
cd ai_service
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
cd ..
```

## 🎯 Running the App

### Quick Start (Recommended)
```bash
# Start all services with one command
python start_services.py

# Or using npm
npm start
```

### Manual Start (Alternative)
```bash
# Terminal 1: Start MongoDB
mongod --dbpath data\db

# Terminal 2: Start Backend
cd server
npm start

# Terminal 3: Start Frontend
cd client
npm start

# Terminal 4: Start AI Service
cd ai_service
venv\Scripts\python app.py
```

### Stopping Services
```bash
# Stop all services
python stop_services.py

# Or press Ctrl+C in the terminal running start_services.py
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **AI Service**: http://localhost:5001
- **MongoDB**: localhost:27017

## 🛠️ Features

### Frontend
- Modern, responsive UI with dark/light theme
- User authentication (register/login)
- Dashboard with health statistics
- Symptom analysis with AI
- Medicine management
- Doctor consultations
- Health tips and alerts

### Backend
- RESTful API with Express.js
- MongoDB database with Mongoose
- JWT authentication
- CORS enabled
- Error handling middleware

### AI Service
- Flask-based AI service
- Symptom analysis using machine learning
- Health recommendations

## 📁 Project Structure

```
healthcare-assistant-app/
├── client/                 # React frontend
│   ├── src/
│   │   ├── App.js         # Main app component
│   │   ├── App.css        # Modern styling
│   │   ├── Dashboard.js   # Dashboard component
│   │   ├── Login.js       # Login component
│   │   ├── Register.js    # Registration component
│   │   └── ...
│   └── package.json
├── server/                 # Node.js backend
│   ├── index.js           # Main server file
│   ├── routes/            # API routes
│   ├── models/            # Database models
│   ├── middleware/        # Middleware functions
│   └── package.json
├── ai_service/            # Python AI service
│   ├── app.py            # Flask AI service
│   ├── requirements.txt  # Python dependencies
│   └── venv/             # Virtual environment
├── start_services.py     # Python service manager
├── stop_services.py      # Service stopper
├── package.json          # Root package.json
└── .gitignore           # Git ignore rules
```

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional healthcare interface
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Toggle between themes
- **Smooth Animations**: CSS transitions and animations
- **Loading States**: User feedback during operations
- **Error Handling**: Clear error messages and validation
- **Accessibility**: Keyboard navigation and screen reader support

## 🔧 Development

### Adding New Features
1. Create components in `client/src/`
2. Add API routes in `server/routes/`
3. Update database models in `server/models/`
4. Test thoroughly before committing

### Debugging
- Check browser console for frontend errors
- Monitor server logs for backend issues
- Verify MongoDB connection
- Check AI service logs

## 🧹 Project Cleanup

This project has been cleaned up to remove redundant files and simplify the structure:

### Removed Files
- Redundant startup scripts (`start_services_improved.py`, `start_services.bat`, etc.)
- Test files (`test_backend.py`)
- Manual documentation (`MANUAL_STARTUP.md`)
- Generated files (`node_modules/`, `package-lock.json`)
- Default React README in client directory

### Current Structure
The project now has a clean, minimal structure with only essential files:
- **Core Services**: `client/`, `server/`, `ai_service/`
- **Service Management**: `start_services.py`, `stop_services.py`
- **Configuration**: `package.json`, `.gitignore`
- **Documentation**: `README.md`
- **Data**: `data/` (MongoDB data directory)

## 🚨 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is installed and running
   - Check if data directory exists: `data\db`

2. **Port Already in Use**
   - Stop existing services: `python stop_services.py`
   - Or manually kill processes using Task Manager

3. **Python Virtual Environment Issues**
   - Recreate virtual environment: `python -m venv venv`
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Node Modules Issues**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Coding! 🎉** 