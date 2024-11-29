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
        messageElement.classList.add('pop');
        setTimeout(() => {
            messageElement.classList.remove('pop');
            messageElement.classList.add('explode');
            setTimeout(() => {
                messageElement.classList.remove('explode');
            }, 500);
        }, 300);
    });
});