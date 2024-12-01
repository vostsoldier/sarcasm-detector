document.getElementById('wordForm').addEventListener('submit', function(event) {
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
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('howToPlayPopup');
    const closePopupButton = document.getElementById('closePopup');
    const doNotShowAgainCheckbox = document.getElementById('doNotShowAgain');

    // Check if the user has previously chosen to not show the popup
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
});
document.getElementById('closeUpdates').addEventListener('click', function() {
    document.getElementById('updates').style.display = 'none';
});