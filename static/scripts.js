document.addEventListener('DOMContentLoaded', function() {
    const wordForm = document.getElementById('wordForm');
    if (wordForm) {
        wordForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const word = document.getElementById('word').value;
            fetch('/add_word', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ word: word })
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('message');
                messageElement.innerText = data.message;
                messageElement.className = data.status === 'error' ? 'error' : 'success';
                if (data.status === 'error') {
                    messageElement.classList.add('shake');
                    setTimeout(() => {
                        messageElement.classList.remove('shake');
                    }, 500);
                } else {
                    messageElement.classList.add('bounce');
                    setTimeout(() => {
                        messageElement.classList.remove('bounce');
                    }, 500);
                    document.getElementById('word').value = '';
                }

                if (data.new_achievements && data.new_achievements.length > 0) {
                    showNotification(data.new_achievements);
                    confetti();
                }
            });
        });
    }

    const wordGameForm = document.getElementById('wordGameForm');
    if (wordGameForm) {
        wordGameForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = event.target;
            const pairs = form.querySelectorAll('.word-game-pair');
            let correct = 0;
            pairs.forEach(pair => {
                const select = pair.querySelector('select');
                const selectedWord = select.value;
                const definition = pair.querySelector('label').innerText;
                if (getWordByDefinition(definition) === selectedWord) {
                    correct++;
                }
            });
            const messageElement = document.getElementById('gameMessage');
            messageElement.innerText = `You got ${correct} out of ${pairs.length} correct!`;
        });
    }

    const closeUpdatesButton = document.getElementById('closeUpdates');
    if (closeUpdatesButton) {
        closeUpdatesButton.addEventListener('click', function() {
            document.getElementById('updates').style.display = 'none';
        });
    }

    const updatesToggle = document.getElementById('updates-toggle');
    const updatesTab = document.getElementById('updates');

    updatesToggle.addEventListener('click', function() {
        updatesTab.classList.toggle('active');
        updatesToggle.classList.toggle('active');
    });

    if (closeUpdatesButton) {
        closeUpdatesButton.addEventListener('click', function() {
            updatesTab.classList.remove('active');
            updatesToggle.classList.remove('active');
        });
    }

    const popup = document.getElementById('howToPlayPopup');
    const closePopupButton = document.getElementById('closePopup');
    const doNotShowAgainCheckbox = document.getElementById('doNotShowAgain');
    if (popup && closePopupButton && doNotShowAgainCheckbox) {
        if (!sessionStorage.getItem('doNotShowHowToPlay') && !sessionStorage.getItem('popupShown')) {
            popup.style.display = 'flex';
            sessionStorage.setItem('popupShown', 'true');
        }

        closePopupButton.addEventListener('click', function() {
            if (doNotShowAgainCheckbox.checked) {
                localStorage.setItem('doNotShowHowToPlay', 'true');
            }
            popup.style.display = 'none';
            startTutorial();
        });
    }

    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.classList.add('fade-out');
        }, 3000);
        flash.addEventListener('transitionend', () => {
            flash.remove();
        });
    });

    const closeFeatureRequest = document.getElementById('closeFeatureRequest');
    const featureRequestBox = document.getElementById('featureRequestBox');

    if (closeFeatureRequest && featureRequestBox) {
        closeFeatureRequest.addEventListener('click', function() {
            featureRequestBox.style.display = 'none';
        });
    }
    const featureRequestForm = document.querySelector('.feature-request-box form');
    if (featureRequestForm) {
        const featureRequestURL = featureRequestForm.getAttribute('action'); 
        
        featureRequestForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const featureRequestBox = document.getElementById('featureRequestBox');
            const description = featureRequestBox.querySelector('textarea').value;

            fetch(featureRequestURL, {  
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ description: description })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const thankYouMessage = document.getElementById('thankYouFeatureRequest');
                    thankYouMessage.style.display = 'block';
                    
                    setTimeout(() => {
                        thankYouMessage.style.display = 'none';
                    }, 3000); 
                    document.getElementById('featureRequestBox').querySelector('textarea').value = '';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error submitting feature request:', error);
            });
        });
    }
    const friendListButton = document.getElementById('friendListButton');
    const friendListPopup = document.getElementById('friendListPopup');
    const closeFriendList = document.getElementById('closeFriendList');

    if (friendListButton && friendListPopup && closeFriendList) {
        friendListButton.addEventListener('click', () => {
            friendListPopup.style.display = 'flex';
        });

        closeFriendList.addEventListener('click', () => {
            friendListPopup.style.display = 'none';
        });

        window.addEventListener('click', (event) => {
            if (event.target === friendListPopup) {
                friendListPopup.style.display = 'none';
            }
        });
    }

    const socket = io();
    socket.on('leaderboard_update', function(data) {
        const leaderboardList = document.querySelector('.leaderboard ul');
        leaderboardList.innerHTML = '';
        data.forEach(user => {
            const li = document.createElement('li');

            const a = document.createElement('a');
            a.href = `/user/${user.id}`;
            a.textContent = user.username;

            const span = document.createElement('span');
            span.textContent = `${user.contributions} contributions`;

            li.appendChild(a);
            li.appendChild(span);
            leaderboardList.appendChild(li);
        });
    });
    const notification = document.getElementById('notification');
    if (notification) {
        notification.setAttribute('aria-live', 'assertive');
        notification.setAttribute('role', 'alert');
    }

    const shopForms = document.querySelectorAll('.shop-item form');
    shopForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('message');
                messageElement.innerText = data.message;
                messageElement.className = data.status === 'error' ? 'error' : 'success';

                if (data.status === 'success' && data.item_type === 'background_color') {
                    document.body.style.backgroundColor = data.color;
                }
            });
        });
    });
    const redeemForms = document.querySelectorAll('.redeem-form');
    redeemForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('message');
                if (data.status === 'success') {
                    messageElement.textContent = data.message;
                    messageElement.className = 'success';
                    
                    if (data.color) {
                        document.body.style.backgroundColor = data.color; 
                    }
                } else {
                    messageElement.textContent = data.message;
                    messageElement.className = 'error';
                }
            })
            .catch(error => {
                console.error('Error redeeming item:', error);
            });
        });
    });
});

function showNotification(achievements) {
    const notification = document.getElementById('notification');
    notification.innerHTML = achievements.map(ach => `<img src="${ach.image}" alt="${ach.name}"> ${ach.name}`).join('<br>');
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

function getWordByDefinition(definition) {
    const wordDefinitions = JSON.parse(document.getElementById('wordDefinitions').textContent);
    for (const [word, def] of Object.entries(wordDefinitions)) {
        if (def === definition) {
            return word;
        }
    }
    return null;
}

function startTutorial() {
    introJs().start();
}