# API Documentation for Fitness And Diet App

This document provides detailed information about the API endpoints available in the Fitness And Diet App.

## Base URL

When running locally, the base URL is: `http://localhost:8000`

## Authentication

Most endpoints require authentication using JWT tokens. To authenticate:

1. Register a user account using the `/auth/signup` endpoint
2. Obtain a JWT token using the `/auth/login` endpoint
3. Include the token in the Authorization header of subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

## API Endpoints

### Authentication Endpoints

#### Register a new user

**Endpoint:** `POST /auth/signup`

**Description:** Creates a new user account.

**Request Body:**
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "your_username",
  "email": "your_email@example.com"
}
```

**Status Codes:**
- 200: Success
- 400: Username or email already registered

#### Login

**Endpoint:** `POST /auth/login`

**Description:** Authenticates a user and returns a JWT token.

**Request Body (Form Data):**
```
username=your_username&password=your_password
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- 200: Success
- 401: Incorrect username or password

#### Delete User Account

**Endpoint:** `DELETE /auth/users/me`

**Description:** Deletes the current user's account and all associated data.

**Authentication:** Required

**Response:** No content (204)

**Status Codes:**
- 204: Success
- 401: Unauthorized

### Fitness Plan Endpoints

#### Generate Fitness Plan

**Endpoint:** `POST /api/fitness-plan`

**Description:** Generates a personalized fitness and diet plan based on user input.

**Authentication:** Required

**Request Body:**
```json
{
  "typical_breakfast": "Hausa koko with koose, tea with bread and eggs",
  "typical_lunch": "Jollof rice with fried chicken, Banku with okra stew",
  "typical_dinner": "Waakye with gari and spaghetti, Yam with palava sauce",
  "typical_snacks": "Fruits, nuts, kelewele",
  "dietary_restrictions": "No specific restrictions",
  "favorite_meals": "Jollof rice with chicken, Banku with tilapia",
  "comfort_foods": "Kelewele, Waakye, Fufu with palm nut soup",
  "eating_out_frequency": "Once a week",
  "eating_out_choices": "Local restaurants serving traditional Ghanaian dishes",
  "current_weight": "190 lbs",
  "weight_goal": "Lose 15 lbs (target: 175 lbs)",
  "workout_frequency": "Workout 3 times per week"
}
```

**Response:**
```json
{
  "workout_plan": [
    {
      "day": "Monday",
      "activity": "30 minutes of cardio (jogging or brisk walking) followed by 15 minutes of core exercises"
    },
    {
      "day": "Tuesday",
      "activity": "Rest day or light stretching"
    },
    // ... other days
  ],
  "diet_plan": [
    {
      "day": "Monday",
      "meals": "Breakfast: Hausa koko with a small portion of koose\nLunch: Jollof rice (1 cup) with grilled chicken (remove skin)\nDinner: Small portion of waakye with grilled fish\nSnacks: Apple or a small handful of nuts"
    },
    {
      "day": "Tuesday",
      "meals": "Breakfast: Tea with whole grain bread and 1 boiled egg\nLunch: Banku (small portion) with okra stew and fish\nDinner: Yam with palava sauce (control portion size)\nSnacks: Orange or pear"
    },
    // ... other days
  ],
  "estimated_days_to_goal": 60
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Error processing request

#### Get User Plans

**Endpoint:** `GET /api/my-plans`

**Description:** Retrieves all fitness plans created by the current user.

**Authentication:** Required

**Response:**
```json
[
  {
    "workout_plan": [
      {
        "day": "Monday",
        "activity": "30 minutes of cardio (jogging or brisk walking) followed by 15 minutes of core exercises"
      },
      // ... other days
    ],
    "diet_plan": [
      {
        "day": "Monday",
        "meals": "Breakfast: Hausa koko with a small portion of koose\nLunch: Jollof rice (1 cup) with grilled chicken (remove skin)\nDinner: Small portion of waakye with grilled fish\nSnacks: Apple or a small handful of nuts"
      },
      // ... other days
    ],
    "estimated_days_to_goal": 60
  },
  // ... other plans
]
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Error retrieving plans

#### Update User Plan

**Endpoint:** `PUT /api/my-plans/{plan_id}`

**Description:** Updates an existing fitness plan with new information.

**Authentication:** Required

**Path Parameters:**
- `plan_id`: ID of the plan to update

**Request Body:**
```json
{
  "current_weight": "185 lbs",
  "weight_goal": "Lose 10 lbs (target: 175 lbs)",
  "workout_frequency": "Workout 4 times per week"
}
```

**Response:** Updated plan in the same format as the GET response

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Plan not found or not owned by user
- 500: Error updating plan

#### Delete User Plan

**Endpoint:** `DELETE /api/my-plans/{plan_id}`

**Description:** Deletes an existing fitness plan.

**Authentication:** Required

**Path Parameters:**
- `plan_id`: ID of the plan to delete

**Response:** No content (204)

**Status Codes:**
- 204: Success
- 401: Unauthorized
- 404: Plan not found or not owned by user
- 500: Error deleting plan

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

The API currently does not implement rate limiting, but excessive requests may be throttled in the future.

## Versioning

The current API version is v1. All endpoints are prefixed with `/api` and do not require a version specifier.