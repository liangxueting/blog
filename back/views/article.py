from django.shortcuts import render, HttpResponse, redirect
# 导入数据库
from blog.models import Article, Member, Comment, Word
# 导入json模块
import json
# 导入用户上传文件的配置的文件路径
from my_pro20 import settings
# 导入bs4模块
from bs4 import BeautifulSoup

from blog.utils import function
# 导入 分页器模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 导入作者模块
from back.models import Conservator
from django.db.models import Count, Q
from back.models import Role
from collections import OrderedDict
from datetime import datetime

# 文章管理 开始
def add(request):  # 添加内容
    # 添加作者信息
    member_obj = Member.objects.all()

    res = {'status': None, 'info': None}
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        description = request.POST.get('article_description')
        content = request.POST.get('content')
        times = request.POST.get('time')
        article_img = request.POST.get('article_img')
        member_id = request.POST.get('member_id')
        article_is_recommend = request.POST.get('article_is_recommend')
        if title:
            if description:
                if content:
                    # 防止xss攻击，过滤script标签
                    soup = BeautifulSoup(content, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法
                    article_addtime = BeautifulSoup(times,
                                                    'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法

                    for tag in soup.find_all():

                        if tag.name == 'script':
                            tag.decompose()  # 过滤调script标签
                            print(tag)
                    obj = Article.objects.create(article_title=title, article_description=description,
                                                 article_content=str(soup), article_addtime=article_addtime,
                                                 article_img=article_img, membered_id=member_id,
                                                 article_is_recommend=article_is_recommend)
                    if obj:
                        # print(obj)
                        res['status'] = 1
                        res['info'] = '发表成功'
                    else:
                        res['status'] = 0
                        res['info'] = '发布失败'
    return render(request, 'article/add.html', locals())


def list(request):
    member_list = Member.objects.all()
    return render(request, 'article/list.html', locals())


def list_part(request):
    # 查询总记录数
    Sum = Article.objects.aggregate(Count('article_id'))
    # print(jilu)
    where = function.getWhere(request)
    articles_list = Article.objects.filter(**where).all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(articles_list, 2)
    # print(paginator)
    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        articles_list = paginator.page(currentPage)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)
    return render(request, 'article/list_part.html', locals())


# 判断删除数据开始
def list_delete(request):
    id = request.POST.get('id')
    # print(id)
    result = Article.objects.filter(article_id=id).delete()
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))


# 判断删除数据结束
# 文章查看
def list_check(request, res):
    article_check = Article.objects.filter(article_id=res).first()
    return render(request, 'article/conservator_check.html', locals())


