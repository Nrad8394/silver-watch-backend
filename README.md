# Silver Watch Backend

A comprehensive healthcare monitoring system backend built with Django REST Framework, designed to manage patient vital signs, medical devices, alerts, appointments, and real-time communication between healthcare providers and patients.

## 🏥 Overview

Silver Watch is a healthcare monitoring platform that enables:
- Real-time patient vital signs monitoring
- Medical device management and status tracking
- Alert system for critical health conditions
- Appointment scheduling and management
- Secure chat communication between patients and caregivers
- Comprehensive reporting and analytics
- User management with role-based access control

## 🚀 Features

### Core Functionality
- **Patient Monitoring**: Real-time tracking of vital signs (heart rate, blood pressure, temperature, oxygen levels, respiratory rate)
- **Device Management**: Monitor and manage various medical devices (heart monitors, temperature sensors, motion sensors, etc.)
- **Alert System**: Automated alerts for critical health conditions with configurable thresholds
- **Appointment System**: Schedule and manage appointments between patients and healthcare providers
- **Chat System**: Real-time messaging with WebSocket support for secure communication
- **Reports**: Generate comprehensive health reports and analytics
- **Settings Management**: Configurable system settings and preferences

### Technical Features
- RESTful API with Django REST Framework
- WebSocket support for real-time communication
- Celery for asynchronous task processing
- Redis for caching and session management
- PostgreSQL database with optimized queries
- Docker containerization for easy deployment
- JWT authentication with refresh tokens
- Role-based access control (Admin, Caregiver, Technician, Patient)
- Mobile payments integration with M-Pesa

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.1.6
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Cache/Message Broker**: Redis
- **Task Queue**: Celery
- **WebSockets**: Django Channels
- **Authentication**: JWT with django-allauth
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)
- **Payment Gateway**: M-Pesa (Daraja API)

## 📋 Prerequisites

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL (if running locally)
- Redis (if running locally)

## 🔧 Installation & Setup

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/silver-watch-backend.git
   cd silver-watch-backend
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database
   DB_NAME=silver_watch
   DB_USER=postgres
   DB_PASSWORD=password
   DB_HOST=postgres
   DB_PORT=5432
   
   # Redis
   REDIS_URL=redis://redis:6379/0
   
   # Celery
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   
   # M-Pesa Configuration (Optional)
   MPESA_CONSUMER_KEY=your-consumer-key
   MPESA_CONSUMER_SECRET=your-consumer-secret
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with local database configurations

4. **Run migrations**
   ```bash
   cd silver_watch
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 🗄️ Database Schema

The system includes the following main models:

### User Management
- **CustomUser**: Extended user model with roles (Admin, Caregiver, Technician, Patient)
- **UserProfile**: Additional user profile information

### Device Management
- **Device**: Medical devices with status tracking
- **DeviceData**: Historical device data and readings

### Health Monitoring
- **VitalSigns**: Patient vital signs with status indicators
- **Alert**: System alerts for critical conditions

### Communication & Scheduling
- **Appointment**: Appointment scheduling between users
- **Chat**: Real-time messaging system
- **Message**: Individual chat messages

### System
- **Reports**: Generated health reports
- **Settings**: System configuration and preferences

## 🔌 API Endpoints

### Authentication
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /auth/refresh/` - Refresh JWT token
- `POST /auth/register/` - User registration

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Devices
- `GET /api/devices/` - List devices
- `POST /api/devices/` - Create device
- `GET /api/devices/{id}/` - Get device details
- `PUT /api/devices/{id}/` - Update device
- `DELETE /api/devices/{id}/` - Delete device

### Vital Signs
- `GET /api/vitals/` - List vital signs
- `POST /api/vitals/` - Record vital signs
- `GET /api/vitals/{id}/` - Get vital signs details

### Alerts
- `GET /api/alerts/` - List alerts
- `POST /api/alerts/` - Create alert
- `PUT /api/alerts/{id}/` - Update alert status

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Schedule appointment
- `PUT /api/appointments/{id}/` - Update appointment

### Chat
- `GET /api/chats/` - List chats
- `POST /api/chats/` - Create chat
- `GET /api/chats/{id}/messages/` - Get chat messages
- WebSocket: `/ws/chat/{chat_id}/` - Real-time messaging

## 🔒 Authentication & Authorization

The system uses JWT-based authentication with role-based access control:

- **Admin**: Full system access
- **Caregiver**: Patient management, vital signs monitoring, alerts
- **Technician**: Device management and maintenance
- **Patient**: Personal data access, appointments, chat with caregivers

## 📊 Monitoring & Alerts

The system provides comprehensive monitoring capabilities:

- Real-time vital signs tracking with configurable thresholds
- Automated alert generation for critical conditions
- Device status monitoring (online/offline, battery levels, signal strength)
- Historical data analysis and trend monitoring

## 🚀 Deployment

### Production Deployment with Docker

1. **Set production environment variables**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Use production Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. **Collect static files**
   ```bash
   docker-compose exec django python manage.py collectstatic --noinput
   ```

### VS Code Tasks

The project includes VS Code tasks for development:

- **Docker Build**: `Ctrl+Shift+P` → `Tasks: Run Task` → `docker-build`
- **Docker Run Debug**: `Ctrl+Shift+P` → `Tasks: Run Task` → `docker-run: debug`

## 🧪 Testing

Run the test suite:

```bash
# In Docker
docker-compose exec django python manage.py test

# Local development
python manage.py test
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

## 🗺️ Architecture

The system follows a microservices-inspired architecture with:
- Modular Django apps for different functionalities
- Redis for caching and real-time features
- Celery for background task processing
- PostgreSQL for reliable data storage
- Docker for containerization and deployment

For detailed architecture diagrams, see the `UmlDiagrams/` directory.