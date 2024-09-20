$(document).ready(function () {
        $('#id_phone_number').inputmask({
            mask: '+9999999999999',  // позволяет ввод от 1 до 13 символов после +
            placeholder: '',
            clearMaskOnLostFocus: false,
        });

        $('#id_phone_number_price').inputmask({
            mask: '+9999999999999',  // позволяет ввод от 1 до 13 символов после +
            placeholder: '',
            clearMaskOnLostFocus: false,
        });

        // Инициализация клавиатуры для нужных полей ввода
        initializeKeyboard('#id_name');
        initializeKeyboard('#id_name_price');
        initializeKeyboard('#id_name_sup');
        initializeKeyboard('#id_company');
        initializeKeyboard('#id_company_price');
        initializeKeyboard('#id_company_sup');
        initializeKeyboard('#id_phone_number');
        initializeKeyboard('#id_phone_number_price');
        initializeKeyboard('#id_email');
        initializeKeyboard('#id_email_price');
        initializeKeyboard('#id_email_sup');
        initializeKeyboard('#id_comment');
        initializeKeyboard('#id_comment_price');
        initializeKeyboard('#id_comment_sup');
    });
