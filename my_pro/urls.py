from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from my_pro20 import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # 没有路径的url
    re_path(r'^blog/',include(('blog.urls','blog'))),
    # 通过127.0.0.1:8000直接访问主页 的全局url设置
    re_path(r'^', include(('blog.urls', 'blog'))),
    re_path(r'^back/',include(('back.urls','back'))),

    # media配置文件
    re_path(r"media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT})
]
