from django.shortcuts import render,HttpResponse
from blog.models import Article
# 导入Django字典模块
from collections import OrderedDict
import json
def regist(request):
    return render(request, 'login/regist1.html', locals())

# 文章列表接口
def article_list(request):
    # 获取所有的文章内容
    article_all = Article.objects.all()
    # 定义一个Django的空字典
    result = OrderedDict()
    # 遍历所有的文章对象
    for v in article_all:
        # 以文章对象的文章id为字典的索引值
        result[v.article_id] = {
            'article_id':v.article_id,
            'article_title':v.article_title,
            'article_description':v.article_description,
            'article_addtime':v.article_addtime.strftime('%Y-%m-%d %H:%M:%S'),
            'article_content':v.article_content,
            'article_praise_num':v.article_praise_num,
            'article_is_recommend':v.article_is_recommend,
            'article_clicknum':v.article_clicknum,
            'membered_id':v.membered_id,
        }
    return HttpResponse(json.dumps(result))

def article_lists(request):

    return render(request,'training/article_list.html',locals())

def article_delete(request):
    article_id = request.GET.get('article_id')
    res = {'status':None,'info':None}
    if article_id:
        article_del = Article.objects.filter(article_id=article_id).delete()
        if article_del:
            res['status'] = 1
            res['info'] = '删除成功！'
        else:
            res['status'] = 0
            res['info'] = '删除失败！'
    return HttpResponse(json.dumps(res))

# 文章添加
def article_add(request):
    res = {'status': None, 'info': None}
    if request.method == 'GET':

        article_title = request.GET.get('article_title')
        article_description = request.GET.get('article_description')
        article_addtime = request.GET.get('article_addtime')
        article_content = request.GET.get('article_content')
        # print(article_title,article_description)
        article_id = True
        if article_id:
            res['status'] = 1
            res['info'] = '添加成功！'
        else:
            res['status'] = 0
            res['info'] = '添加失败！'
        return HttpResponse(json.dumps(res))
    return render(request,'training/article_add.html',locals())

# 文章修改
def article_update(request,id):
    res = {'status': None, 'info': None}
    article_id = request.GET.get('article_id')
    print(article_id)
    article_obj = Article.objects.filter(article_id=article_id).first()
    result = OrderedDict()
    # result[article_obj.article_id] = {
    #
    # }
    if article_obj:
        if article_id:
            res['status'] = 1
            res['info'] = '添加成功！'

        else:
            res['status'] = 0
            res['info'] = '添加失败！'
        return HttpResponse(json.dumps(res))
    return render(request,'training/article_update.html',locals())


