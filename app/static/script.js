// ./app/static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const homeButton = document.getElementById('homeButton');
    const genreButton = document.getElementById('genreButton');
    const ratingButton = document.getElementById('ratingButton');
    const similarButton = document.getElementById('similarButton');

    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '/home'
        });
    };
    if (genreButton) {
        genreButton.addEventListener('click', function() {
            window.location.href = '/genre'
        });
    };
    if (ratingButton) {
        ratingButton.addEventListener('click', function() {
            window.location.href = '/rating'
        });
    };
    if (similarButton) {
        similarButton.addEventListener('click', function() {
            window.location.href = '/similar'
        });
    };

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

    const movies = document.querySelectorAll('.image');
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