from django.shortcuts import render, HttpResponse,redirect
from blog.models import Member
import json
# 登录功能
def newtext(request):
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        print(pwd)
        print(username)
        member_obj = Member.objects.filter(member_name=username, member_pwd=pwd).first()
        print(member_obj)
        if member_obj:
            res['status'] = 1
            res['info'] = '登陆成功'
            print(res)
            # 设置成session
            # 当用户名与密码符合数据库中的记录时显示登录成功并存下session缓存
            request.session['member_id'] = member_obj.member_id  # 设置用户id
            request.session['member_name'] = member_obj.member_name  # 设置用户名
            member_obj = Member.objects.filter(member_name = username).first()

        elif member_obj != username :
            res['status'] = 0
            res['info'] = '用户不存在'
        else:
            res['status'] = 0
            res['info'] = '登录失败'
            # print(res)

        # import json
        return HttpResponse(json.dumps(res))
    return render(request, 'login/newtext.html', locals())


# 注销功能 开始 dt
# 导入Django模块
from django.contrib.auth import logout
def logout_auth(request):
    # logout(request)
    # 删除指定的session值
    del request.session['member_id']
    del request.session['member_name']
    # request.session['member_name'].flush()
    # print(logout(request))
    return redirect("/blog/index/")

# 注销功能 结束 dt