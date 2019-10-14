from django.shortcuts import render,reverse,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.db.models import F,Count
from blog.models import Article
from blog.models import Member,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from bs4 import BeautifulSoup

import json
# 博客日记的方法
def diary(request):
    member_id = request.session.get('member_id')
    # 判断sesion是否存在存在显示用户名
    if member_id:
        member_session_obj = Member.objects.filter(member_id=member_id).first()

    article_obj = Article.objects.all().order_by('-article_addtime')
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()
    article_obj02 = Article.objects.order_by('-article_clicknum')[:4]
    # 分页器 开始
    # 获取前端页面的当前页面
    currentPage = int(request.GET.get('page', 1))
    # 遍历数据库数据渲染到前端页面
    # article_list = Article.objects.all().order_by('-article_addtime')
    # 将数据库中的所有的记录传入到分液器函数中处理
    # 第一参数为数据库中的所有的记录
    # 第二个参数为前端页面展示的记录条数
    paginator = Paginator(article_obj, 3)
    # print("*" * 10)
    # print(paginator)
    # 用paginator.num_pages可以获得数据的总的页数
    print(paginator.num_pages)
    # 获取记录的总页数，判断当页数的总的页数大于当前的页数值时执行下面代码
    if paginator.num_pages > 3:
        # 判断当前页数显示
        # 当前页的值小于等于3时，显示1 - 6
        # 页
        if currentPage - 2 < 1:
            # 显示1 - 5
            # 页的记录
            pagRange = range(1, 4)
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
        pagRange = range(1, paginator.num_pages + 1)
        print(pagRange)
        # print(type(pagRange))

    try:
        article_obj = paginator.page(currentPage)
    except PageNotAnInteger:
        article_obj = paginator.page(1)
    except EmptyPage:
        article_obj = paginator.page(1)
        # return render(request, 'index.html', locals())
    # 分页器 结束
    return render(request, 'diary/diary.html', locals())


# 博客日记的内容的方法
def text(request,res):
    # 当前文章id

    article_dianji = Article.objects.filter(article_id=res).update(article_clicknum=F('article_clicknum') + 1)
    # print(article_dianji)
    article_obj = Article.objects.filter(article_id=res).first()
    # 上一篇文章
    article_top = Article.objects.filter(article_id__lt=res).order_by('-article_id').first()
    # 下一篇文章
    article_next = Article.objects.filter(article_id__gt=res).order_by('article_id').first()
    article_last = Article.objects.all().last()
    # print(article_top)
    # print(article_next)
    # link='<a href="http://www.baidu.com">百度</a>'
    # url = reverse('text',)
    link = article_obj.article_content
    # print(link)
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime')[:3]
    article_obj02 = Article.objects.all().order_by('article_clicknum')[:3]

    # 评论
    # username = request.GET.get('username')
    dosubmit = request.GET.get('dosubmit')
    comment = request.GET.get('saytext')
    article_id = request.GET.get('article_id')
    member_id = request.session.get('member_id')

    # 判断sesion是否存在存在显示用户名

    if member_id:
        member_session_obj = Member.objects.filter(member_id=member_id).first()
    # print(member_id)
    # print(request.GET)
    member_comment_obj = Member.objects.filter(member_id=member_id).first()
    comment_num = Comment.objects.filter(article__article_id=res).aggregate(Count('comment_id'))
    # print(comment_num)
    comment_newobj = Comment.objects.filter(article_id=res).order_by('comment_addtime')
    cue = {'status': None, 'info': None}
    if member_comment_obj:
        if dosubmit:
            if comment:

                # print(member_comment_obj.member_id)
                comment_obj = Comment.objects.create(comment_content = comment,article_id = article_id, member_id = member_comment_obj.member_id)
                # print('*'*100)
                # print(comment_obj.comment_addtime)
                cue['status'] = 1
                # 不能传对象
                cue['info'] = '评论成功!'

            else:
                cue['status'] = 0
                cue['info'] = '写点儿什么吧!'

            return HttpResponse(json.dumps(cue))

    # 点赞
    if request.method == "POST":
        try:
            # 定义一个字典用于返回给前段数据
            par = {'status': None, 'info': None}
            # print(request.POST)
            # 获取前端页面传过来的当前的文章id
            article_id = request.POST.get('article_id')
            # 获取文章的作者(点赞过的人的)id
            member_id = int(request.POST.get('membered_id'))
            # 获取当前登录的人的session缓存的用户id
            user = request.session['member_id']
            # print(user)
            if user:
                # 通过多对多查询出点赞过本文章的所有的用户的id
                articles_obj = Article.objects.filter(article_id=article_id).first()
                member_list = articles_obj.member_set.all().values("member_id")
                # print(member_list)
                # 创建一个空的列表
                list1 = []
                # 遍历点赞本文章的的所有的用户的id
                for v in member_list:
                    # 将评论过该文章的用户的id以追加的方式写入空列表
                    list1.append(v["member_id"])
                # 将缓存的用户的id与列表中的id进行对比 当当前的用户id不存在时可以点赞本文章
                if user not in list1:
                    # list1.append(member_id)
                    # print(list1)
                    # print(article_id)
                    # 修改数据库中的点赞的数据
                    article_obj05 = Article.objects.filter(article_id=article_id).update(
                        article_praise_num=F('article_praise_num') + 1)
                    # print(article_obj05)
                    # 将修改后的点赞的数据记录再次返回前端页面
                    article_obj03 = Article.objects.values('article_praise_num').filter(article_id=article_id)[0]
                    # 将当前登陆的用户的id添加到点赞表中
                    praise = articles_obj.member_set.add(user)
                    # print(article_obj03)
                    par["status"] = 1
                    par['info'] = article_obj03
                    # return HttpResponse(json.dumps(par))
                else:
                    # 存在时返回已点赞
                    par["status"] = 0
                    par['info'] = "已经赞过了！"
                return HttpResponse(json.dumps(par))
        except KeyError:
            par["status"] = 2
            par['info'] = "正在跳转登录页面..."
                # raise ValidationError('两次密码不一致！')

        return HttpResponse(json.dumps(par))
    return render(request, 'diary/text1.html', locals())



