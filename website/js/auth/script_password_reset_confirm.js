document.addEventListener('DOMContentLoaded', function() {
    const btnSubmit = document.getElementById('btn-submit');
    const passwordForm = document.getElementById('passwordForm');

    btnSubmit.addEventListener('click', function() {
        const formData = new FormData(passwordForm);
        // 서버에 비밀번호 재설정 요청 보내기
        // 'password-reset-confirm-endpoint'는 실제 서버의 엔드포인트로 교체해야 합니다.
        fetch('password-reset-confirm-endpoint', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 비밀번호 재설정 성공 시 처리
                alert('Your password has been successfully reset.');
                window.location.href = '/login'; // 로그인 페이지로 리다이렉션
            } else {
                // 비밀번호 재설정 실패 시 처리
                alert('Failed to reset password. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
    });
});