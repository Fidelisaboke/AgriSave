# 📡 AgriSave API Endpoints Documentation

Base URL: `http://localhost:8000`

## Authentication

All endpoints except registration and login require JWT authentication.

**Authorization Header:**
```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### 1. Register User
**POST** `/api/auth/register/`

Creates a new user account with profile.

**Request Body:**
```json
{
  "username": "farmer1",
  "email": "farmer1@example.com",
  "password": "securepass123",
  "password2": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "location": "Kiambu, Kenya",
  "farm_size": 5.5
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "farmer1",
    "email": "farmer1@example.com"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Login
**POST** `/api/auth/login/`

Obtain JWT tokens.

**Request Body:**
```json
{
  "username": "farmer1",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Refresh Token
**POST** `/api/auth/refresh/`

Get new access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Current User
**GET** `/api/auth/me/`

Get current authenticated user profile.

**Response (200):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "farmer1",
    "email": "farmer1@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "phone_number": "+254712345678",
  "location": "Kiambu, Kenya",
  "farm_size": "5.50",
  "total_green_points": 45,
  "badge_tier": "bronze",
  "created_at": "2025-10-07T10:30:00Z",
  "updated_at": "2025-10-07T10:30:00Z"
}
```

---

## 🌾 Crop Endpoints

### 1. List All Crops
**GET** `/api/crops/`

Get all crops for authenticated user.

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_username": "farmer1",
      "name": "Maize",
      "crop_type": "cereals",
      "variety": "Hybrid 614",
      "planting_date": "2025-10-01",
      "expected_harvest_date": "2026-01-15",
      "area_planted": "2.50",
      "status": "planted",
      "notes": "First season planting",
      "created_at": "2025-10-07T10:30:00Z",
      "updated_at": "2025-10-07T10:30:00Z"
    }
  ]
}
```

### 2. Create Crop
**POST** `/api/crops/`

Create a new crop record.

**Request Body:**
```json
{
  "name": "Maize",
  "crop_type": "cereals",
  "variety": "Hybrid 614",
  "planting_date": "2025-10-01",
  "expected_harvest_date": "2026-01-15",
  "area_planted": 2.5,
  "status": "planted",
  "notes": "First season planting"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "farmer1",
  "name": "Maize",
  "crop_type": "cereals",
  "variety": "Hybrid 614",
  "planting_date": "2025-10-01",
  "expected_harvest_date": "2026-01-15",
  "area_planted": "2.50",
  "status": "planted",
  "notes": "First season planting",
  "created_at": "2025-10-07T10:30:00Z",
  "updated_at": "2025-10-07T10:30:00Z"
}
```

### 3. Get Crop Details
**GET** `/api/crops/{id}/`

Get specific crop details.

**Response (200):** Same as Create Crop response

### 4. Update Crop
**PUT** `/api/crops/{id}/`

Update crop information.

**PATCH** `/api/crops/{id}/`

Partial update of crop.

### 5. Delete Crop
**DELETE** `/api/crops/{id}/`

Delete a crop record.

**Response (204):** No content

### 6. Crop Statistics
**GET** `/api/crops/statistics/`

Get crop statistics for current user.

**Response (200):**
```json
{
  "total_crops": 5,
  "by_status": {
    "planted": 2,
    "growing": 2,
    "harvested": 1
  },
  "by_type": {
    "cereals": 2,
    "vegetables": 2,
    "legumes": 1
  },
  "total_area": 12.5
}
```

### 7. Upcoming Harvest
**GET** `/api/crops/upcoming_harvest/`

Get crops with harvest expected in next 30 days.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Tomatoes",
    "crop_type": "vegetables",
    "expected_harvest_date": "2025-10-25",
    "status": "growing"
  }
]
```

---

## 🌤️ Weather Endpoints

### 1. List Weather Data
**GET** `/api/weather/`

Get weather data with optional filters.

**Query Parameters:**
- `location` (optional): Filter by location
- `start_date` (optional): Filter from date (YYYY-MM-DD)
- `end_date` (optional): Filter to date (YYYY-MM-DD)

