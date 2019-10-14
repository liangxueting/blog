from django.shortcuts import render, HttpResponse,redirect
from blog.models import Article,Member,Word
from blog.models import Web
from django.db.models import F,Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json
# 导入随机数
from blog.utils import function
# 首页功能
def index(request):
    member_id = request.session.get('member_id')
    # 用户名是否存在
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()
    article_obj = Article.objects.all()[:3]
    article_obj01 = Article.objects.all().order_by('-article_addtime')[:6]
    web_obj = Web.objects.all()
    # print(web_obj[0].web_content)
    article_obj03 = Article.objects.all().order_by('-article_clicknum')[:3]
    article_obj04 = Article.objects.filter(article_is_recommend=1).order_by('-article_clicknum')[:3]

    # 获取前端页面的当前页面
    currentPage = int(request.GET.get('page', 1))

    # 遍历数据库数据渲染到前端页面
    article_list = Article.objects.all().order_by('-article_addtime')
    # 将数据库中的所有的记录传入到分液器函数中处理
    # 第一参数为数据库中的所有的记录
    # 第二个参数为前端页面展示的记录条数
    paginator = Paginator(article_list, 3)
    # print("*" * 10)
    # print(paginator)
    # 用paginator.num_pages可以获得数据的总的页数
    # print(paginator.num_pages)
    # 获取记录的总页数，判断当页数的总的页数大于当前的页数值时执行下面代码
    if paginator.num_pages > 5:
        # 判断当前页数显示
        # 当前页的值小于等于3时，显示1 - 6
        # 页
        if currentPage - 2 < 1:
            # 显示1 - 5
            # 页的记录
            pagRange = range(1,4)
            # 判断当前页面显示12页时 ，显示当前页 - 2
            # 14
            # 页
        elif currentPage + 1 > paginator.num_pages:
            pagRange = range(currentPage - 2, paginator.num_pages + 1)
            # 判断当选择的为最后一个页码时，显示最后5页
            if currentPage == paginator.num_pages:
                pagRange = range(currentPage - 2, paginator.num_pages + 1)
        else:
            # 判断当前显示页数在3 - 12
            # 3 - 2 = 1
            # 3 + 2 = 5
            # 12 - 2 = 10
            # 12 + 3 = 15
            pagRange = range(currentPage - 1, currentPage + 2)
    else:
        # 获取记录的总页数，判断总页数等于6， pageRange
        # 1 - 5
        pagRange =range(1,paginator.num_pages+1)
        print(pagRange)
        # print(type(pagRange))

    try:
        article_list = paginator.page(currentPage)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(1)
        # return render(request, 'index.html', locals())

    return render(request, 'login/index.html', locals())

def about(request):
    # 用户名是否存在
    username = request.session.get('member_id')
    web_obj = Web.objects.all()
    if username:
        member_obj = Member.objects.filter(member_id=username).first()
    return render(request,'login/about.html',locals())

# 留言功能 开始 dt
def gbook(request):
    res = {"status":None,'info':None}
    # 用户名是否存在
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()
    # 用户留言功能 开始 dt
    word_obj = Word.objects.all()
    word_name = request.GET.get('username')
    word_img = request.GET.get('heading')
    word_content = request.GET.get('content')
    print(word_name,word_img,word_content)
    # print(type(word_name),type(word_img),type(word_content))
    if word_name:
        if word_content:
            word_obj01 = Word.objects.create(word_name=word_name,word_content=word_content,word_img=word_img)
    # 用户留言功能 结束 dt
            res['status'] = 1
            res['info'] = '发表成功'
            return HttpResponse(json.dumps(res))
        else:
            # print(123)
            res['status'] = 0
            res['info'] = '你不想写点什么吗？'
        return HttpResponse(json.dumps(res))
    return render(request,'login/gbook.html',locals())
# 留言功能 结束 dt

