document.addEventListener('DOMContentLoaded', function() {
    const homeButton = document.getElementById('homeButton');
    const ratingButton = document.getElementById('ratingButton');
    const genreButton = document.getElementById('genreButton');
    const similarButton = document.getElementById('similarButton');
    const signInButton = document.getElementById('signInButton');
    const newUserButton = document.getElementById('newUserButton');
    const userPageButton = document.getElementById('userPageButton');

    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '/home';
        });
    }
    if (ratingButton) {
        ratingButton.addEventListener('click', function() {
            window.location.href = '/rating';
        });
    }
    if (genreButton) {
        genreButton.addEventListener('click', function() {
            window.location.href = '/genre';
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
    if (newUserButton) {
        newUserButton.addEventListener('click', function() {
            window.location.href = '/new_user';
        });
    }
    if (userPageButton) {
        userPageButton.addEventListener('click', function() {
            const username = userPageButton.getAttribute('data-username');
            window.location.href = `/user_page/${username}`;
        });
    }

    const addFavouriteButton = document.querySelectorAll('.addFavouriteButton');
    addFavouriteButton.forEach(button => {
        button.addEventListener('click', () => {
            const movie = button.getAttribute('data-movie');

            fetch('/add_favourite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ movie: movie }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.error) {
                        displayMessage(data.error, 'error');
                    } else {
                        displayMessage(data.message, 'success');
                        button.textContent = '✔';
                        button.disabled = true;
                        button.classList.add('added');
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    displayMessage('An unexpected error occurred.', 'error');
                });
        });
    });

    const removeFavouriteButtons = document.querySelectorAll('.removeFavouriteButton');
    removeFavouriteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const title = button.getAttribute('data-movie');

            fetch('/remove_favourite', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: title })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    displayMessage(data.error);
                } else {
                    displayMessage(data.message);
                    button.closest('.movie').remove();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });


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

    const movies = document.querySelectorAll('.imageInfo');
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

function toggleContent(favDiv) {
    const contentDiv = favDiv.nextElementSibling;
    const toggleOpen = document.getElementById('open');
    const toggleShut = document.getElementById('shut');
    if (contentDiv && contentDiv.classList.contains('favContent')) {

        const currentDisplay = window.getComputedStyle(contentDiv).display;
        if (currentDisplay === 'none') {
            contentDiv.style.display = 'flex';
            favDiv.classList.add('active');
            toggleOpen.style.display = 'none';
            toggleShut.style.display = 'flex';
        } else {
            contentDiv.style.display = 'none';
            contentDiv.classList.remove('active');
            toggleOpen.style.display = 'flex';
            toggleShut.style.display = 'none';
        }
    }
}

function displayMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}