# 🌱 AgriSave - AI-Powered Climate Resilience Dashboard

A Django-based microservice platform integrating machine learning for climate prediction, crop health monitoring, and sustainable farming insights.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)

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
agrisave-backend/
├── config/                 # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   ├── celery.py         # Celery configuration
│   └── __init__.py
├── apps/
│   ├── core_api/          # Core API app
│   │   ├── models.py     # Database models
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py      # API views
│   │   └── urls.py       # API URLs
│   └── ml_engine/         # ML microservice app
│       ├── views.py      # ML endpoints
│       ├── urls.py       # ML URLs
│       └── pipelines/    # ML training pipelines
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
├── .env.example          # Environment template
└── manage.py             # Django management script
```

## Quick Start

1. **Clone and Setup**:

   ```bash
   git clone https://github.com/Fidelisaboke/AgriSave.git
   cd AgriSave/agrisave-backend
   cp .env.example .env
   ```

2. **Configure Environment**: Set `DOCKER_ENV=true` in `.env`

3. **Run with Docker**:

   ```bash
   docker-compose build
   docker-compose up -d
   ```

## Documentation

See the [`docs/`](../docs/) folder for:

- Detailed setup instructions
- API endpoints documentation
- Architecture overview
- Development guides
- Deployment instructions

## 📝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## 📄 License

MIT License - Built for sustainable agriculture 🌾
