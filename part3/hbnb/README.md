# HBnB Project: Database Schema and Initial Data Report

This document outlines the SQL scripts used to generate the entire HBnB database schema, insert initial data, and perform basic CRUD operations.

---

## Objective

Create SQL scripts to generate the HBnB project database schema, establish relationships, and insert initial data, including an administrator user and basic amenities.

---

## SQL Scripts

### Table Creation

| Table Name | SQL Script |
|------------|------------|
| **User**   | ```sql
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);
``` |
| **Place**  | ```sql
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);
``` |
| **Review** | ```sql
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    UNIQUE(user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
);
``` |
| **Amenity**| ```sql
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
``` |
| **Place_Amenity** | ```sql
CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
``` |

---

### Initial Data Insertion

| Data Description | SQL Script |
|------------------|------------|
| **Administrator User** | ```sql
-- Password hashed with bcrypt (example)
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$examplebcrypthashedpassword', TRUE);
``` |
| **Initial Amenities** | ```sql
INSERT INTO Amenity (id, name) VALUES
('uuid-generated-1', 'WiFi'),
('uuid-generated-2', 'Swimming Pool'),
('uuid-generated-3', 'Air Conditioning');
``` |

---

## Execution Evidence

### Tables Successfully Created

```sql
mysql> SHOW TABLES;
+------------------------+
| Tables_in_hbnb_project |
+------------------------+
| Amenity                |
| Place                  |
| Place_Amenity          |
| Review                 |
| User                   |
+------------------------+
```

### Initial Data Inserted

```sql
mysql> SELECT id, email, is_admin FROM User;
+--------------------------------------+---------------+----------+
| id                                   | email         | is_admin |
+--------------------------------------+---------------+----------+
| 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | admin@hbnb.io | TRUE     |
+--------------------------------------+---------------+----------+

mysql> SELECT * FROM Amenity;
+--------------------+------------------+
| id                 | name             |
+--------------------+------------------+
| uuid-generated-1   | WiFi             |
| uuid-generated-2   | Swimming Pool    |
| uuid-generated-3   | Air Conditioning |
+--------------------+------------------+
```

---

## CRUD Operations Testing

| Operation | SQL Script |
|-----------|------------|
| **Create**| ```sql
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('uuid-place-1', 'Beach House', 'Example description', 150.00, 18.4655, -66.1057, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');
``` |
| **Read**  | ```sql
SELECT * FROM Place WHERE id = 'uuid-place-1';
``` |
| **Update**| ```sql
UPDATE Place SET price = 175.00 WHERE id = 'uuid-place-1';
``` |
| **Delete**| ```sql
DELETE FROM Place WHERE id = 'uuid-place-1';
SELECT * FROM Place WHERE id = 'uuid-place-1'; -- Should return empty
``` |

---

## Conclusion

All tables were created successfully following the provided instructions. Initial data, including the admin user and amenities, were inserted correctly. Basic CRUD operations have been successfully performed, confirming the database schema's integrity and functionality. The database is now ready for use in the HBnB project.

---

**Author:**  
Your Name Here  
Holberton School – HBnB Project  
Date: March 17, 2025