# 文章修改操作
def list_update(request, par):
    article_update = Article.objects.filter(article_id=par).first()
    article_update_num = 1
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        description = request.POST.get('article_description')
        content = request.POST.get('content')
        times = request.POST.get('time')
        article_img = request.POST.get('article_img')
        member_id = request.POST.get('member_id')
        article_is_recommend = request.POST.get('article_is_recommend')
        # print(title,description,content,times,article_img,member_id,article_is_recommend)
        if title and description and content:
            # 防止xss攻击，过滤script标签
            soup = BeautifulSoup(content, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法
            article_addtime = BeautifulSoup(times, 'html.parser')  # 通过字符串创建BeautifulSoup对象，即将字符串转化成对象，然后调用对象的相关方法

            for tag in soup.find_all():

                if tag.name == 'script':
                    tag.decompose()  # 过滤调script标签
                    print(tag)
            obj = Article.objects.filter(article_id=par).update(article_title=title, article_description=description,
                                                                article_content=content, article_addtime=times,
                                                                article_img=article_img, membered_id=member_id,
                                                                article_is_recommend=article_is_recommend)
            if obj:
                # print(obj)
                res['status'] = 1
                res['info'] = '发表成功'
                return redirect('back:article/list/')
            else:
                return HttpResponse('修改失败')
    return render(request, 'article/add.html', locals())


# 文章批量删除
def list_alldel(request):
    res = {'status': None, 'info': None}
    alldel = request.GET.getlist('chedel[]')
    print(alldel)
    if alldel:
        for i in alldel:
            article_del = Article.objects.filter(article_id=i).delete()
            # print(article_del)
            if article_del:
                res['status'] = 1
                res['info'] = '批量删除成功！'
            else:
                res['status'] = 0
                res['info'] = '操作失败！'
                # print(i)
        # print(request.GET)
        return HttpResponse(json.dumps(res))
    else:
        res['status'] = 0
        res['info'] = '操作失败！'
    return HttpResponse(json.dumps(res))


# 文章管理结束


import os

def upload(request):
    # 编辑器上传文件接受视图的函数
    img_obj = request.FILES.get('upload_img')

    path = os.path.join(settings.MEDIA_ROOT, 'add_article_img', img_obj.name)
    with open(path, 'wb') as f:
        for line in img_obj:
            f.write(line)
    response = {
        'error': 0,
        'url': '/media/add_article_img/%s' % img_obj.name
    }
    return HttpResponse(json.dumps(response))


def upload2(request):
    img_obj = request.FILES.get("file")  # 通过前台提交过来的图片资源   img_obj.name  avatar.jpg
    print(img_obj)
    range_num = function.range_num(15)  # 生成一个15位随机数

    # print(img_obj.name)
    img_type = os.path.splitext(img_obj.name)[1]  # .jpg  获取文件名后缀
    new_img_path = os.path.join(settings.MEDIA_ROOT, "add_article_img",
                                range_num + img_type)  # E:\ftp\code\www\pro\media\add_article_img\676161546271228.jpg        #/media/add_article_img/123456.jpg
    print(new_img_path)
    img_type2 = img_type.replace(".", "")  # png

    # print(new_img_path)
    with open(new_img_path, "wb") as f:
        for line in img_obj:
            f.write(line)
    response = {
        "status": 1,
        "message": "上传成功",
        'file': "/media/add_article_img/" + range_num + img_type,
        'file_type': img_type2
    }

    return HttpResponse(json.dumps(response))


def delImg(request):
    img_path = request.POST.get('path')  # /media/add_article_img/722264423391172.jpg
    img_name = os.path.split(img_path)[1]  # 获取图片名称 722264423391172.jpg
    img_new_path = os.path.join(settings.MEDIA_ROOT, "add_article_img",
                                img_name)  # E:\ftp\code\www\pro\media\add_article_img\722264423391172.jpg
    if not os.remove(img_new_path):
        response = {
            "status": 1,
            "message": "删除成功"
        }
        return HttpResponse(json.dumps(response))


def sanjiliandong(request):
    return render(request, 'article/add1.html', locals())


# 管理员管理方法
def conservator_list(request):
    # member_list = Member.objects.all()
    return render(request, 'article/conservator_list.html', locals())


def conservator_list_part(request):
    # 管理员列表
    # # 查询总记录数
    Sum = Conservator.objects.aggregate(Count('conservator_id'))
    # print(Sum)
    conservator_list = OrderedDict()
    # member_name = request.POST.get("member_name")
    # member_tel = request.POST.get("member_tel")
    where = function.getWhere01(request)
    conservator = Conservator.objects.filter(**where).all()
    for v in conservator:
        role_obj = v.role_set.filter(conservator=v.conservator_id).all()
        # print(role_obj)
        role_names = []
        for v2 in role_obj:
            role_names.append(v2.role_name)
        role_names_str = ','.join(role_names)
        conservator_list[v.conservator_id] = {
            'conservator_id': v.conservator_id,
            'conservator_name': v.conservator_name,
            'role_names': role_names_str,
        }
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(conservator_list, 2)
    # print(paginator.page(str(currentPage)))
    # print(paginator.page)
    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)
    # print(paginator.page(currentPage))
    # try:
    #     conservator_list = paginator.page(currentPage)
    #     print(paginator.page(currentPage))
    # except PageNotAnInteger:
    #     conservator_list = paginator.page(1)
    # except EmptyPage:
    #     conservator_list = paginator.page(paginator.num_pages)

    return render(request, 'article/conservator_list_part.html', locals())


# 判断删除数据开始
def conservator_list_delete(request):
    id = request.POST.get('id')
    conservator_id = request.session['conservator_id']
    conservator_name = request.session['conservator_name']
    print(type(conservator_id),type(conservator_name))
    res = {'status': None, 'info': None}
    if conservator_id == 1:
        res['status'] = 0
        res['info'] = '操作失败,超级管理员不可删除！'
        return HttpResponse(json.dumps(res))
    else:
        print(123)
        # result = Conservator.objects.filter(conservator_id=id).first()
        # result.role_set.clear()  # 多对多解除关系
        # result1 = result.delete()
        # if result1:
        #     res['status'] = 1
        #     res['info'] = '操作成功'
        # else:
        #     res['status'] = 0
        #     res['info'] = '操作失败'
        # return HttpResponse(json.dumps(res))

# 判断删除数据结束

# 添加管理员
def conservator_add(request):
    role_obj = Role.objects.all()
    res = {'status': None, 'info': None}
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        tel = request.POST.get('tel','')
        email = request.POST.get('email','')
        province = request.POST.get('province','')
        city = request.POST.get('city','')
        area = request.POST.get('area','')
        time = request.POST.get('time','')
        role = request.POST.getlist('role[]', [])
        conservator_one = Conservator.objects.filter(conservator_name=username).first()
        if conservator_one:
            res['status'] = 0
            res['info'] = '管理员已存在！'
            return HttpResponse(json.dumps(res))
        else:
            conservator_obj = Conservator.objects.create(conservator_name=username, conservator_tel=tel,
                                                         conservator_email=email, conservator_province=province,
                                                         conservator_city=city, conservator_area=area,
                                                         conservator_addtime=time, conservator_pwd=pwd)
            role_list_obj = Role.objects.filter(id__in=role)
            result = conservator_obj.role_set.add(*role_list_obj)
            # print(result)
            # print(role_list_obj)
            if not result:
                res['status'] = 1
                res['info'] = '添加成功!'
            else:
                res['status'] = 0
                res['info'] = '添加失败!'
            return HttpResponse(json.dumps(res))
    return render(request, 'article/conservator_add.html', locals())