# 文章搜索功能 开始 dt
def like_list(request):
    # 用户名是否存在
    username = request.session.get('member_id')
    if username:
        member_session_obj = Member.objects.filter(member_id=username).first()

    article_obj02 = Article.objects.order_by('-article_clicknum', '-article_addtime')[:4]
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()

    src = {'status':None,'info':None}
    if request.method =="GET":
        # print(request.GET)
        keyboard = request.GET.get('keyboard')
        member_id = request.GET.get('member_id')
        print(member_id)
        print(keyboard)
        if member_id:
            key_like01 = Article.objects.filter(membered__member_id = member_id)
            # print(key_like01.filter(article_title__icontains='个人'))

            if keyboard:
                key_like = key_like01.filter(Q(article_title__icontains=keyboard)|Q(article_description__icontains=keyboard)|Q(article_content__icontains=keyboard)|Q(membered__member_nickname__icontains=keyboard)).order_by('article_title','membered__member_nickname','article_description','article_content')

                if key_like:
                    src['status'] = 1
                    src['info'] = key_like
                    sr = keyboard
                else:
                    src["status"] = 0
                    src["info"] = '没有相关内容'
                    sr = keyboard
            else:

                src["status"] = 0
                src["info"] = '没有相关内容'
                sr = keyboard
        else:
            if keyboard:
                key_like = Article.objects.filter(
                    Q(article_title__icontains=keyboard) | Q(article_description__icontains=keyboard) | Q(
                        article_content__icontains=keyboard) | Q(
                        membered__member_nickname__icontains=keyboard)).order_by('article_title',
                                                                                 'membered__member_nickname',
                                                                                 'article_description',
                                                                                 'article_content')

                if key_like:
                    src['status'] = 1
                    src['info'] = key_like
                    sr = keyboard
                else:
                    src["status"] = 0
                    src["info"] = '没有相关内容'
            else:

                src["status"] = 0
                src["info"] = '没有相关内容'

            # lab = "<a href='{% url 'blog:diary' %}' >跳转列表页</a>"
    return render(request,'diary/like_list.html',locals())
# 文章搜索功能 结束 dt


# 找回密码 开始 dt
def get_pwd(request):
    # 导入email相关模块
    from django.core.mail import send_mail
    # 导入Email的配置文件
    from my_pro20 import settings
    # print(request.POST)
    res ={"status":None,'info':None}
    if request.method == "POST":
        username = request.POST.get('username')
        chartCode = request.POST.get('chartCode')
        valid_code_str = request.session.get('valid_code_str')
        member_email = Member.objects.filter(member_name=username).values('member_email').first()
        if member_email:
            if chartCode:
                if chartCode.upper() == valid_code_str.upper():
                    # 导入随机数作为密码
                    num = function.range_num(6)
                    print(username)
                    print(chartCode)
                    print(member_email['member_email'])
                        # 方法1：通过调用send_mail 函数 发送邮件
                    # send_mail(
                    #     '标题(找回密码)',
                    #     '您的密码已重置，新密码已发至您的邮箱，新密码为%s' % num,
                    #     settings.EMAIL_HOST_USER,
                    #     ['643353453@qq.com']
                    # )
                    #     方法2：多线程
                    import threading

                    t = threading.Thread(target=send_mail,args=(
                        '标题(找回密码)',   #邮件标题
                        '您的密码已重置，新密码已发至您的邮箱，新密码为%s' % num,  #邮件内容
                        settings.EMAIL_HOST_USER,   #发件人
                        [member_email['member_email']],   #收件人  列表或是元组格式
                    ))
                    t.start()
                    # 将修改后的密码重新写入数据库
                    newmember_pwd = Member.objects.filter(member_name=username).update(member_pwd=num)
                    if newmember_pwd:
                        res['status'] = 1
                        res['info'] = '您的密码已修改，新密码稍后将发送到您的邮箱，请使用新密码登录！'
                    else:
                        res['status'] = 0
                        res['info'] = '密码修改失败!'
                    return HttpResponse(json.dumps(res))
                # print(num)
                else:
                    res['status'] = 0
                    res['info'] = '验证码不正确！'
                return HttpResponse(json.dumps(res))
            else:
                res['status'] = 0
                res['info'] = '验证码不能为空！'
            return HttpResponse(json.dumps(res))
        else:
            res['status'] = 0
            res['info'] = '用户名不存在！'
        return HttpResponse(json.dumps(res))
    return render(request, 'login/get_pwd.html', locals())
# 找回密码 结束 dt
