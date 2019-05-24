$(function () {/* 文档加载，执行一个函数*/
    console.log("verify_change_info_log")
    $('#defaultForm')
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
                username: {//验证input项：验证规则
                    message: 'The username is not valid',

                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '用户名不能为空'

                        },
                        stringLength: {
                            min: 1,
                            max: 20,
                            message: '用户名长度必须在1到20之间'
                        },
                        regexp: {
                            regexp: /^.+$/,
                            message: ''
                        }
                    }
                },
                password: {
                    message: '密码无效',
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 16,
                            message: '密码长度必须在6到16之间'
                        },
                        identical: {//相同
                            field: 'password', //需要进行比较的input name值
                            message: '两次密码不一致'
                        },
                        different: {//不能和用户名相同
                            field: 'username',//需要进行比较的input name值
                            message: '不能和用户名相同'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '密码只能是大小写字母、数字、点与下划线'
                        }
                    }
                },
                repassword: {
                    message: '密码无效',
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 16,
                            message: '密码长度必须在6到16之间'
                        },
                        identical: {//相同
                            field: 'password',
                            message: '两次密码不一致'
                        },
                        different: {//不能和用户名相同
                            field: 'username',
                            message: '不能和用户名相同'
                        },
                        regexp: {//匹配规则
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: 'The username can only consist of alphabetical, number, dot and underscore'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮件不能为空'
                        },
                        emailAddress: {
                            message: '请输入正确的邮件地址如：465074419@qq.com'
                        }
                    }
                },
                phone: {
                    message: 'The phone is not valid',
                    validators: {
                        notEmpty: {
                            message: '手机号码不能为空'
                        },
                        stringLength: {
                            min: 11,
                            max: 11,
                            message: '请输入11位手机号码'
                        },
                        regexp: {
                            regexp: /^1[3|5|8|9|6|7]{1}[0-9]{9}$/,
                            message: '请输入正确的手机号码'
                        }
                    }
                },
            }
        })

        //自动触发表单验证
        .on('success.form.bv', function (e) {//点击提交之后
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data 提交至form标签中的action，result自定义
            $.post('/personal_details/', $form.serialize(), function (result) {
//do something...
                if (result == 'OK') {
                    window.location.href = '/login/'
                }
            });
        });
});