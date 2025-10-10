# 🌱 AgriSave - AI-Powered Climate Resilience Dashboard

A Django-based microservice platform integrating machine learning for climate prediction, crop health monitoring, and sustainable farming insights.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Testing](#testing)

## ✨ Features

- **User Management**: JWT-based authentication with farmer profiles
- **Crop Management**: Track crops, planting dates, and harvest schedules
- **Weather Integration**: Store and query historical weather data
- **Green Points System**: Sustainability scoring with badge tiers
- **ML Integration**: Disease detection, crop recommendations, and climate forecasting
- **RESTful API**: Comprehensive API with Swagger documentation
- **Async Tasks**: Celery integration for background processing

## 🛠 Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery
- **Authentication**: JWT (Simple JWT)
- **API Docs**: drf-yasg (Swagger/ReDoc)
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
backend/
├── climate_dashboard/      # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   ├── celery.py         # Celery configuration
│   └── __init__.py
├── core_api/              # Core API app
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # API URLs
│   └── admin.py          # Admin configuration
├── ml_engine/             # ML microservice app
│   ├── views.py          # ML endpoints
│   ├── urls.py           # ML URLs
│   └── models/           # ML model storage
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
└── .env                  # Environment variables
```

## 🚀 Setup Instructions

### Prerequisites
- Docker Desktop installed
- Git
- At least 4GB RAM available

### Step 1: Clone Repository

```bash
git clone https://github.com/Fidelisaboke/AgriSave.git
cd AgriSave/backend
```

### Step 2: Configure Environment

The `.env` file is already created with default values. Update if needed:

```bash
# Database credentials
DB_NAME=agrisave_db
DB_USER=agrisave_user
DB_PASSWORD=agrisave_pass123

# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Step 3: Build and Run with Docker

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

Or manually:

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec django_api python manage.py makemigrations
docker-compose exec django_api python manage.py migrate

# Create superuser
docker-compose exec django_api python manage.py createsuperuser
```

### Step 4: Verify Installation

Check if all services are running:

```bash
docker-compose ps
```

Expected output:
- `agrisave_postgres` - PostgreSQL database
- `agrisave_redis` - Redis cache
- `agrisave_django` - Django API server
- `agrisave_celery` - Celery worker

### Step 5: Load Datasets
Ensure you download and place the datasets in the `backend/ml_engine/data/raw` directory for ML model training. 

The datasets are:
-  PlantVillage Dataset: [Download Link](https://www.kaggle.com/datasets/emmarex/plantdisease)
- Nairobi Weather Data: [Download Link](https://www.kaggle.com/datasets/johnkiriba/nairobi-weather-data)
- Crop Recommendation Dataset: [Download Link](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

### Step 6: Train ML models
```bash
# Climate forecaster
docker-compose exec django_api python manage.py train_climate_forecaster

# Crop recommender
docker-compose exec django_api python manage.py train_crop_recommender

# Disease detector
docker-compose exec django_api python manage.py train_disease_detector
```
- The model artifacts will be saved within `backend/media/models/`.

Access the API:
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 📡 API Endpoints

### Authentication
```
POST /api/auth/register/          # Register new user
POST /api/auth/login/             # Get JWT tokens
POST /api/auth/refresh/           # Refresh access token
GET  /api/auth/me/                # Get current user profile
```

### Crops
```
GET    /api/crops/                # List all crops
POST   /api/crops/                # Create new crop
GET    /api/crops/{id}/           # Get crop details
PUT    /api/crops/{id}/           # Update crop
DELETE /api/crops/{id}/           # Delete crop
GET    /api/crops/statistics/     # Get crop statistics
GET    /api/crops/upcoming_harvest/ # Get upcoming harvests
```

### Weather
```
GET    /api/weather/              # List weather data
POST   /api/weather/              # Add weather data
GET    /api/weather/{id}/         # Get weather details
GET    /api/weather/latest/       # Get latest weather for location
```

### Green Points
```
GET    /api/greenpoints/          # List green points
POST   /api/greenpoints/          # Record new activity
GET    /api/greenpoints/summary/  # Get points summary
POST   /api/greenpoints/{id}/verify/ # Verify activity (admin)
```

### ML Endpoints
```
POST /api/ml/predict-disease/     # Predict crop disease from image
POST /api/ml/recommend-crop/      # Get crop recommendations
POST /api/ml/climate-forecast/    # Get climate forecast
GET  /api/ml/status/              # Check ML service status
```

## 💻 Development

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f django_api

# Access Django shell
docker-compose exec django_api python manage.py shell

# Run tests
docker-compose exec django_api python manage.py test

# Create migrations
docker-compose exec django_api python manage.py makemigrations

# Apply migrations
docker-compose exec django_api python manage.py migrate

# Collect static files
docker-compose exec django_api python manage.py collectstatic

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Database Access

Using pgAdmin 4:
- **Host**: localhost
- **Port**: 5432
- **Database**: agrisave_db
- **Username**: agrisave_user
- **Password**: agrisave_pass123

### Hot Reload

The Docker setup includes volume mounting, so code changes will automatically reload the Django development server.

## 🧪 Testing

### Manual Testing with cURL

**Register User:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "email": "farmer1@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "location": "Kiambu, Kenya",
    "farm_size": 5.5
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "password": "securepass123"
  }'
```

**Create Crop (with JWT token):**
```bash
curl -X POST http://localhost:8000/api/crops/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Maize",
    "crop_type": "cereals",
    "variety": "Hybrid 614",
    "planting_date": "2025-10-01",
    "expected_harvest_date": "2026-01-15",
    "area_planted": 2.5,
    "status": "planted"
  }'
```

**Test ML Disease Prediction:**
```bash
curl -X POST http://localhost:8000/api/ml/predict-disease/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "image=@/path/to/leaf_image.jpg"
```

## 📊 Database Models

### UserProfile
- Extends Django User model
- Tracks location, farm size, green points, and badge tier

### Crop
- Crop management (name, type, variety, dates, area)
- Status tracking (planted, growing, harvested, failed)

### WeatherData
- Historical weather records
- Temperature, humidity, rainfall, wind speed, pressure

### GreenPoint
- Sustainability activities tracking
- Auto-calculated points based on activity type
- Badge tier system (Bronze → Silver → Gold → Platinum)

## 🎯 Current Status

### ✅ Completed (Day 1 & 2)
- Docker multi-container setup
- PostgreSQL database integration
- Django REST API with all CRUD endpoints
- JWT authentication
- User registration and profiles
- Crop management system
- Weather data endpoints
- Green Points engine
- ML placeholder endpoints
- API documentation (Swagger/ReDoc)
- Celery configuration

### 🚧 Next Steps (Day 3 - Wednesday)
- Integrate actual ML models
- Disease detection with CNN
- Climate forecasting with LSTM
- Crop recommendation with Random Forest
- Celery async tasks for ML inference
- Redis caching for predictions

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong database passwords
- Enable HTTPS in production
- Implement rate limiting
- Add input validation and sanitization

## 🐛 Troubleshooting

### Container won't start
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database connection errors
```bash
# Check if PostgreSQL is ready
docker-compose logs postgres

# Restart services
docker-compose restart django_api
```

### Port already in use
```bash
# Stop conflicting services
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5432 | xargs kill -9
```

### Migrations issues
```bash
# Reset migrations
docker-compose exec django_api python manage.py migrate --fake
docker-compose exec django_api python manage.py migrate
```

## 📝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## 📄 License

This project is part of a hackathon and is for educational purposes.

## 👥 Team

- **Backend Developer**: API development and database design
- **Frontend Developer**: React dashboard UI
- **AI/ML Engineer**: Machine learning models
- **Data & QA Engineer**: Testing and data validation
- **Project Lead/DevOps**: Infrastructure and deployment

## 📞 Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/Fidelisaboke/AgriSave/issues)
- Documentation: Check `/docs` folder
- API Docs: http://localhost:8000/swagger/

---

**Built with ❤️ for sustainable agriculture** 🌾