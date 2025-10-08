# 🚀 Quick Start Guide - AgriSave Backend

Get the AgriSave backend up and running in 10 minutes!

## Prerequisites Checklist

- ✅ Ubuntu/Linux system
- ✅ Docker Desktop installed and running
- ✅ Git installed
- ✅ VS Code (optional but recommended)

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
cd ~
git clone https://github.com/Fidelisaboke/AgriSave.git
cd AgriSave
git checkout -b backend
cd backend
```

### 2. Create Project Files

Copy all the artifact files I provided into your `backend` directory:

```
backend/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── setup.sh
├── README.md
└── (Django apps will be created automatically)
```


### 3. Create Superuser

```bash
docker-compose exec django_api python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 4. Verify Installation

Open your browser and check:

1. **API Root**: http://localhost:8000/api/
2. **Admin Panel**: http://localhost:8000/admin/
3. **Swagger Docs**: http://localhost:8000/swagger/
4. **ReDoc**: http://localhost:8000/redoc/

### 5. Test the API

**Option A: Using cURL**

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testfarmer",
    "email": "test@example.com",
    "password": "Test123456",
    "password2": "Test123456",
    "first_name": "Test",
    "last_name": "Farmer",
    "location": "Nairobi, Kenya",
    "farm_size": 3.0
  }'
```

**Option B: Using Swagger UI**

1. Go to http://localhost:8000/swagger/
2. Try out the `/api/auth/register/` endpoint
3. Copy the access token from the response
4. Click "Authorize" button at the top
5. Enter: `Bearer YOUR_ACCESS_TOKEN`
6. Now you can test all protected endpoints!

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Django only
docker-compose logs -f django_api

# PostgreSQL only
docker-compose logs -f postgres
```

### Django Management
```bash
# Django shell
docker-compose exec django_api python manage.py shell

# Create migrations
docker-compose exec django_api python manage.py makemigrations

# Apply migrations
docker-compose exec django_api python manage.py migrate

# Collect static files
docker-compose exec django_api python manage.py collectstatic
```

### Docker Management
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache

# Restart specific service
docker-compose restart django_api
```

## Quick Test Workflow

### 1. Register & Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "email": "farmer1@example.com",
    "password": "Farmer123",
    "password2": "Farmer123",
    "location": "Kiambu",
    "farm_size": 5
  }'

# Save the access token from response
export TOKEN="your_access_token_here"
```

### 2. Create a Crop

```bash
curl -X POST http://localhost:8000/api/crops/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Maize",
    "crop_type": "cereals",
    "planting_date": "2025-10-01",
    "expected_harvest_date": "2026-01-15",
    "area_planted": 2.5,
    "status": "planted"
  }'
```

### 3. Record Green Activity

```bash
curl -X POST http://localhost:8000/api/greenpoints/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "activity_type": "organic",
    "description": "Using organic fertilizers"
  }'
```

### 4. Get Green Points Summary

```bash
curl -X GET http://localhost:8000/api/greenpoints/summary/ \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Test ML Endpoint

```bash
curl -X POST http://localhost:8000/api/ml/recommend-crop/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "soil_type": "loam",
    "rainfall": 800,
    "temperature": 25,
    "location": "Kiambu"
  }'
```

## Troubleshooting

### "Port already in use" Error

```bash
# Find and kill process on port 8000
sudo lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### "Module not found" Error

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Migrations Not Applied

```bash
# Force migrations
docker-compose exec django_api python manage.py migrate --fake-initial
docker-compose exec django_api python manage.py migrate
```

## Database Access with pgAdmin 4

1. Open pgAdmin 4
2. Right-click "Servers" → "Register" → "Server"
3. Enter details:
   - **Name**: AgriSave Local
   - **Host**: localhost
   - **Port**: 5432
   - **Database**: agrisave_db
   - **Username**: agrisave_user
   - **Password**: agrisave_pass123

## Next Steps

1. ✅ Backend is running
2. ✅ All endpoints tested
3. ✅ Database connected

**What's Next (Day 3 - Wednesday):**
- Integrate real ML models
- Set up Celery tasks for async processing
- Optimize API performance
- Add Redis caching

## Useful Resources

- **API Documentation**: `/docs/API_ENDPOINTS.md`
- **Full README**: `/README.md`
- **Swagger UI**: http://localhost:8000/swagger/
- **Django Admin**: http://localhost:8000/admin/

## Git Workflow

```bash
# Add all changes
git add .

# Commit with message
git commit -m "feat: complete backend API setup"

# Push to your branch
git push origin backend

# Create pull request on GitHub
```

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify all containers are running: `docker-compose ps`
3. Check the troubleshooting section above
4. Review `/docs/API_ENDPOINTS.md` for endpoint details

---

**🎉 Congratulations! Your backend is ready for development!** 🚀