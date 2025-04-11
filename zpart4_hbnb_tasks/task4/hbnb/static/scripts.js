// scripts.js 
// -------------------- UTILIDADES -------------------- //

// Función para obtener una cookie por su nombre
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Función para cerrar sesión
function logoutUser() {
    console.log("[AUTH] Cerrando sesión...");
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = '/login';
}

// Función para extraer el place_id de la URL
function getPlaceIdFromURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    return urlParams.get('place_id');
}

// -------------------- LOGIN -------------------- //

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/;`;
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                alert('Login failed: ' + (errorData.error || response.statusText));
            }
        } catch (error) {
            console.error('Error during login:', error);
            alert('Login failed: Could not connect to server.');
        }
    });
}

// -------------------- PÁGINA PRINCIPAL -------------------- //

function setupPage() {
    const token = getCookie('token');
    const loginButton = document.querySelector('nav .login-button');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        if (loginButton) loginButton.style.display = 'block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        if (loginButton) loginButton.style.display = 'none';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logoutUser);
        }
        fetchPlaces(token);
    }

    setupPriceFilter();
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('/api/v1/places', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places.');
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = `<h2>No hay lugares disponibles</h2><p>¡Intenta más tarde o añade uno!</p>`;
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');
        placeCard.setAttribute('data-price', place.price);

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <a href="/place.html?place_id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    priceFilter.addEventListener('change', async () => {
        const selectedPrice = priceFilter.value;
        const placeCards = document.querySelectorAll('.place-card');

        if (selectedPrice === 'All') {
            const token = getCookie('token');
            await fetchPlaces(token);
        } else {
            placeCards.forEach(card => {
                const price = parseInt(card.getAttribute('data-price'));
                if (price <= parseInt(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    });
}

// -------------------- PÁGINA DE DETALLE DEL LUGAR -------------------- //
function setupPlaceDetails() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('Place ID not found.');
        window.location.href = '/';
        return;
    }

    loadPlaceDetails(placeId);

    const reviewFormSection = document.getElementById('add-review');
    if (reviewFormSection) {
        reviewFormSection.style.display = token ? 'block' : 'none';
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            const rating = parseInt(document.getElementById('rating').value);

            if (!reviewText) {
                alert('Please enter a review before submitting.');
                return;
            }

            const reviewData = { text: reviewText, rating: rating };
            const response = await submitReview(token, placeId, reviewData);
            await handleResponse(response, reviewForm);
        });
    }
}

async function loadPlaceDetails(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        if (!response.ok) throw new Error('Failed to load place details');

        const place = await response.json();
        displayPlaceDetails(place);
        displayReviews(place.reviews);  // <-- AÑADE ESTO AQUI
    } catch (error) {
        console.error('Error loading place details:', error);
        document.getElementById('place-details').innerHTML = '<p>Error loading place details.</p>';
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-card">
            <p><strong>Host:</strong> ${place.user_name || "Unknown"}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Amenities:</strong> ${place.amenities && place.amenities.length > 0 ? place.amenities.join(', ') : 'None'}</p>
        </div>
    `;
}

async function loadReviews(placeId) {
    try {
        const response = await fetch(`/api/v1/places/reviews/${placeId}`);
        if (!response.ok) throw new Error('Failed to load reviews');

        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
        document.getElementById('reviews-list').innerHTML = '<p>Error loading reviews.</p>';
    }
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.innerHTML = `<p>No reviews yet. Be the first to review!</p>`;
        return;
    }

    reviews.forEach(review => {
        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        const reviewCard = document.createElement('div');
        reviewCard.classList.add('review-card');
        reviewCard.innerHTML = `
            <p><strong>${review.user_name || 'Anonymous'}:</strong></p>
            <p>${review.text}</p>
            <p>Rating: ${stars}</p>
        `;
        reviewsList.appendChild(reviewCard);
    });
}

async function submitReview(token, placeId, reviewData) {
    try {
        const response = await fetch(`/api/v1/places/reviews/${placeId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewData)
        });
        return response;
    } catch (error) {
        console.error('Error submitting review:', error);
        return null;
    }
}

async function handleResponse(response, form) {
    if (response && response.ok) {
        alert('Review submitted successfully!');
        form.reset();
        const placeId = getPlaceIdFromURL();
        await loadPlaceDetails(placeId);  // <-- Recargar todo el lugar
    } else {
        let errorText = 'Failed to submit review. Please try again.';
        if (response) {
            try {
                const errorData = await response.json();
                if (errorData && errorData.error) {
                    errorText = errorData.error;
                }
            } catch (e) {
                console.error('Error parsing error response:', e);
            }
        }
        alert(errorText);
    }
}

// -------------------- INICIO -------------------- //

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placeDetailsSection = document.getElementById('place-details');

    if (loginForm) {
        setupLoginForm();
    } else if (placeDetailsSection) {
        setupPlaceDetails();
    } else {
        setupPage();
    }
});
