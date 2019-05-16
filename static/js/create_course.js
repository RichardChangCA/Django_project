$(function () {/* 文档加载，执行一个函数*/
    console.log("verify_create_course_log")
    $('#create_course_id')
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

                course_name: {//验证input项：验证规则
                    message: 'The username is not valid',

                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '课程名不能为空'

                        },
                        stringLength: {
                            min: 1,
                            max: 20,
                            message: '课程名长度必须在1到20之间'
                        },
                        threshold: 1, //有1字符以上才发送ajax请求，（input中输入一个字符，插件会向服务器发送一次，设置限制，1字符以上才开始）
                        remote: {//ajax验证。server result:{"valid",true or false} 向服务发送当前input name值，获得一个json数据。例表示正确：{"valid",true}
                            url: '/course_verify/',//验证地址
                            message: '课程已存在',//提示消息
                            delay: 2000,//每输入一个字符，就发ajax请求，服务器压力还是太大，设置2秒发送一次ajax（默认输入一个字符，提交一次，服务器压力太大）
                            type: 'POST',//请求方式
                            /**自定义提交数据，默认值提交当前input value*/
                            data: function(t) {

                               return {
                                   cour_num_verify: $('[name="course_id"]').val(),
                                   email_verify: $('[name="email"]').val()
                                   // whatever: $('[name="whateverNameAttributeInYourForm"]').val()
                               };
                            }

                        },
                        regexp: {
                            regexp: /^.+$/,
                            message: ''
                        }
                    }
                },

                course_id: {
                    message: 'The student number is not valid',
                    validators: {
                        notEmpty: {
                            message: '课程号不能为空'
                        },
                        stringLength: {
                            min: 7,
                            max: 7,
                            message: '请输入7位课程号'
                        },
                        regexp: {
                            regexp: /^([0-9]{7})$/,
                            message: '请输入正确的课程号'
                        }
                    }
                },

            }
        })
});