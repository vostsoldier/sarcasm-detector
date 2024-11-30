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