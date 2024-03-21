function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}

function certificatePhone() {
    var phone = document.getElementById('phone').value;
    if (!phone) {
        alert('Please enter your phone number.');
        return;
    }

    // SMS 인증 번호를 전송하는 서버 로직 호출
    // 'send-sms-endpoint'는 실제 서버의 엔드포인트로 교체해야 합니다.
    fetch('send-sms-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({phone: phone}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('sms_certification_div').classList.remove('d-none');
            // 인증번호 전송 성공 메시지 처리
        } else {
            alert('Failed to send the verification number. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

function certificateNumber() {
    var smsCertificationNumber = document.getElementById('sms_certification_number').value;
    // SMS 인증 번호 검증 로직 호출
    // 'verify-sms-endpoint'는 실제 서버의 엔드포인트로 교체해야 합니다.
    fetch('verify-sms-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({smsCertificationNumber: smsCertificationNumber}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('btn-next').classList.remove('d-none');
            // 인증 성공 처리, 예를 들어 "Next" 버튼을 활성화
        } else {
            alert('Verification failed. Please check the number and try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

function getRegisterPage() {
    // 인증이 성공한 후, 사용자를 등록 페이지로 리디렉션하는 로직
    // 여기서는 예시로만 작성하였습니다.
    window.location.href = 'register-page-url'; // 실제 등록 페이지 URL로 교체해야 합니다.
}