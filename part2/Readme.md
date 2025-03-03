# HBNB - Part 2

This is Part 2 of the HBNB project for Holberton School.  
This part adds a RESTful API to manage:

- Users
- Places
- Reviews
- Amenities

---

The project includes:

- API endpoints using Flask and Flask-RESTx
- Models for each entity with basic validation
- A service layer to handle business logic
- A persistence layer to manage storage
- Automated tests for all models and endpoints

---
## What it does

- Accepts HTTP requests to create, read, update, and delete each entity.
- Validates all input (like email format, prices, coordinates).
- Handles errors with proper HTTP status codes.
- Saves data using a simple storage layer.

## Entity Models
are the core data objects that represent the "things" your application manages. In this case, your application manages entities like:

### User

| Attribute | Type | Description |
|---|---|---|
| `id` | string (UUID) | Unique identifier |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `email` | string | Email address |
| `is_admin` | boolean | Admin flag |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

### Place

| Attribute | Type | Description |
|---|---|---|
| `id` | string (UUID) | Unique identifier |
| `title` | string | Place title |
| `description` | string | Place description |
| `price` | float | Price per night |
| `latitude` | float | Latitude coordinate |
| `longitude` | float | Longitude coordinate |
| `owner_id` | string (UUID) | Reference to the owner (User) |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

### Review

| Attribute | Type | Description |
|---|---|---|
| `id` | string (UUID) | Unique identifier |
| `text` | string | Review content |
| `rating` | integer | Rating (1 to 5) |
| `user_id` | string (UUID) | Reference to the author (User) |
| `place_id` | string (UUID) | Reference to the reviewed place |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

### Amenity

| Attribute | Type | Description |
|---|---|---|
| `id` | string (UUID) | Unique identifier |
| `name` | string | Amenity name (e.g., Pool, WiFi) |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

## Testing

The project includes:

- Unit tests for all models.
- Functional tests for all endpoints.
- Validation of successful cases and failure cases (invalid data).
- Tests organized under the `tests/` folder.

---



## Testing

- All features are tested using `unittest`.
- Tests include both valid and invalid cases.
- Manual testing can be done with `curl` or Postman.

---

## Author

Hector Ruiz  
Holberton School 
