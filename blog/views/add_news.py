from django.shortcuts import render,HttpResponse,redirect
from blog.models import Article
def add_news(request):
    article_obj =Article.objects.create(article_title='网页',article_content='大嘴巴',article_description='刘菲的',member_id=2)
    print(article_obj)
    return HttpResponse("OK")