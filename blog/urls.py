from django.contrib import admin
from django.urls import path,re_path
from blog.views import regist,index,enroll,newtext,login,diary,add_news

urlpatterns = [
    path('admin/', admin.site.urls),
    # 主页url
    re_path(r'^index/', index.index, name='index'),
    # 通过127.0.0.1:8000直接访问主页 的项目url设置
    re_path(r'^$', index.index, name='index'),
    # 登录url
    re_path(r'^newtext/', newtext.newtext, name='newtext'),
    # 注册url
    re_path(r'^enroll/', enroll.enroll, name='enroll'),
    # 注销url
    re_path(r'^logout_auth/',newtext.logout_auth,name='logout_auth'),
    # 练习url
    re_path(r'^regist/', regist.regist, name='regist'),

    # 博客日记的url
    re_path(r'^diary/', diary.diary, name='diary'),

    # 博客日记详情页url
    re_path(r'^text(\d+)/$', diary.text, name='text'),

    # 定义一个图形验证码的url
    re_path(r'^login/', login.login, name='login'),

    re_path(r'^get_valid_code_img/', login.get_valid_code_img, name='get_valid_code_img'),

    # 电话号码验证码url
    re_path(r'^loginTel/',login.loginTel,name='loginTel'),

    # 综合登录验证
    re_path(r'^login_all/',login.login_all,name='login_all'),
    re_path(r'^add_news/',add_news.add_news,name='add_news'),


    # 个人列表页
    re_path(r'^person_list(\d+)/$',diary.person_list,name='person_list'),
    # 个人中心url
    re_path(r'^personal/', diary.personal, name='personal'),
    # 个人中心列表url
    re_path(r'^person_core/$',diary.person_core,name='person_core'),
    # 个人文章删除url
    re_path(r'^person_del/$',diary.person_del,name='person_del'),
    # 个人文章修改url
    re_path(r'^person_update(\d+)/$', diary.person_update, name='person_update'),
    # 点击排行列表
    re_path(r'^click_list/$',diary.click_list,name='click_list'),
    # 推荐列表
    re_path(r'^recommend_list/$',diary.recommend_list,name='recommend_list'),


    # 关于页面的url
    re_path(r'^about/$',index.about,name='about'),
    re_path(r'^gbook/$',index.gbook,name='gbook'),

    # 模糊查询
    re_path(r"^like_list/$",index.like_list,name='like_list'),

    # 文章发布url
    re_path(r'^publish/$',diary.publish,name='publish'),
    re_path(r'^add/', diary.add, name='add'),

    # 找回密码url
    re_path(r'^get_pwd/',index.get_pwd,name='get_pwd'),



    # 接口练习
    # 文章列表接口url
    re_path(r'^article_list/', regist.article_list, name='article_list'),
    re_path(r'^article_lists/', regist.article_lists, name='article_lists'),
    # 文章删除接口url
    re_path(r'^article_delete/', regist.article_delete, name='article_delete'),
    # 文章添加接口 url
    re_path(r'^article_add/', regist.article_add, name='article_add'),
    # 文章修改接口 url
    re_path(r'^article_update(\d+)/$', regist.article_update, name='article_update'),
]
