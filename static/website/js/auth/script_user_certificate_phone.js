const sms_certification_number = document.getElementById("sms_certification_number");
const phone = document.getElementById("phone");
const register_url = document.getElementById("register-url");
const certificated_phone = document.getElementById("certificated-phone");

const sms_certification_div = document.getElementById("sms_certification_div");
const btn_certificate_phone = document.getElementById("btn_certificate_phone");
const btn_next = document.getElementById("btn-next");

let time = 179;
let min, sec;
let timer;

async function certificatePhone(elem) {
    if (!regPhone(phone.value)) {
        phone.focus();
        return;
    }
    phone.readOnly = true;
    elem.disabled = true;

    $.ajax({
        type: "POST",
        url: "/api/certificate-phone/",
        data: {
            "phone": phone.value
        },
        datatype: "JSON",
        async: false,
        success: function(data) {
            elem.value = "re-send";
            elem.disabled = false;
            startTimer();
            sms_certification_div.classList.remove('d-none');
        },
        error: function(error) {
            alert(error.responseJSON.message);
            phone.readOnly = false;
            elem.disabled = false;
        },
    });

}

async function certificateNumber(elem) {
    if (!regPhone(phone.value)) {
        phone.focus();
        return;
    }
    if (sms_certification_number.value.length != 6) {
        sms_certification_number.focus();
        return;
    }
    sms_certification_number.readOnly = true;
    elem.disabled = true;

    $.ajax({
        type: "POST",
        url: "/api/validate-sms-certification-number/",
        data: {
            "phone": phone.value,
            "certification_number": sms_certification_number.value
        },
        datatype: "JSON",
        async: false,
        success: function(data) {
            alert(data.message);
            clearInterval(timer);
            phone.value = data.phone;
            btn_next.classList.remove("d-none");
            btn_certificate_phone.classList.add('d-none');
            sms_certification_div.classList.add('d-none');
            register_url.value = "/registration/";
            certificated_phone.value = data.phone;
        },
        error: function(error) {
            alert(error.responseJSON.message);
            sms_certification_number.readOnly = false;
            elem.disabled = false;
        },
    });
}

async function getRegisterPage(){
    if (!regPhone(phone.value)) {
        phone.focus();
        return;
    }
    const form = document.createElement('form');
    form.name = 'newForm';
    form.method = 'post';
    form.action = register_url.value;

    const input1 = document.createElement('input');
    const input2 = document.createElement('input');
    
    input1.setAttribute('type', 'hidden');
    input1.setAttribute('name', 'phone');
    input1.setAttribute('value', certificated_phone.value);
    input2.setAttribute('type', 'hidden');
    input2.setAttribute('name', 'csrfmiddlewaretoken');
    input2.setAttribute('value', csrftoken);

    form.appendChild(input1);
    form.appendChild(input2);

    document.body.appendChild(form);

    form.submit();
}

//전화번호 정규식
function regPhone(str) {
    let reg_phone = /^(1\s?)?(\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{4}$/;

    if (!reg_phone.test(str)) {
        alert('Invalid phone number format.');
        return false;
    }
    return true;
}

function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}


function startTimer() {
    clearInterval(timer);
    time = 179;
    document.getElementById("expiration_time").innerHTML = ``;
    timer = setInterval(countTimer, 1000);
}

function countTimer() {
    if (time < 0) {
        clearInterval(timer);
        document.getElementById("expiration_time").innerHTML = `timeout`;
    } else {
        min = parseInt(time / 60);
        sec = time % 60;
        document.getElementById("expiration_time").innerHTML = `${min} min ${sec} sec`;
        time--;
    }
}