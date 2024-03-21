function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}

function findEmail() {
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var phone = document.getElementById('phone').value;
    var resultContainer = document.getElementById('result-email');

    if (!firstName || !lastName || !phone) {
        alert('Please fill in all fields.');
        return;
    }

    // 서버에 요청을 보내기 위한 데이터 구성
    var data = {
        first_name: firstName,
        last_name: lastName,
        phone: phone
    };

    // Fetch API를 사용하여 서버에 데이터 전송
    // 'find-email-endpoint'는 실제 서버의 엔드포인트로 교체해야 합니다.
    fetch('find-email-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.email) {
            resultContainer.innerHTML = `<p>Your email is: ${data.email}</p>`;
        } else {
            resultContainer.innerHTML = `<p>Email not found. Please try again.</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultContainer.innerHTML = `<p>An error occurred. Please try again later.</p>`;
    });
}