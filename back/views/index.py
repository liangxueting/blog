from django.shortcuts import render,HttpResponse,redirect
from blog.models import Member
from back.models import Conservator
from back.utils import validCode
# 导入时间模块
from datetime import datetime
def index(request):
    return render(request,'index/index.html')
def top(request):
    conservator_id = request.session.get('conservator_id')
    conservator_obj = Conservator.objects.filter(conservator_id=conservator_id).first()
    # print(request)
    # print(conservator_id)
    # print(conservator_obj)
    return render(request,'index/top.html',locals())
def left(request):
    return render(request,'index/left.html')

def left2(request):
    return render(request,'index/left2.html')

def main(request):
    conservator_id = request.session.get('conservator_id')
    # print(conservator_id)
    # print('*'*100)
    conservator_obj = Conservator.objects.filter(conservator_id= conservator_id).first()
    # print(conservator_obj)
    # 获取当前年月入时间
    newday = datetime.today()
    # 获取当前的时间小时
    newtime = str(newday.time())[:2]

    print(newday)
    return render(request,'index/main.html',locals())
def footer(request):
    return render(request,'index/footer.html')
def login(request):
    res={'status':None,'info':None}
    if request.method == 'POST':
        valid_code = request.POST.get('valid_code')
        valid_code_str = request.session.get('valid_code_str')
        if valid_code.upper() == valid_code_str.upper():
            # 查询用户和密码是否正确
            username = request.POST.get('username')
            pwd = request.POST.get('pwd')
            # print(username,pwd,valid_code_str)
            conservator_obj = Conservator.objects.filter(conservator_name=username,conservator_pwd=pwd).first()
            if conservator_obj:
                res['status'] = 1
                res['info'] = '登陆成功!'
                # 将登录的管理员id存入session
                request.session['conservator_id'] = conservator_obj.conservator_id  # 设置用户id
                request.session['conservator_name'] = conservator_obj.conservator_name  # 设置用户id
                print(request.session['conservator_id'])
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

    return render(request, 'index/login.html')

# 基于PIL模块定义一个动态生成相应状态码图片
def get_valid_code_img(request):
    img_data = validCode.get_valid_code_img(request)
    return HttpResponse(img_data)

# 注销功能 开始 dt
# 导入Django模块
from django.contrib.auth import logout
def logout_auth(request):
    # logout(request)
    del request.session['conservator_id']
    return redirect("/back/login/")
# 注销功能 结束 dt
# 无权访问 开始
def no_power(request):
    return render(request,'rbac/no_power.html')
# 无权访问 结束
