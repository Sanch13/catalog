


function isEmptyField(value) {
    return value.trim() === "";
}


function showEmptyFieldError(elementId, errorElement) {
    errorElement.textContent = "Поле не может быть пустым.";
}
