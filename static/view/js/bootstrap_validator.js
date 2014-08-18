$(document).ready(function () {
    $('#loginForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            email: {
                validators: {
                    notEmpty: {
                        message: 'Введите свою почту'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'Необходимо ввести пароль'
                    }
                }
            }
        }
    });
});

$(document).ready(function () {
    $('#registrationForm')
        .bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Пол необходимо указать'
                        }
                    }
                },
            }
        });
    $('#profileForm').bootstrapValidator();
});