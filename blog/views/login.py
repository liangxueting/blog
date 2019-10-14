from django.shortcuts import render, HttpResponse,redirect
from blog.models import Member
 # 导入Django的加密解密包
from blog.utils import validCode
import json

# 定义一个图形验证码的方法
def login(request):
    res={'status':None,'info':None}
    if request.method == 'POST':
        valid_code = request.POST.get('valid_code')
        valid_code_str = request.session.get('valid_code_str')
        if valid_code.upper() == valid_code_str.upper():
            # 查询用户和密码是否正确
            username = request.POST.get('username')
            pwd = request.POST.get('pwd')
            member_obj = Member.objects.filter(member_name=username,member_pwd=pwd).first()
            if member_obj:
                res['status'] = 1
                res['info'] = '登录成功!'
                # print(res)
                # return redirect('/blog/index/')
            else:

                res['status'] = 0
                res['info'] = '账号或密码错误！'
                # print(res)
            import json
            response_new = HttpResponse(json.dumps(res))  # 将结果返回给前台页面

            return response_new
        else:
            res['status'] = 2
            res['info'] = '验证码不正确！'
            # print(res)

        import json
        response_new = HttpResponse(json.dumps(res)) #将结果返回给前台页面

            # request.session['member_id'] = 2
        return response_new
        # return redirect('/blog/index/')

    return render(request, 'login/login.html', locals())


# 基于PIL模块定义一个动态生成相应状态码图片
def get_valid_code_img(request):
    img_data = validCode.get_valid_code_img(request)
    return HttpResponse(img_data)


from blog.utils import sendMsg #引入自定义的验证码
from blog.utils import function #引入自定义的验证码



# 手机号码验证码
def loginTel(request):
    res = {'status':None,'info':None}  #定义一个空的字典用于用户交互的信息
    import json

    # 点击发送短信执行下面程序
    # 判断是否点击获取手机短信验证码，当点击时
    if request.POST.get('sendSms')=='1':
        # 获取前端传过来的手机号
        tel = request.POST.get('user_tel')
        # 执行函数获取随机的四位数验证码
        range_num = function.range_num(4)
        # 将随机生成的四位数的验证码，存入到session缓存中
        request.session['validcode'] = range_num

        # 调用发送短信的函数 传入相应的参数
        # result = sendMsg.request2(tel,range_num,"GET")
        result = "ok"

        if result == 'ok':
            # 判断当发送成功时，执行下面操作
            res['status'] = 1
            res['info'] = '发送成功%s'%range_num
            # res['info'] = '发送成功'
            print(res)
            return HttpResponse(json.dumps(res))  #将结果过返回给前台用户使用者，ajax

        else:
            # 当发送失败时，执行下面操作
            res['status'] = 0
            res['info'] = '发送失败'
            print(res)
            return HttpResponse(json.dumps(res))


    # 当点击登录按钮时执行的操作
    #    request.POST.get('sendSms') == '1':
    if request.POST.get('dosubmit')== '1':
        # 获取前端页面的随机验证码
        validCode_form = request.POST.get('validcode')
        # 获取session中缓存的随机验证码
        validCode_session = request.session.get('validcode')
        # 判断validcode_form是否存在
        if validCode_form:
        # 对比前端页面输入的随机验证码和session中缓存的随机验证码是否相同
            if validCode_form != validCode_session:
                res["status"] = 0
                res['info'] = '短信验证码不正确'
                print(res)
                return HttpResponse(json.dumps(res))
        else:
            # 当验证码不存在时
            res['status'] = 0
            res['info'] = '短信验证码不存在'
            print(res)
            return HttpResponse(json.dumps(res))

        # 判断手机号是否在数据库表中
        # 获取前端页面的手机号
        tel = request.POST.get('user_tel')
        print(tel)
        user_obj = Member.objects.filter(member_tel=tel)
        if user_obj:
            res['status'] = 1
            res['info'] = '登录成功!'
            print(res)
        else:
            res['status'] = 0
            res['info'] = '没有该用户!'
        return HttpResponse(json.dumps(res))


    return render(request,'login/loginTel.html',locals())


# 登录综合
def login_all(request):
    # 定义一个图形验证码的方法
    res = {'status': None, 'info': None}
    import json
    # 手机号码验证码
    # def loginTel(request):
        # res = {'status': None, 'info': None}  # 定义一个空的字典用于用户交互的信息
        # 点击发送短信执行下面程序
        # 判断是否点击获取手机短信验证码，当点击时
    if request.POST.get('sendSms') == '1':
        # 获取前端传过来的手机号
        tel = request.POST.get('user_tel')
        # 执行函数获取随机的四位数验证码
        range_num = function.range_num(4)
        # 将随机生成的四位数的验证码，存入到session缓存中
        request.session['validcode'] = range_num
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
            res['status'] = 0
            res['info'] = '发送失败'
            print(res)
            return HttpResponse(json.dumps(res))

        # # 当点击登录按钮时执行的操作
        # #    request.POST.get('sendSms') == '1':

    if request.POST.get('dosubmit') == '1':
        print(request.POST)
         # 获取前端页面的随机验证码
        validCode_form = request.POST.get('validcode')
        # 获取session中缓存的随机验证码
        # print(validCode_form)
        validCode_session = request.session.get('validcode')
        # 判断validcode_form是否存在
        # print(validCode_session)
        if validCode_form:
            # 对比前端页面输入的随机验证码和session中缓存的随机验证码是否相同
            if validCode_form != validCode_session:
                res["status"] = 0
                res['info'] = '短信验证码不正确'


            elif validCode_form == validCode_session:
                valid_code = request.POST.get('valid_code')
                valid_code_str = request.session.get('valid_code_str')
                if valid_code:
                    if valid_code.upper() == valid_code_str.upper():
                        username = request.POST.get('username')
                        pwd = request.POST.get('pwd')
                        tel = request.POST.get('user_tel')

                        user_obj = Member.objects.filter(member_tel=tel,member_name=username,member_pwd=pwd)
                        if user_obj:
                            res['status'] = 1
                            res['info'] = '登录成功!'
                            # print(res)

                        else:
                            res['status'] = 2
                            res['info'] = '该用户不存在!'
                        return HttpResponse(json.dumps(res))

                    else:

                        res['status'] = 0
                        res['info'] = '验证码不正确!'
                        # print(res)
                return HttpResponse(json.dumps(res))
            else:
                # 当验证码不存在时
                res['status'] = 0
                res['info'] = '短信验证码不存在'

                # print(res)
            return HttpResponse(json.dumps(res))

    return render(request,'login/login_all.html',locals())