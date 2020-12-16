function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function send_data(data) {
    fetch('/profile/', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },

        body: JSON.stringify(data),
    })
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function appointmentDelete(value) {
    let element = document.getElementById(value);
    element.remove();
    let data = {
        'id': value,
    }
    send_data(data);
}