**Response (200):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "location": "Kiambu, Kenya",
      "latitude": "-1.171944",
      "longitude": "36.835278",
      "temperature": "23.50",
      "humidity": "65.00",
      "rainfall": "5.20",
      "wind_speed": "12.30",
      "pressure": "1013.25",
      "description": "Partly cloudy",
      "recorded_at": "2025-10-07T12:00:00Z",
      "created_at": "2025-10-07T12:05:00Z"
    }
  ]
}
```

### 2. Add Weather Data
**POST** `/api/weather/`

Add new weather record.

**Request Body:**
```json
{
  "location": "Kiambu, Kenya",
  "latitude": -1.171944,
  "longitude": 36.835278,
  "temperature": 23.5,
  "humidity": 65.0,
  "rainfall": 5.2,
  "wind_speed": 12.3,
  "pressure": 1013.25,
  "description": "Partly cloudy",
  "recorded_at": "2025-10-07T12:00:00Z"
}
```

### 3. Latest Weather
**GET** `/api/weather/latest/?location=Kiambu`

Get most recent weather data for a location.

**Response (200):** Single weather object

---

## 🌱 Green Points Endpoints

### 1. List Green Points
**GET** `/api/greenpoints/`

Get all green point activities for current user.

**Response (200):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_username": "farmer1",
      "activity_type": "organic",
      "description": "Switched to organic fertilizers",
      "points_earned": 15,
      "verified": true,
      "verification_date": "2025-10-07T14:00:00Z",
      "created_at": "2025-10-06T10:00:00Z"
    }
  ]
}
```

### 2. Record Activity
**POST** `/api/greenpoints/`

Record a new sustainability activity.

**Request Body:**
```json
{
  "activity_type": "organic",
  "description": "Switched to organic fertilizers for all crops"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "farmer1",
  "activity_type": "organic",
  "description": "Switched to organic fertilizers for all crops",
  "points_earned": 15,
  "verified": false,
  "verification_date": null,
  "created_at": "2025-10-07T15:30:00Z"
}
```

### 3. Green Points Summary
**GET** `/api/greenpoints/summary/`

Get comprehensive green points summary.

**Response (200):**
```json
{
  "total_points": 45,
  "badge_tier": "bronze",
  "recent_activities": [
    {
      "id": 1,
      "activity_type": "organic",
      "points_earned": 15,
      "verified": true,
      "created_at": "2025-10-06T10:00:00Z"
    }
  ],
  "points_to_next_tier": 105,
  "next_tier": "silver"
}
```

### 4. Verify Activity (Admin Only)
**POST** `/api/greenpoints/{id}/verify/`

Verify a green point activity.

**Response (200):** Updated green point object

---

## 🤖 ML Endpoints

### 1. Predict Disease
**POST** `/api/ml/predict-disease/`

Predict crop disease from leaf image.

**Request (multipart/form-data):**
```
image: <file>
```

**Response (200):**
```json
{
  "disease": "Early Blight",
  "confidence": 0.87,
  "severity": "Medium",
  "recommendation": "Apply fungicide and remove affected leaves. Ensure proper spacing for air circulation.",
  "timestamp": "2025-10-07T16:00:00"
}
```

### 2. Recommend Crop
**POST** `/api/ml/recommend-crop/`

Get crop recommendations based on conditions.

**Request Body:**
```json
{
  "soil_type": "loam",
  "rainfall": 800,
  "temperature": 25,
  "location": "Kiambu, Kenya"
}
```

**Response (200):**
```json
{
  "location": "Kiambu, Kenya",
  "soil_type": "loam",
  "recommendations": [
    {
      "name": "Maize",
      "suitability_score": 0.92,
      "expected_yield": "35 bags/acre",
      "growing_period": "3-4 months",
      "water_requirement": "Medium"
    },
    {
      "name": "Beans",
      "suitability_score": 0.88,
      "expected_yield": "12 bags/acre",
      "growing_period": "2-3 months",
      "water_requirement": "Low"
    }
  ],
  "timestamp": "2025-10-07T16:10:00"
}
```

### 3. Climate Forecast
**POST** `/api/ml/climate-forecast/`

Get climate forecast for location.

**Request Body:**
```json
{
  "location": "Kiambu, Kenya",
  "days": 7
}
```

**Response (200):**
```json
{
  "location": "Kiambu, Kenya",
  "forecast_period": "7 days",
  "forecast": [
    {
      "date": "2025-10-08",
      "temperature": {
        "min": 18,
        "max": 26,
        "avg": 22
      },
      "rainfall": 3.5,
      "humidity": 75,
      "wind_speed": 12.5,
      "description": "Partly Cloudy"
    }
  ],
  "agricultural_advice": "Plan irrigation accordingly based on rainfall forecast.",
  "timestamp": "2025-10-07T16:15:00"
}
```

### 4. ML Status
**GET** `/api/ml/status/`

Check ML service status.

**Response (200):**
```json
{
  "status": "operational",
  "models": {
    "disease_detection": "mock",
    "crop_recommendation": "mock",
    "climate_forecast": "mock"
  },
  "message": "ML endpoints are operational with mock data. Real models will be integrated on Day 3."
}
```

---

## 📋 Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## 📊 Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server error |

---

## 🔗 Useful Links

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/