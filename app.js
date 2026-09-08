const API_BASE = 'http://localhost:8000';
let currentUser = null;

// UI Elements
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const rateForm = document.getElementById('rate-form');
const recomForm = document.getElementById('recom-form');
const displayUsername = document.getElementById('display-username');
const ratingsList = document.getElementById('ratings-list');
const recomGrid = document.getElementById('recommendations-grid');
const recomContainer = document.getElementById('recommendations-container');
const logoutBtn = document.getElementById('logout-btn');
const toast = document.getElementById('toast');

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Inputs & Dropdowns
const rateInput = document.getElementById('anime-title-input');
const rateDropdown = document.getElementById('rate-dropdown');
const recomInput = document.getElementById('recom-anime-input');
const recomDropdown = document.getElementById('recom-dropdown');

// Tab Navigation Logic
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.add('hidden'));

        // Add active class to clicked button and target content
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        document.getElementById(targetId).classList.remove('hidden');
    });
});

// Utility: Show Toast
function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility: Fetch Kitsu API Image for Anime (single)
async function getAnimeImage(title) {
    try {
        const res = await fetch(`https://kitsu.io/api/edge/anime?filter[text]=${encodeURIComponent(title)}&page[limit]=1`);
        const data = await res.json();
        if (data.data && data.data.length > 0) {
            const attrs = data.data[0].attributes;
            if (attrs.posterImage && attrs.posterImage.small) {
                return attrs.posterImage.small;
            }
        }
    } catch (e) {
        console.error("Failed to fetch image for", title, e);
    }
    return 'https://via.placeholder.com/300x400/eeeeee/333333?text=' + encodeURIComponent(title);
}

// Visual Search Logic
let searchTimeout = null;

async function performSearch(query, dropdownEl, inputEl) {
    if (!query) {
        dropdownEl.classList.add('hidden');
        dropdownEl.innerHTML = '';
        return;
    }

    try {
        dropdownEl.innerHTML = '<div class="loading-text">Searching...</div>';
        dropdownEl.classList.remove('hidden');

        // Using Kitsu API instead of Jikan for stability
        const res = await fetch(`https://kitsu.io/api/edge/anime?filter[text]=${encodeURIComponent(query)}&page[limit]=5`);
        const data = await res.json();

        dropdownEl.innerHTML = '';
        if (data.data && data.data.length > 0) {
            data.data.forEach(anime => {
                const item = document.createElement('div');
                item.className = 'search-result-item';
                
                const attrs = anime.attributes;
                const title = attrs.canonicalTitle || query;
                const year = attrs.startDate ? attrs.startDate.split('-')[0] : 'Unknown';
                const img = (attrs.posterImage && attrs.posterImage.tiny) ? attrs.posterImage.tiny : 'https://via.placeholder.com/50x70/eee/333';
                const showType = attrs.subtype ? attrs.subtype.toUpperCase() : 'TV';

                item.innerHTML = `
                    <img src="${img}" class="search-result-poster" alt="${title}">
                    <div class="search-result-info">
                        <span class="search-result-title">${title}</span>
                        <span class="search-result-year">${year} • ${showType}</span>
                    </div>
                `;

                // On click, auto-fill input and hide dropdown
                item.addEventListener('click', () => {
                    inputEl.value = title;
                    dropdownEl.classList.add('hidden');
                });

                dropdownEl.appendChild(item);
            });
        } else {
            dropdownEl.innerHTML = '<div class="loading-text">No results found.</div>';
        }

    } catch (err) {
        console.error("Search error:", err);
        dropdownEl.innerHTML = '<div class="loading-text" style="color:red;">Error fetching results.</div>';
    }
}

// Attach input listeners for debounce
function setupAutocomplete(inputEl, dropdownEl) {
    inputEl.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        clearTimeout(searchTimeout);
        
        if (val.length < 2) {
            dropdownEl.classList.add('hidden');
            dropdownEl.innerHTML = '';
            return;
        }

        // Wait 500ms after user stops typing
        searchTimeout = setTimeout(() => {
            performSearch(val, dropdownEl, inputEl);
        }, 500);
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!inputEl.contains(e.target) && !dropdownEl.contains(e.target)) {
            dropdownEl.classList.add('hidden');
        }
    });
}