# 管理员修改
def conservator_update(request, res):

    role_obj = Role.objects.all()
    conservator_one = Conservator.objects.filter(conservator_id=res).first()
    role_obj_now = conservator_one.role_set.filter(conservator=res).all()

    resa = {'status': None, 'info': None}
    if request.method == 'POST':
        print(request.POST)
        conservator_id = request.session.get('conservator_id')
        username = request.POST.get('username')
        pwd = request.POST.get('pwd','')
        tel = request.POST.get('tel','')
        email = request.POST.get('email','')
        province = request.POST.get('province','')
        city = request.POST.get('city','')
        area = request.POST.get('area','')
        role = request.POST.getlist('role[]', [])
        time = request.POST.get('time','')
        print(type(time))
        if time == '':
            time =  datetime.today()
        else:
            time = time
        if province == '0':
            province = ''
        else:
            province = province
        # conservator_one_1 = Conservator.objects.filter(conservator_name=username).first()
        # if conservator_one_1:
        #     resa['status'] = 0
        #     resa['info'] = '管理员已存在！'
        #     return HttpResponse(json.dumps(resa))
        # else:
        Conservator.objects.filter(conservator_id=res).update(conservator_name=username, conservator_tel=tel,
                                                              conservator_email=email, conservator_province=province,
                                                              conservator_city=city, conservator_area=area,
                                                              conservator_addtime=time, conservator_pwd=pwd)
        conservator_obj = Conservator.objects.filter(conservator_id=res).first()
        conservator_obj.role_set.clear()

        role_list_obj = Role.objects.filter(id__in=role)
        result = conservator_obj.role_set.add(*role_list_obj)
        if not result:
            resa['status'] = 1
            resa['info'] = '修改成功！'
        else:
            resa['status'] = 0
            resa['info'] = '操作失败！'
        return HttpResponse(json.dumps(resa))
    return render(request, 'article/conservator_update.html', locals())

# 管理员信息查看
def conservator_check(request, res):
    conservator_obj = Conservator.objects.filter(conservator_id=res).first()
    return render(request, 'article/conservator_check.html', locals())


# 用户管理
def user_list(request):
    return render(request, 'article/user_list.html')


def user_list_part(request):
    # 查询总记录数
    Sum = Member.objects.aggregate(Count('member_id'))
    # print(jilu)
    where = function.getWhere02(request)
    member_list = Member.objects.filter(**where).all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(member_list, 2)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        member_list = paginator.page(currentPage)
    except PageNotAnInteger:
        member_list = paginator.page(1)
    except EmptyPage:
        member_list = paginator.page(paginator.num_pages)
    return render(request, 'article/user_list_part.html', locals())


def user_list_delete(request):
    id = request.POST.get('id')
    # print(id)
    result = Member.objects.filter(member_id=id).delete()
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))


def user_list_check(request, res):
    print(res)
    member_obj = Member.objects.filter(member_id=res).first()

    return render(request, 'article/conservator_check.html', locals())


# 评论管理
def comment_list(request):
    return render(request, 'article/comment_list.html')


def comment_list_part(request):
    # 查询总记录数
    Sum = Comment.objects.aggregate(Count('comment_id'))
    # print(jilu)
    where = function.getWhere03(request)
    comment_list = Comment.objects.filter(**where).all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(comment_list, 2)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        comment_list = paginator.page(currentPage)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)
    return render(request, 'article/comment_list_part.html', locals())


# 删除评论
def comment_list_delete(request):
    id = request.POST.get('id')
    print(id)
    result = Comment.objects.filter(comment_id=id).delete()
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))


# 评论查看
def comment_list_check(request, res):
    print(request, res)

    comment_check = Comment.objects.filter(comment_id=res).first()
    # member_id = comment_check.member.member_id
    #
    # comment_allcheck = Comment.objects.filter(member_id=member_id)
    # print(comment_allcheck)
    # article_id = comment_check.article.article_id
    # comment_all = Comment.objects.filter(article_id=article_id)
    # print(comment_all)
    return render(request, 'article/conservator_check.html', locals())


# 留言管理
def word_list(request):
    return render(request, 'article/word_list.html')


def word_list_part(request):
    # 查询总记录数
    Sum = Word.objects.aggregate(Count('word_id'))
    # print(jilu)
    where = function.getWhere04(request)
    word_list = Word.objects.filter(**where).all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(word_list, 2)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        word_list = paginator.page(currentPage)
    except PageNotAnInteger:
        word_list = paginator.page(1)
    except EmptyPage:
        word_list = paginator.page(paginator.num_pages)
    return render(request, 'article/word_list_part.html', locals())


# 删除留言
def word_list_delete(request):
    id = request.POST.get('id')
    print(id)
    result = Word.objects.filter(word_id=id).delete()
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))


def word_list_check(request, res):
    # print(res)
    word_list = Word.objects.filter(word_id=res).first()

    return render(request, 'article/conservator_check.html', locals())
