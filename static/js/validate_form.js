document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('rulesCondition');
    const submitButton = document.getElementById('sendForm');

    checkbox.addEventListener('change', function() {
        submitButton.disabled = !checkbox.checked;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const checkbox2 = document.getElementById('rulesCondition2');
    const submitButton2 = document.getElementById('sendForm2');

    checkbox2.addEventListener('change', function() {
        submitButton2.disabled = !checkbox2.checked;
    });
});