setupAutocomplete(rateInput, rateDropdown);
setupAutocomplete(recomInput, recomDropdown);

// Auth Logic: Register
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        let res = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Registration failed");
        }

        const user = await res.json();
        handleLoginSuccess(user);
        showToast(`Account created! Welcome, ${user.username}!`);
    } catch (error) {
        showToast(error.message);
    }
});

// Auth Logic: Login
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        let res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Login failed");
        }

        const user = await res.json();
        handleLoginSuccess(user);
        showToast(`Welcome back, ${user.username}!`);
    } catch (error) {
        showToast(error.message);
    }
});

function handleLoginSuccess(user) {
    currentUser = user;
    displayUsername.textContent = user.username;
    authSection.classList.add('hidden');
    dashboardSection.classList.remove('hidden');
    
    // reset to first tab
    tabBtns[0].click();
    
    loadRatings();
}

logoutBtn.addEventListener('click', () => {
    currentUser = null;
    dashboardSection.classList.add('hidden');
    authSection.classList.remove('hidden');
    recomContainer.classList.add('hidden');
    
    // clear forms
    loginForm.reset();
    registerForm.reset();
    rateForm.reset();
    recomForm.reset();

    showToast("Logged out successfully");
});

// Load Ratings
async function loadRatings() {
    if (!currentUser) return;
    try {
        const res = await fetch(`${API_BASE}/ratings/${currentUser.id}`);
        const ratings = await res.json();
        
        ratingsList.innerHTML = '';
        if (ratings.length === 0) {
            ratingsList.innerHTML = '<p style="color: var(--text-muted);">You haven\'t rated any anime yet.</p>';
            return;
        }

        ratings.forEach(r => {
            const div = document.createElement('div');
            div.className = 'rating-item';
            div.innerHTML = `
                <span class="rating-title">${r.anime_title}</span>
                <span class="rating-score">${r.rating}/10</span>
            `;
            ratingsList.appendChild(div);
        });
    } catch (e) {
        showToast("Failed to load ratings");
    }
}

// Add/Update Rating
rateForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const title = document.getElementById('anime-title-input').value;
    const rating = document.getElementById('rating-input').value;

    try {
        // Try to add rating first
        let res = await fetch(`${API_BASE}/rate/${currentUser.id}/${encodeURIComponent(title)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ anime_title: title, rating: parseInt(rating) })
        });

        // If it exists, update it instead
        if (res.status === 400) {
            res = await fetch(`${API_BASE}/rate/${currentUser.id}/${encodeURIComponent(title)}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ anime_title: title, rating: parseInt(rating) })
            });
        }

        if (res.ok) {
            showToast("Rating saved!");
            document.getElementById('anime-title-input').value = '';
            document.getElementById('rating-input').value = '';
            loadRatings();
            
            // Switch to ratings tab to show success
            tabBtns[0].click();
        } else {
            throw new Error("Failed to save rating");
        }
    } catch (e) {
        showToast(e.message);
    }
});

// Get Recommendations
recomForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const targetTitle = document.getElementById('recom-anime-input').value;
    recomContainer.classList.remove('hidden');
    recomGrid.innerHTML = '<div class="loading-text">Loading recommendations (this might take a few seconds)...</div>';

    try {
        const res = await fetch(`${API_BASE}/recommendations/${currentUser.id}/${encodeURIComponent(targetTitle)}`);
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Failed to get recommendations");
        }
        
        const data = await res.json();
        const recoms = data.recommendations;

        recomGrid.innerHTML = '';
        if (recoms.length === 0) {
            recomGrid.innerHTML = '<p>No recommendations found.</p>';
            return;
        }

        for (const title of recoms) {
            const card = document.createElement('div');
            card.className = 'anime-card';
            
            // fetch image
            const imgUrl = await getAnimeImage(title);

            card.innerHTML = `
                <img src="${imgUrl}" alt="${title}" class="anime-poster">
                <div class="anime-info">
                    <div class="anime-title">${title}</div>
                </div>
            `;
            recomGrid.appendChild(card);
        }
    } catch (e) {
        recomGrid.innerHTML = `<p style="color: #ff4757; text-align: center; width: 100%;">Error: ${e.message}</p>`;
    }
});
