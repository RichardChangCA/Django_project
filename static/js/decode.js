$(function () {/* 文档加载，执行一个函数*/
    console.log("verify_decode_tag_log");
    $('#decodeForm')
        .bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                /*input状态样式图片*/
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                /*验证：规则*/
                decode: {//验证input项：验证规则
                    message: 'The code is not valid',
                    validators: {
                        stringLength: {
                            max: 16,
                            message: '长度不能超过16个字符'
                        },
                        regexp: {//匹配规则
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: 'The code can only consist of alphabetical, number, dot and underscore'
                        }
                    }
                },
            }
        })
});