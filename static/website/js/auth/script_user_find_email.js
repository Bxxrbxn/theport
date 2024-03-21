const first_name = document.getElementById("first-name");
const last_name = document.getElementById("last-name");
const phone = document.getElementById("phone");
const btn_submit = document.getElementById("btn-submit");
const result_email = document.getElementById("result-email");
const btn_submit_container = document.getElementById("btn-submit-container")

async function findEmail(){
    if(!validation()){
        return false;
    }
    $.ajax({
        type: "POST",
        url: "/api/find-email/",
        data: {
            "first_name" : first_name.value,
            "last_name" : last_name.value,
            "phone" : phone.value
        },
        datatype: "JSON",
        async: false,
        success: function (data) {
            result_email.innerHTML = `Your email is <strong>${data.email}</strong>`
            btn_submit_container.classList.add("d-none");
        },
        error: function (error) {
            alert(error.responseJSON.message);
        },
    });
}



//유효성 체크 함수
function validation() {
    if (first_name.value == "") {
        alert('성을 입력해주세요.');
        first_name.focus();
        return false;
    }
    if (last_name.value == "") {
        alert('이름을 입력해주세요.');
        last_name.focus();
        return false;

    }
    if (phone.value.length < 10) {
        phone.focus();
        return false;
    }
 
    return true;
}

function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}
