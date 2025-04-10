document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placeDetailsSection = document.getElementById('place-details');

    if (loginForm) {
        // Estamos en login.html
        setupLoginForm();
    } else if (placeDetailsSection) {
        // Estamos en place.html
        setupPlaceDetails();
    } else {
        // Estamos en index.html
        setupPage();
    }
});

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
                window.location.href = '/'; // Redirige al index después de login
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

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

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
    placesList.innerHTML = ''; // Limpia la lista

    if (places.length === 0) {
        const noPlacesMessage = document.createElement('div');
        noPlacesMessage.classList.add('no-places-message');
        noPlacesMessage.innerHTML = `
            <h2>No hay lugares disponibles</h2>
            <p>¡Intenta más tarde o añade uno!</p>
        `;
        placesList.appendChild(noPlacesMessage);
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

    priceFilter.addEventListener('change', () => {
        const selectedPrice = priceFilter.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const price = parseInt(card.getAttribute('data-price'));

            if (selectedPrice === 'All' || price <= parseInt(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

function logoutUser() {
    console.log("[AUTH] Cerrando sesión...");
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = '/login';
}

function setupPlaceDetails() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('place_id');

    if (!placeId) {
        alert('Place ID not found.');
        window.location.href = '/';
        return;
    }

    fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch place details.');
        }

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error fetching place details:', error);
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

    loadReviews(place.id);
}

// review
async function loadReviews(placeId) {
    const token = getCookie('token');
    try {
        const response = await fetch(`/api/v1/reviews/places/${placeId}/reviews`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        let reviews = [];
        if (response.ok) {
            reviews = await response.json();
        } else if (response.status === 404) {
            reviews = [];
        } else {
            throw new Error('Error loading reviews');
        }

        displayReviews(reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
    }
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.innerHTML = `<p>No reviews yet.</p>`;
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.classList.add('review-card');
        reviewCard.innerHTML = `
            <p><strong>${review.user?.name || "Anonymous"}:</strong></p>
            <p>${review.text}</p>
            <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
        `;
        reviewsList.appendChild(reviewCard);
    });
}
