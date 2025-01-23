document.addEventListener('DOMContentLoaded', function() {
    // Navigation buttons
    const homeButton = document.getElementById('homeButton');
    const genreButton = document.getElementById('genreButton');
    const ratingButton = document.getElementById('ratingButton');
    const similarButton = document.getElementById('similarButton');
    const signInButton = document.getElementById('signInButton');

    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '/home';
        });
    }
    if (genreButton) {
        genreButton.addEventListener('click', function() {
            window.location.href = '/genre';
        });
    }
    if (ratingButton) {
        ratingButton.addEventListener('click', function() {
            window.location.href = '/rating';
        });
    }
    if (similarButton) {
        similarButton.addEventListener('click', function() {
            window.location.href = '/similar';
        });
    }
    if (signInButton) {
        signInButton.addEventListener('click', function() {
            window.location.href = '/sign_in';
        });
    }

    const currentPath = window.location.pathname;
    const pathToButton = {
        '/home': homeButton,
        '/genre': genreButton,
        '/rating': ratingButton,
        '/similar': similarButton
    };

    for (const path in pathToButton) {
        if (currentPath.includes(path)) {
            if (pathToButton[path]) {
                pathToButton[path].classList.add('active');
            }
        }
    }

    const amountButtons = {
        '10': document.getElementById('amount10Button'),
        '25': document.getElementById('amount25Button'),
        '50': document.getElementById('amount50Button'),
        '100': document.getElementById('amount100Button')
    };

    for (const key in amountButtons) {
        if (amountButtons.hasOwnProperty(key) && amountButtons[key]) {
            amountButtons[key].addEventListener('click', function() {
                const genreInput = document.getElementById('genreInput');
                let currentGenre = genreInput ? genreInput.value.trim() : '';
                if (!currentGenre) {
                    const urlParams = new URLSearchParams(window.location.search);
                    currentGenre = urlParams.get('genre') || 'action';
                }
                window.location.href = `/genre?genre=${encodeURIComponent(currentGenre)}&amount=${key}`;
            });
        }
    }

    const simAmountButtons = {
        '10': document.getElementById('simAmount10Button'),
        '25': document.getElementById('simAmount25Button'),
        '50': document.getElementById('simAmount50Button')
    };

    for (const key in simAmountButtons) {
        if (simAmountButtons.hasOwnProperty(key) && simAmountButtons[key]) {
            simAmountButtons[key].addEventListener('click', function() {
                const titleInput = document.getElementById('titleInput');
                let currentTitle = titleInput ? titleInput.value.trim() : '';
                if (!currentTitle) {
                    const urlParams = new URLSearchParams(window.location.search);
                    currentTitle = urlParams.get('title') || 'The Godfather';
                }
                window.location.href = `/similar?title=${encodeURIComponent(currentTitle)}&amount=${key}`;
            });
        }
    }

    const movies = document.querySelectorAll('.movie');
    movies.forEach(container => {
        const movieImg = container.querySelector('.movieImage');
        const movieInfoDiv = container.querySelector('.movieInfo');

        container.dataset.state = 'image';
        container.addEventListener('click', function() {
            if (container.dataset.state === 'image') {
                movieImg.style.display = 'none';
                movieInfoDiv.style.display = 'flex';
                container.dataset.state = 'info';
            } else {
                movieInfoDiv.style.display = 'none';
                movieImg.style.display = 'block';
                container.dataset.state = 'image';
            }
        });
    });
});