# 个人列表页
def person_list(request,res):
    # 用户判断用户session是否存在
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()

    article_obj = Article.objects.filter(membered_id=res).order_by('-article_addtime')
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()
    article_obj02 = Article.objects.order_by('-article_clicknum')[:4]
    article_obj03 = Article.objects.filter(membered_id=res).first()

    return render(request,'diary/person_list.html',locals())

# 个人中心列表页
def person_core(request):
    # 用户判断用户session是否存在
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()
        article_obj = Article.objects.filter(membered_id=username).order_by('-article_addtime')
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()
    article_obj02 = Article.objects.order_by('-article_clicknum')[:4]

    return render(request, 'diary/person_core.html', locals())

# 个人中心文章删除页
def person_del(request):
    print(request.POST)
    id = request.POST.get('id')
    print(id)
    result = Article.objects.filter(article_id=id).delete()
    res = {'status':None,'info':None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))


# 个人文章修改
def person_update(request,res):
    article_update = Article.objects.filter(article_id=res).first()
    article_update_num = 1
    print(request.POST)
    dosubmit = request.POST.get('dosubmit')
    if request.method == 'POST':
        if dosubmit == '修改':
            title = request.POST.get('title')
            description = request.POST.get('article_description')
            content = request.POST.get('content')
            times = request.POST.get('time')
            member_id = request.session.get('member_id')
            article_img = request.POST.get('article_img')
            # print(member_id,title,description,content,times)
            # print(request.POST)
            if title and description and content:
                soup = BeautifulSoup(content, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法
                article_addtime = BeautifulSoup(times, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法
                for tag in soup.find_all():
                    if tag.name == 'script':
                        tag.decompose()  # 过滤调script标签
                        # print(tag)
                # 构建摘要数据，获取标签字符串的文本前150个符号
                # print(type(title))
                # print(type(content))
                # print(type(str(soup)))
                # print(type(desc))
                # print(desc)
                obj = Article.objects.filter(article_id=res).update(article_title=title,article_description=description,article_content=content,article_addtime=times,article_img=article_img)
                print(obj)

    #             res['status'] = 1
    #             res['info'] = '发表成功'
    #             print(res)
    #             # return redirect('/blog/index/',{'target':'_blank'})
                return redirect('/blog/person_core/')
    #         else:
    #             res['status'] = 0
    #             res['info'] = '发布失败'
    #     else:
    #         res['status'] = 0
    #         res['info'] = '请先登录'
    #         # return HttpResponse(json.dumps(res))
    return render(request,'login/add.html',locals())
    # 文章修改结束

    # 个人中心 开始
def personal(request):
    member_id = request.session.get('member_id')
    # print(member_id)
    article_obj01=Article.objects.filter(membered_id=member_id).all().order_by('-article_addtime')[:6]
    article_obj=Article.objects.filter(membered_id=member_id).all().order_by('-article_addtime')[:3]
    # print(article_obj)
    member_obj = Member.objects.filter(member_id=member_id).first()
    res = {'status':None,'info':None}
    if request.method =="POST":
        print(request.POST)
        member_tel = request.POST.get('tel')
        member_email = request.POST.get('email')
        member_nickname = request.POST.get('nickname')
        print(member_tel,member_email,member_nickname)
        if member_nickname and member_tel and member_email:
            member_obj = Member.objects.filter(member_id=member_id).update(member_tel=member_tel,member_email=member_email,member_nickname=member_nickname)
            if member_obj:
                res['status'] = 1
                res['info'] = '修改成功'
            else:
                res['status'] = 0
                res['info'] = '修改失败'
            return HttpResponse(json.dumps(res))
    return render(request,'login/personal .html',locals())
    # 个人中心 结束


# 排行列表页
def click_list(request):
    # 判断sesion是否存在存在显示用户名
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()

    article_obj = Article.objects.order_by('-article_clicknum',"-article_praise_num")
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()
    return render(request,'diary/click_list.html',locals())


def recommend_list(request):
    # 判断sesion是否存在存在显示用户名
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()

    article_obj = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime')
    article_obj02 = Article.objects.order_by('-article_clicknum','-article_addtime')[:4]
    article_obj01 = Article.objects.filter(article_is_recommend=1).order_by('-article_addtime').first()
    return render(request,'diary/recommend_list.html',locals())

# 文章添加功能 开始 dt
def publish(request):
    # 用户名是否存在
    username = request.session.get('member_id')
    if username:
        member_obj = Member.objects.filter(member_id=username).first()
    return render(request,'login/publish.html',locals())

# 添加文章
def add(request):
    # 添加内容  获取用户session值判断用户是否登录
    member_id = request.session.get('member_id')
    # 定义一个空的字典
    res = {'status':None,'info':None}
    # 判断提交方式
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('article_description')
        content = request.POST.get('content')
        times = request.POST.get('time')
        member_id = request.session.get('member_id')
        article_img = request.POST.get('article_img')
        print(times,article_img)
        # print(request.POST)
        # 判断是否登录(是否有session存在)
        if member_id:
            if title and description and content:
                soup = BeautifulSoup(content, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法
                article_addtime = BeautifulSoup(times, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法

                for tag in soup.find_all():

                    if tag.name == 'script':
                        tag.decompose()  # 过滤调script标签
                        print(tag)
                # 构建摘要数据，获取标签字符串的文本前150个符号
                # print(type(title))
                # print(type(content))
                # print(type(str(soup)))
                # print(type(desc))
                # print(desc)
                #
                obj = Article.objects.create(article_title=title, article_description=description, article_content=str(soup),article_addtime=times,article_img = article_img, membered_id=member_id)
                # print(obj)
                res['status'] = 1
                res['info'] = '发表成功'
                print(res)
                # return redirect('/blog/index/',{'target':'_blank'})
                return redirect('/blog/person_core/')
            else:
                res['status'] = 0
                res['info'] = '发布失败'
        else:
            res['status'] = 0
            res['info'] = '请先登录'
            # return HttpResponse(json.dumps(res))

    return render(request,'login/add.html',locals())
# 文章添加功能 结束 dt
