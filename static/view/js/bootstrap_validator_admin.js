$(document).ready(function () {
    $('#gameaddForm')
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
});

$(document).ready(function () {
    $('#courtaddForm').bootstrapValidator();
});