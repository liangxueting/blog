from django.shortcuts import render, HttpResponse,redirect
from blog.my_forms import *
from blog.utils import function
from blog.my_forms import UserForm
# 注册
def enroll(request):
    # 定义一个空字典
    res = {'status': None, 'info': None}  # 与用户交互时返回给客户的交互信息
    import json
    if request.POST.get('sendSms') == '1':
        # 获取前端传过来的手机号
        tel = request.POST.get('user_tel')
        # 执行函数获取随机的四位数验证码
        range_num = function.range_num(4)
        # 将随机生成的四位数的验证码，存入到session缓存中
        request.session['phoneCode'] = range_num
        # 调用发送短信的函数 传入相应的参数
        # result = sendMsg.request2(tel,range_num,"GET")
        result = "ok"

        if result == 'ok':
            # 判断当发送成功时，执行下面操作
            res['status'] = 1
            res['info'] = '发送成功%s' % range_num
            # res['info'] = '发送成功'
            print(res)
            return HttpResponse(json.dumps(res))  # 将结果过返回给前台用户使用者，ajax
        else:
            # 当发送失败时，执行下面操作
            res['status'] = 3
            res['info'] = '发送失败'
            print(res)
            return HttpResponse(json.dumps(res))

        #  当点击登录按钮时执行的操作

    if request.POST.get('dosubmit') == '1':
        print(request.POST)
        # 获取前端页面的随机验证码
        validCode_form = request.POST.get('phoneCode')
        # 获取session中缓存的随机验证码
        # print(validCode_form)
        validCode_session = request.session.get('phoneCode')
        # 判断validcode_form是否存在
        # print(validCode_session)
        if validCode_form:
            # print(11111111111111)
            # 对比前端页面输入的随机验证码和session中缓存的随机验证码是否相同
            if validCode_form != validCode_session:
                res["status"] = 3
                res['info'] = '短信验证码不正确'

            elif validCode_form == validCode_session:
                # print(22222222222)
                valid_code = request.POST.get('chartCode')
                valid_code_str = request.session.get('valid_code_str')
                # print(valid_code)
                # print(valid_code_str)
                if valid_code:
                    # print(333333)
                    if valid_code.upper() == valid_code_str.upper():
                        # print(4444)
                        # print(request.POST)

                        form = UserForm(request.POST)  # 获取UserForm处理过的form表单的数据
                            # 判断如果获取的数据记录符合用户信息的规则(not 符合规则)
                        # print(form.errors)
                        if not form.is_valid():
                            # print(5555)
                            # 所有的干净的(原始的数据){'username':'11','pwd':'111','r_pwd':'111','email':'643353453@qq.com','tel':'15239970225'}
                            # 导入json序列化的包
                            res['status'] = 0
                            res['info'] = form.errors
                            # print(form.errors)
                            # print(form.cleaned_data)
                            # print("走到这")
                        else:
                            # 将结果序列化并传输到前端
                            member_email = request.POST.get("member_email")
                            member_tel = request.POST.get('member_tel')
                            member_name = request.POST.get('member_name')
                            member_nickname = request.POST.get('member_nickname')
                            member_pwd = request.POST.get('member_pwd')
                            # # 将符合条件的数据插入数据库

                            user_obj = Member.objects.create(member_name=member_name,member_tel=member_tel,member_email=member_email,member_nickname=member_nickname,member_pwd=member_pwd)
                            if user_obj:
                                res['status'] = 1
                                res['info'] = '登录成功!'
                                # return redirect('/index/')
                                # print(res)
                            else:
                                res['status'] = 2
                                res['info'] = '登录失败!'
                            request.session['member_id'] = user_obj.member_id  # 设置用户id
                            request.session['member_name'] = user_obj.member_name  # 设置用户名
                            return HttpResponse(json.dumps(res))

                    else:

                        res['status'] = 3
                        res['info'] = '验证码不正确!'
                        # print(res)
                return HttpResponse(json.dumps(res))
            else:
                # 当验证码不存在时
                res['status'] = 3
                res['info'] = '短信验证码不存在'

                # print(res)
            return HttpResponse(json.dumps(res))

    return render(request, 'login/enroll.html', locals())


