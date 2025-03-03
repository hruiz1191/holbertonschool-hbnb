#!/bin/bash

set -e  # Si falla, se detiene

API="http://localhost:5000/api/v1"

echo "🚀 Starting Full HBnB API Test Suite (Task 0 to 5)..."

# -------------------------
# USER - CRUD
# -------------------------

echo "👤 Creating User..."
USER_RESPONSE=$(curl -s -X POST $API/users/ \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}')
USER_ID=$(echo "$USER_RESPONSE" | jq -r '.id')
echo "✅ User Created: $USER_ID"

echo "📋 Getting all Users..."
curl -s $API/users/ | jq .

echo "✏️ Updating User..."
curl -s -X PUT $API/users/$USER_ID \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Johnny"
}' | jq .

echo "🗑️ Deleting User..."
curl -s -X DELETE $API/users/$USER_ID | jq .

echo "📋 Getting all Users after deletion..."
curl -s $API/users/ | jq .

# -------------------------
# AMENITY - CRUD
# -------------------------

echo "🏊‍♂️ Creating Amenity..."
AMENITY_RESPONSE=$(curl -s -X POST $API/amenities/ \
-H "Content-Type: application/json" \
-d '{"name": "Piscina"}')
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | jq -r '.id')
echo "✅ Amenity Created: $AMENITY_ID"

echo "📋 Getting all Amenities..."
curl -s $API/amenities/ | jq .

echo "✏️ Updating Amenity..."
curl -s -X PUT $API/amenities/$AMENITY_ID \
-H "Content-Type: application/json" \
-d '{"name": "Jacuzzi"}' | jq .

echo "🗑️ Deleting Amenity..."
curl -s -X DELETE $API/amenities/$AMENITY_ID | jq .

echo "📋 Getting all Amenities after deletion..."
curl -s $API/amenities/ | jq .

# -------------------------
# USER (recrear) - Required for Place & Review
# -------------------------

echo "👤 Creating User again for Place & Review tests..."
USER_RESPONSE=$(curl -s -X POST $API/users/ \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Alice",
    "last_name": "Wonder",
    "email": "alice@example.com"
}')
USER_ID=$(echo "$USER_RESPONSE" | jq -r '.id')
echo "✅ User Created: $USER_ID"

# -------------------------
# AMENITY (recrear) - Required for Place
# -------------------------

echo "🏊‍♂️ Creating Amenity again..."
AMENITY_RESPONSE=$(curl -s -X POST $API/amenities/ \
-H "Content-Type: application/json" \
-d '{"name": "Piscina"}')
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | jq -r '.id')
echo "✅ Amenity Created: $AMENITY_ID"

# -------------------------
# PLACE - CRUD
# -------------------------

echo "🏠 Creating Place..."
PLACE_RESPONSE=$(curl -s -X POST $API/places/ \
-H "Content-Type: application/json" \
-d "{
    \"title\": \"Hermoso apartamento\",
    \"description\": \"Vista al mar\",
    \"price\": 120.0,
    \"latitude\": 18.4655,
    \"longitude\": -66.1057,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
}")
PLACE_ID=$(echo "$PLACE_RESPONSE" | jq -r '.id')
echo "✅ Place Created: $PLACE_ID"

echo "📋 Getting all Places..."
curl -s $API/places/ | jq .

echo "✏️ Updating Place..."
curl -s -X PUT $API/places/$PLACE_ID \
-H "Content-Type: application/json" \
-d '{"title": "Apartamento de lujo"}' | jq .

# No DELETE de PLACE aún (Task 5 no lo pide)

# -------------------------
# REVIEW - CRUD
# -------------------------

echo "⭐ Creating Review..."
REVIEW_RESPONSE=$(curl -s -X POST $API/reviews/ \
-H "Content-Type: application/json" \
-d "{
    \"text\": \"Excelente lugar\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}")
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | jq -r '.id')
echo "✅ Review Created: $REVIEW_ID"

echo "📋 Getting all Reviews..."
curl -s $API/reviews/ | jq .

echo "📋 Getting Reviews for Place $PLACE_ID..."
curl -s $API/places/$PLACE_ID/reviews | jq .

echo "✏️ Updating Review..."
curl -s -X PUT $API/reviews/$REVIEW_ID \
-H "Content-Type: application/json" \
-d '{
    "text": "Increíble experiencia"
}' | jq .

echo "🗑️ Deleting Review..."
curl -s -X DELETE $API/reviews/$REVIEW_ID | jq .

echo "📋 Getting all Reviews after deletion..."
curl -s $API/reviews/ | jq .

echo "✅ Full Test Suite Completed Successfully!"
