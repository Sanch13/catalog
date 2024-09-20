'use strict';

function isEmptyField(valueField) {
    return valueField.trim() === "";
}

function isValidEmail(value) {
    return /\S+@\S+\.\S+/.test(value);
}

function showEmptyFieldError(nameInput, errorElement) {
    nameInput.classList.add("is-invalid");
    errorElement.textContent = "Поле не может быть пустым.";
}

function showLengthPhoneNumber(nameInput, errorElement) {
    nameInput.classList.add("is-invalid");
    errorElement.textContent =
        "Номер телефона должен содержать не менее 8 цифр.";
}

function handleSimpleFieldBlur(nameInput) {
    const valueField = nameInput.value;
    const errorElement = document.getElementById(nameInput.id + '-error');
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

function handlePhoneNumberBlur(nameInput) {
    const valueField = nameInput.value;
    const errorElement = document.getElementById(nameInput.id + '-error');
    let flag = false

    if (isEmptyField(valueField)) {
        showEmptyFieldError(nameInput, errorElement);
    } else if (valueField.length < 9) {
        showLengthPhoneNumber(nameInput, errorElement)
    } else {
        nameInput.classList.remove('is-invalid');
        errorElement.textContent = '';
        flag = true
    }
    return flag
}

function handleEmailBlur(nameInput) {
    const valueField = nameInput.value;
    const errorElement = document.getElementById(nameInput.id + '-error');
    let flag = false

    if (isEmptyField(valueField)) {
        showEmptyFieldError(nameInput, errorElement);
    } else if (!isValidEmail(valueField)) {
        errorElement.textContent = 'Введите корректный email';
    } else {
        nameInput.classList.remove('is-invalid');
        errorElement.textContent = '';
        flag = true
    }
    return flag
}

function handleDepartmentBlur(nameInput) {
    const valueField = nameInput.value;
    const errorElement = document.getElementById(nameInput.id + '-error');
    let flag = false

    if (valueField === "") {
        nameInput.classList.add("is-invalid");
        errorElement.textContent = 'Выберете отдел';
    } else {
        nameInput.classList.remove('is-invalid');
        errorElement.textContent = '';
        flag = true
    }
    return flag
}

function checkFields(name, company, phone_number, email) {
    const flag1 = handleSimpleFieldBlur(name)
    const flag2 = handleSimpleFieldBlur(company)
    const flag3 = handlePhoneNumberBlur(phone_number)
    const flag4 = handleEmailBlur(email)
    return flag1 && flag2 && flag3 && flag4;
}

function checkFieldsSupplierForm() {
    const flag1 = handleSimpleFieldBlur(formSupplierElem.name)
    const flag2 = handleSimpleFieldBlur(formSupplierElem.company)
    const flag3 = handleEmailBlur(formSupplierElem.email)
    const flag4 = handleDepartmentBlur(formSupplierElem.department)
    return flag1 && flag2 && flag3 && flag4;
}

function initializeKeyboard(selector) {
    $(selector).keyboard({
        layout: 'russian-qwerty',
        usePreview: false,
        autoAccept: true,
        position: {
            my: 'center top',
            at: 'center bottom'
        },
    });
}

function createFormGetSizeFile(category, ids){
    const data = new FormData();
    data.append("category", category);
    data.append("ids", ids ? JSON.stringify(ids.map(product => product.id)): '');
    return data
}

function createFormData(formElement, category, place, ids=null) {
    let data = new FormData(formElement);
        data.append("category", category);
        data.append("place", place);
        data.append("ids", ids ? JSON.stringify(ids.map(product => product.id)): '');
    return data
}
