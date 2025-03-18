# Database Diagram for HBnB Project

This diagram visually represents the database schema structure for the HBnB project, highlighting the core entities and their relationships.

## 🎯 Core Entities and Attributes

### User
- `id`, `first_name`, `last_name`, `email`, `password`, `is_admin`

### Place
- `id`, `title`, `description`, `price`, `latitude`, `longitude`, `owner_id`

### Review
- `id`, `text`, `rating`, `user_id`, `place_id`

### Amenity
- `id`, `name`

### Place_Amenity (join table for many-to-many relationships between Place and Amenity)
- `place_id`, `amenity_id`

## 🔗 ER Diagram using Mermaid.js

```mermaid
erDiagram
    User {
        int id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    Place {
        int id
        string title
        string description
        float price
        float latitude
        float longitude
        int owner_id
    }

    Review {
        int id
        string text
        int rating
        int user_id
        int place_id
    }

    Amenity {
        int id
        string name
    }

    Place_Amenity {
        int place_id
        int amenity_id
    }

    User ||--o{ Place : "owns"
    User ||--o{ Review : "writes"
    Place ||--o{ Review : "has"
    Place ||--o{ Place_Amenity : "offers"
    Amenity ||--o{ Place_Amenity : "is available at"
```

## 🚦 Explanation of Relationships

- **User → Place** *(one-to-many)*  
  A user can own multiple places.

- **User → Review** *(one-to-many)*  
  A user can write multiple reviews.

- **Place → Review** *(one-to-many)*  
  A place can receive multiple reviews.

- **Place ↔ Amenity** *(many-to-many)*  
  A place can have multiple amenities, and an amenity can be found in multiple places, represented through the intermediate table **Place_Amenity**.
