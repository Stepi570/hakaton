document.getElementById('registrationForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Проверка валидности формы
    if (!this.checkValidity()) {
        // Если форма не валидна, показываем сообщения об ошибках
        this.reportValidity();
        return;
    }

    // Получаем данные формы
    const formData = {
        lastName: document.getElementById('lastName').value,
        firstName: document.getElementById('firstName').value,
        middleName: document.getElementById('middleName').value,
        birthDate: document.getElementById('birthDate').value,
        passportNumber: document.getElementById('passportNumber').value
    };

    // Здесь можно добавить обработку данных (например, отправку на сервер)
    console.log('Данные для регистрации:', formData);

    // Пример использования eel (если нужно)
    // eel.register_user(formData)(function(response) {
    //     console.log('Ответ от Python:', response);
    //     window.location.href = 'webHV1.html';
    // });

    // Перенаправление на webHV1.html
    window.location.href = 'webHV1.html';
});
// Добавьте в script.js
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        const link = item.getAttribute('href');
        if (link === currentPage) {
            item.classList.add('active');
        }
    });
});
// Обработка формы перевода
document.getElementById('transferForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const cardNumber = document.getElementById('cardNumber').value;
    const amount = document.getElementById('amount').value;

    if (!cardNumber || !amount) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    // Здесь можно добавить логику обработки перевода
    console.log(`Перевод ${amount}₽ на карту ${cardNumber}`);

    // Показываем уведомление об успешном переводе
    alert(`Перевод на сумму ${amount}₽ успешно отправлен!`);

    // Очищаем форму
    this.reset();
});

// Форматирование номера карты
document.getElementById('cardNumber').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/g, '');

    if (value.length > 0) {
        value = value.match(new RegExp('.{1,4}', 'g')).join(' ');
    }

    e.target.value = value;
});