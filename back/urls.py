
from django.urls import path,re_path
from blog.views import regist
from back.views import index,article,statistics,role,menu,permission

urlpatterns = [
    re_path(r'^index/index/',index.index,name='index/index/'),
    re_path(r'^index/top/',index.top,name='index/top/'),
    re_path(r'^index/left/',index.left,name='index/left/'),
    re_path(r'^index/main/',index.main,name='index/main/'),
    re_path(r'^index/footer/',index.footer,name='index/footer/'),
    re_path(r'^article/add/',article.add,name='article/add/'),

    re_path(r'^article/upload/', article.upload, name='article/upload/'),
    # 多图片上传路由
    re_path(r'^article/upload2/', article.upload2, name='article/upload2/'),
    # 图片删除路由
    re_path('article/delImg/', article.delImg, name='article/delImg/'),
    # 三级联动路由
    re_path('article/sanjiliandong/',article.sanjiliandong, name = 'article/sanjiliandong/'),

    # ajax分页与where条件拼接路由 文章管理url
    re_path(r'^article/list/',article.list,name='article/list/'),
    re_path(r"^article/list_part/",article.list_part,name='article/list_part/'),
    re_path(r'^article/list_delete/',article.list_delete,name='article/list_delete/'),
    re_path(r'^article/list_check(\d+)/$',article.list_check,name='article/list_check/'),
    re_path(r'^article/list_update(\d+)/$',article.list_update,name='article/list_update/'),
    re_path(r'^article/list_alldel/$',article.list_alldel,name='article/list_alldel/'),

    # 图形验证码url
    re_path(r'^index/login/', index.login, name='index/login/'),
    re_path(r'^login/$', index.login, name='index/login/'),
    re_path(r'^index/$', index.login, name='index/login/'),
    re_path(r'^$', index.login, name='index/login/'),
    # 注销url
    re_path(r'^index/logout_auth/', index.logout_auth, name='index/logout_auth/'),

    re_path(r'^index/get_valid_code_img/', index.get_valid_code_img, name='index/get_valid_code_img/'),


    # 用户管理url
    re_path(r'^article/user_list/', article.user_list,
            name='article/user_list/'),
    re_path(r'^article/user_list_part/', article.user_list_part,
            name='article/user_list_part/'),
    # 删除操作url
    re_path(r'^article/user_list_delete/',article.user_list_delete,name='article/user_list_delete/'),
    # 查看操作url
    re_path(r'^article/user_list_check(\d+)/$', article.user_list_check, name='article/user_list_check/'),


    # 用户评论管理url
    re_path(r'^article/comment_list/', article.comment_list,
            name='article/comment_list/'),
    re_path(r'^article/comment_list_part/', article.comment_list_part,
            name='article/comment_list_part/'),
    # 删除操作
    re_path(r'^article/comment_list_delete/', article.comment_list_delete, name='article/comment_list_delete/'),
    re_path(r'^article/comment_list_check(\d+)/$', article.comment_list_check, name='article/comment_list_check/'),


    # 图表分析url
    re_path(r'^statistics/click/',statistics.click,name='statistics/click/'),

    # 留言管理url
    re_path(r'^article/word_list/', article.word_list,
            name='article/word_list/'),
    re_path(r'^article/word_list_part/', article.word_list_part,
            name='article/word_list_part/'),
    # 留言删除操作
    re_path(r'^article/word_list_delete/', article.word_list_delete, name='article/word_list_delete/'),
    re_path(r'^article/word_list_check(\d+)/$', article.word_list_check, name='article/word_list_check/'),


# 权限管理url
#     显示角色的url
    re_path(r'^role/list/$',role.role_list,name='role_list'),
    # 添加角色url
    re_path(r'^role/add/$',role.role_add,name='role_add'),
    # 删除角色url
    re_path(r'^role/delete/$',role.role_delete,name='role_delete'),



    # 对一级菜单操作的url 开始
    # 显示菜单
    re_path(r'^menu/list/$',menu.menu_list,name='menu_list'),
    # 增加菜单
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    # 修改菜单
    re_path(r'^menu/edit/(?P<mid>\d+)/$', menu.menu_edit, name='menu_edit'),
    # 删除菜单
    re_path(r'^menu/delete/$', menu.menu_delete, name='menu_delete'),
    # 对一级菜单操作的url 结束
    # 对二级菜单操作url 开始
    re_path(r'^menu/menu_add_second(?P<mid>\d+)/$', menu.menu_add_second, name='menu_add_second'),
    re_path(r'^menu/menu_edit_second(?P<mid>\d+)/(?P<sid>\d+)/$', menu.menu_edit_second, name='menu_edit_second'),
    # 对二级菜单操作url 结束
    # 权限的操作 url 开始
    # 权限分配
    re_path(r'^role/permission/(?P<rid>\d+)/$',role.permission,name='permission'),
    # 修改(分配的)权限
    re_path(r'^role/do_permission/$',role.do_permission,name='do_permission'),
    # 权限列表
    re_path(r'^permission/list/$',permission.permission_list,name='permission_list'),
    # 权限添加
    re_path(r'^permission/add/$', permission.permission_add, name='permission_add'),
    # 权限修改
    re_path(r'^permission/edit/(?P<mid>\d+)/$', permission.permission_edit, name='permission_edit'),
    # 权限删除
    re_path(r'^permission/delete/$', permission.permission_delete, name='permission_delete'),
    # 对二级权限(菜单)的添加
    re_path(r'^permission/permission_add_second/(?P<mid>\d+)/$', permission.permission_add_second, name='permission_add_second'),
    # 对二级权限(菜单)的修改
    re_path(r'^permission/permission_edit_second/(?P<mid>\d+)/(?P<sid>\d+)/$', permission.permission_edit_second,
            name='permission_edit_second'),
    # 权限的操作 url 结束

    # 管理员操作 开始
    re_path(r'^admin/list/$',role.admin_list,name='admin_list'),
    # 管理员url
    re_path(r'^article/conservator_list/',article.conservator_list,name='article/conservator_list/'),
    re_path(r'^article/conservator_list_part/',article.conservator_list_part,name='article/conservator_list_part/'),
    re_path(r'^article/conservator_list_delete/',article.conservator_list_delete,name='article/conservator_list_delete/'),
    re_path(r'^article/conservator_add/', article.conservator_add,
            name='article/conservator_add/'),
    re_path(r'^article/conservator_update(\d+)/$', article.conservator_update,
            name='article/conservator_update/'),
re_path(r'^article/conservator_check(\d+)/$', article.conservator_check,
            name='article/conservator_check/'),
    # 管理员操作 结束

    # 无权访问
    re_path(r'^index/no_power/', index.no_power, name='index/no_power/'),

    re_path(r'^index/left2/', index.left2, name='index/left2/'),
    re_path(r'^permission/permission_tree/', permission.permission_tree, name='permission/permission_tree/'),

]
