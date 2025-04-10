document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        // Estamos en login.html
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
    } else {
        // Estamos en index.html
        setupPage();
    }
});

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
    const logoutButton = document.getElementById('logout-button'); // Si agregas botón de logout

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
    placesList.innerHTML = ''; // Limpiar la lista antes de mostrar nuevos lugares

    if (places.length === 0) {
        const noPlacesMessage = document.createElement('div');
        noPlacesMessage.classList.add('no-places-message');
        noPlacesMessage.innerHTML = `
            <h2>No hay lugares disponibles </h2>
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
            <a href="/places/${place.id}" class="details-button">View Details</a>
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
