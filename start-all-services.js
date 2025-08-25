const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Unified Service Launcher
 * Starts all three services: AI Service, Backend Server, and React Frontend
 */
class ServiceLauncher {
  constructor() {
    this.processes = [];
    this.projectRoot = __dirname;
    this.services = {
      ai: {
        name: 'AI Service',
        command: process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python',
        args: ['app.py'],
        cwd: path.join(this.projectRoot, 'ai_service'),
        port: 5001,
        color: '\x1b[36m', // Cyan
        readyMessage: 'Running on'
      },
      backend: {
        name: 'Backend Server',
        command: 'node',
        args: ['index.js'],
        cwd: path.join(this.projectRoot, 'server'),
        port: 5000,
        color: '\x1b[32m', // Green
        readyMessage: 'Server running on port'
      },
      frontend: {
        name: 'React Frontend',
        command: 'npm',
        args: ['start'],
        cwd: path.join(this.projectRoot, 'client'),
        port: 3000,
        color: '\x1b[33m', // Yellow
        readyMessage: 'webpack compiled'
      }
    };
  }

  log(message, service = 'MAIN', color = '\x1b[37m') {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`${color}[${timestamp}] [${service}] ${message}\x1b[0m`);
  }

  async checkDependencies() {
    this.log('🔍 Checking dependencies...', 'MAIN', '\x1b[35m');
    
    // Check if directories exist
    const requiredDirs = ['ai_service', 'server', 'client'];
    for (const dir of requiredDirs) {
      const dirPath = path.join(this.projectRoot, dir);
      if (!fs.existsSync(dirPath)) {
        throw new Error(`Directory ${dir} not found at ${dirPath}`);
      }
    }

    // Check if key files exist
    const requiredFiles = [
      'ai_service/app.py',
      'server/index.js',
      'client/package.json'
    ];
    
    for (const file of requiredFiles) {
      const filePath = path.join(this.projectRoot, file);
      if (!fs.existsSync(filePath)) {
        throw new Error(`Required file ${file} not found`);
      }
    }

    this.log('✅ All dependencies checked', 'MAIN', '\x1b[32m');
  }

  startService(serviceKey) {
    return new Promise((resolve, reject) => {
      const service = this.services[serviceKey];
      this.log(`🚀 Starting ${service.name}...`, serviceKey.toUpperCase(), service.color);

      const childProcess = spawn(service.command, service.args, {
        cwd: service.cwd,
        stdio: 'pipe',
        shell: true,
        env: {
          ...process.env,
          PORT: service.port,
          NODE_ENV: 'development'
        }
      });

      let isReady = false;

      childProcess.stdout.on('data', (data) => {
        const output = data.toString();

        // Log output with service-specific color
        output.split('\n').forEach(line => {
          if (line.trim()) {
            this.log(line.trim(), serviceKey.toUpperCase(), service.color);
          }
        });

        // Check if service is ready
        if (!isReady && output.includes(service.readyMessage)) {
          isReady = true;
          this.log(`✅ ${service.name} is ready on port ${service.port}`, serviceKey.toUpperCase(), '\x1b[32m');
          resolve(childProcess);
        }
      });

      childProcess.stderr.on('data', (data) => {
        const output = data.toString();
        output.split('\n').forEach(line => {
          if (line.trim()) {
            this.log(`ERROR: ${line.trim()}`, serviceKey.toUpperCase(), '\x1b[31m');
          }
        });
      });

      childProcess.on('error', (error) => {
        this.log(`❌ Failed to start ${service.name}: ${error.message}`, serviceKey.toUpperCase(), '\x1b[31m');
        reject(error);
      });

      childProcess.on('exit', (code) => {
        if (code !== 0) {
          this.log(`❌ ${service.name} exited with code ${code}`, serviceKey.toUpperCase(), '\x1b[31m');
        }
      });

      this.processes.push({ name: service.name, process: childProcess, serviceKey });

      // Timeout for service startup
      setTimeout(() => {
        if (!isReady) {
          this.log(`⚠️ ${service.name} startup timeout - continuing anyway`, serviceKey.toUpperCase(), '\x1b[33m');
          resolve(childProcess);
        }
      }, 30000); // 30 second timeout
    });
  }

  async startAllServices() {
    try {
      this.log('🎯 Healthcare Assistant - Starting All Services', 'MAIN', '\x1b[35m');
      this.log('=' .repeat(60), 'MAIN', '\x1b[37m');

      await this.checkDependencies();

      // Start services in sequence with delays
      this.log('📡 Starting AI Service...', 'MAIN', '\x1b[36m');
      await this.startService('ai');
      await this.delay(3000); // Wait 3 seconds

      this.log('🖥️ Starting Backend Server...', 'MAIN', '\x1b[32m');
      await this.startService('backend');
      await this.delay(3000); // Wait 3 seconds

      this.log('⚛️ Starting React Frontend...', 'MAIN', '\x1b[33m');
      await this.startService('frontend');

      this.log('=' .repeat(60), 'MAIN', '\x1b[37m');
      this.log('🎉 All services started successfully!', 'MAIN', '\x1b[32m');
      this.log('📱 Frontend: http://localhost:3000', 'MAIN', '\x1b[33m');
      this.log('🖥️ Backend: http://localhost:5000', 'MAIN', '\x1b[32m');
      this.log('🤖 AI Service: http://localhost:5001', 'MAIN', '\x1b[36m');
      this.log('=' .repeat(60), 'MAIN', '\x1b[37m');
      this.log('Press Ctrl+C to stop all services', 'MAIN', '\x1b[37m');

    } catch (error) {
      this.log(`❌ Failed to start services: ${error.message}`, 'MAIN', '\x1b[31m');
      this.cleanup();
      process.exit(1);
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  cleanup() {
    this.log('🛑 Stopping all services...', 'MAIN', '\x1b[31m');
    
    this.processes.forEach(({ name, process }) => {
      try {
        if (process && !process.killed) {
          process.kill('SIGTERM');
          this.log(`✅ Stopped ${name}`, 'MAIN', '\x1b[32m');
        }
      } catch (error) {
        this.log(`⚠️ Error stopping ${name}: ${error.message}`, 'MAIN', '\x1b[33m');
      }
    });

    this.processes = [];
  }

  setupGracefulShutdown() {
    const signals = ['SIGINT', 'SIGTERM', 'SIGQUIT'];
    
    signals.forEach(signal => {
      process.on(signal, () => {
        this.log(`\n📡 Received ${signal} - shutting down gracefully...`, 'MAIN', '\x1b[33m');
        this.cleanup();
        process.exit(0);
      });
    });

    process.on('uncaughtException', (error) => {
      this.log(`❌ Uncaught Exception: ${error.message}`, 'MAIN', '\x1b[31m');
      this.cleanup();
      process.exit(1);
    });
  }
}

// Main execution
if (require.main === module) {
  const launcher = new ServiceLauncher();
  launcher.setupGracefulShutdown();
  launcher.startAllServices();
}

module.exports = ServiceLauncher;
