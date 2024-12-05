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
        });
    }
});

function showNotification(achievements) {
    const notification = document.getElementById('notification');
    notification.innerHTML = achievements.map(ach => `<img src="${ach.image}" alt="${ach.name}"> ${ach.name}`).join('<br>');
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

function confetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
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