function isEmptyField(valueField) {
    return valueField.trim() === "";
}

function isValidEmail(value) {
    return /\S+@\S+\.\S+/.test(value);
}

function showEmptyFieldError(nameInput, errorElement) {
    nameInput.classList.add('is-invalid');
    errorElement.textContent = "Поле не может быть пустым.";
}

document.addEventListener("DOMContentLoaded", function () {
    const nameInput = document.getElementById('id_name');
    const companyInput = document.getElementById('id_company');
    const phoneNumberInput = document.getElementById('id_phone_number');
    const emailInput = document.getElementById('id_email');

    nameInput.addEventListener('blur', handleNameBlur);
    companyInput.addEventListener('blur', handleCompanyBlur);
    phoneNumberInput.addEventListener('blur', handlePhoneNumberBlur);
    emailInput.addEventListener('blur', handleEmailBlur);

    function handleNameBlur() {
        const valueField = document.getElementById('id_name').value;
        const errorElement = document.getElementById('id_name' + '-error');
        let flag = false

        if (isEmptyField(valueField)) {
            showEmptyFieldError(nameInput, errorElement);
        } else {
            nameInput.classList.remove('is-invalid');
            errorElement.textContent = '';
            flag = true
        }
        return flag
    }

    function handleCompanyBlur() {
        const valueField = document.getElementById('id_company').value;
        const errorElement = document.getElementById('id_company' + '-error');
        let flag = false

        if (isEmptyField(valueField)) {
            showEmptyFieldError(companyInput, errorElement);
        } else {
            companyInput.classList.remove('is-invalid');
            errorElement.textContent = '';
            flag = true
        }
        return flag
    }

    function handlePhoneNumberBlur() {
        const valueField = document.getElementById('id_phone_number').value;
        const errorElement = document.getElementById('id_phone_number' + '-error');
        let flag = false

        if (isEmptyField(valueField)) {
            showEmptyFieldError(phoneNumberInput, errorElement);
        } else {
            phoneNumberInput.classList.remove('is-invalid');
            errorElement.textContent = '';
            flag = true

        }
        return flag
    }

    function handleEmailBlur() {
        const valueField = document.getElementById('id_email').value;
        const errorElement = document.getElementById('id_email' + '-error');
        let flag = false

        if (isEmptyField(valueField)) {
            showEmptyFieldError(emailInput, errorElement);
        } else if (!isValidEmail(valueField)) {
            errorElement.textContent = 'Введите корректный email';
        } else {
            emailInput.classList.remove('is-invalid');
            errorElement.textContent = '';
            flag = true
        }
        return flag
    }

    function checkFields() {
        const flag1 = handleNameBlur()
        const flag2 = handleCompanyBlur()
        const flag3 = handlePhoneNumberBlur()
        const flag4 = handleEmailBlur()
        return flag1 && flag2 && flag3 && flag4;
    }

    document.getElementById('contactForm').addEventListener('submit', function (event) {
        event.preventDefault();

        if (checkFields()) {
            let data = new FormData(this);
            data.append("ids", JSON.stringify(get_ids()));
            data.append("category", 'jar');
            data.append("place", 'catalog');

            fetch("{% url 'catalog:send_data_to_email' %}", {
                method: 'POST',
                body: data,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('popupForm').style.display = 'none';
                        document.getElementById('successPopup').style.display = 'flex';

                        document.getElementById('contactForm').reset();

                        setTimeout(function () {
                            document.getElementById('successPopup').style.display = 'none';
                        }, 3000); // Закрытие через 3 секунды
                    } else {
                        alert('Ошибка: ' + JSON.stringify(data.errors));
                    }
                });
        }
    });

    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        if (isNaN(e.target.value)) {
            e.target.value = e.target.value.replace(/\D/g, '');
        }
    });

    const checkbox = document.getElementById('rulesCondition');
    const submitButton = document.getElementById('sendForm');

    checkbox.addEventListener('change', function() {
        submitButton.disabled = !checkbox.checked;
    });

});


