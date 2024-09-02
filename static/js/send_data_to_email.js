//    Возвращает    список    ids
function get_ids() {
    const cards = document.querySelectorAll('.card');
    const ids = [];

    cards.forEach(function (card) {
        ids.push(card.id);
    });
    return ids
}

//    Запрос    на    размер    отправляемого    файла
document.getElementById('openPopup').addEventListener('click', function () {
    document.getElementById('popupForm').style.display = 'flex';
    const data = new FormData();
    data.append('ids', JSON.stringify(get_ids()));

    fetch("{% url 'catalog:get_size_list_files' %}", {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Если ответ успешный, вставляем размер файла в блок div
                document.getElementById('fileSizeDisplay').innerText = `Размер файла: ${data.file_size} `;
            } else {
                // Если возникла ошибка, отображаем сообщение об ошибке
                document.getElementById('fileSizeDisplay').innerText = "Ошибка при получении размера файла.";
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            document.getElementById('fileSizeDisplay').innerText = "Произошла ошибка при выполнении запроса.";
        });
});

//     Закрытие    попапа    по    кнопке    Х
document.getElementById('closePopup').addEventListener('click', function () {
    document.getElementById('popupForm').style.display = 'none';
});

//    Закрытие    попапа    по    клику    вне    окна
document.addEventListener('click', function (event) {
    let popup = document.querySelector('.popup-content');
    let formPopup = document.getElementById('popupForm');
    if (formPopup.style.display === 'flex' && !popup.contains(event.target) && event.target.id !== 'openPopup') {
        formPopup.style.display = 'none';
    }
});

//    Закрытие    успешного    попапа    по    клику    вне    окна
document.addEventListener('click', function (event) {
    let popup = document.querySelector('.success-popup-content');
    let formPopup = document.getElementById('successPopup');
    if (formPopup.style.display === 'flex' && !popup.contains(event.target) && event.target.id !== 'openPopup') {
        formPopup.style.display = 'none';
    }
});

//    Отправка    форма    по    нажатию    на    кнопку    Отправить
document.getElementById('contactForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let data = new FormData(this);
    data.append("ids", JSON.stringify(get_ids()));

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
});