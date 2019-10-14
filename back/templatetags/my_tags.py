# 过滤器
from django import template
register = template.Library()
from django.shortcuts import HttpResponse
from back import models
from back.models import Conservator,Menu,Permission,Role
from collections import OrderedDict

# (1) multi_menu
@register.inclusion_tag('index/menu.html')
def multi_menu(request):

    # 判断是否登录有没有session值
    id = request.session.get('conservator_id')
    # 有的话进行管理员匹配拿出管理员信息

    user_obj = Conservator.objects.filter(conservator_id=id).first()
    # 查询出该管理员所有的角色身份
    role_obj =user_obj.role_set.all()
    # 定义角色表中的权限id=空的字符串
    access = ''
    # 遍历该管理员的所有的角色身份
    for role in role_obj:
        # print(role.role_access)
        # 以追加的方式拿出管理员的所有的角色身份的权限id写入到角色的权限的空白字符传中
        access+=role.role_access+','
        # 进行切片切去最后的一个'，'逗号
    access=access[:-1]
    # 以逗号为分隔符 分割字符串
    arr_access = access.split(',')
    # set集合去重，再list转为列表
    arr_access = list(set(arr_access))
    # python中有个模块collections(英文，收集、集合)，里面自带了一个子类
    # OrderedDict，实现了对字典对象中元素的排序。
    menu_all = OrderedDict()
    # 遍历arr_access
    # enumerate()
    # 是python的内置函数
    # enumerate在字典上是枚举、列举的意思
    # 对于一个可迭代的（iterable） / 可遍历的对象（如列表、字符串），          enumerate将其组成一个索引序列，利用它可以同时获得索引和值。 s索引值作为键名
    # print(arr_access)
    for k,v in enumerate(arr_access):

        # 将遍历的权限id与权限表中的权限id进行对比,取出对应的权限对象
        permission = Permission.objects.filter(id=v).first()
        # print(permission)
        # 如果权限中存在菜单的id值，则证明是菜单对象
        # return HttpResponse('123')
        if permission.menu_id:
            # print(permission.menu_id)
            # 将存在的菜单id传入菜单列表进行对比
            menu = Menu.objects.filter(id = permission.menu_id).first()
            # print(menu.pid_id)
            # 如果菜单中的pid值为None则为一级菜单
            if menu.pid_id==None:
                # 如果菜单id值不在 定义的OrderedDict的对象中
                if menu.id not in menu_all:
                    # print(menu_all)
                    # 将该条数据添加到该对象中
                    menu_all[menu.id] = {
                        # 添加的彩单名称
                        'menu_name':menu.menu_name,
                        # 添加的菜单的路径
                        'menu_path':menu.menu_path,
                        # 菜单的pid的id
                        'children':[]
                    }
            else:
                # 如果菜单id值存在OrderedDict对象中
                node = {'menu_name':menu.menu_name,'menu_path':menu.menu_path}
                # print(node)
                # 如果菜单表中的pid值存在OrderedDict对象中
                if menu.pid_id in menu_all:
                    menu_all[menu.pid.id]['children'].append(node)
                else:
                    menu_all[menu.pid_id] ={
                        'menu_name':menu.pid.menu_name,
                        'menu_path':menu.pid.menu_path,
                        'children':[node,]
                    }
                    # print(menu_all[menu.pid_id])
                    # print(menu.pid_id)
    current_path = request.path
    # 返回菜单和路径
    return {'menu':menu_all,'current_path':current_path}

# 自定义一个过滤器进行筛选和管理
# 如果一个元素，如新建，他不是菜单，想进行权限管理
#新建一个过滤器，因为只要过滤器才能用在if条件中，不能自定义一个标签
@register.filter
def is_have_permission(request,name):
    # 判断是否登录有没有session值
    id = request.session.get('conservator_id')
    # 有的话进行管理员匹配拿出管理员信息
    user_obj = Conservator.objects.filter(conservator_id=id).first()
    # 查询出该管理员所有的角色身份
    role_obj = user_obj.role_set.all()
    # 定义角色表中的权限id=空的字符串
    role_access = ''
    # 遍历该管理员的所有的角色身份
    for role in role_obj:
        # 以追加的方式拿出管理员的所有的角色身份的权限id写入到角色的权限的空白字符传中
        role_access += role.role_access + ','
        # 进行切片拿出最后一个
    role_access = role_access[:-1]
    # 以逗号为分隔符 分割字符串

    arr_access = role_access.split(',')
    # set集合去重，再list转为列表
    arr_access = list(set(arr_access))
    # 根据规则来判断
    print(arr_access)
    print(request)
    print(name)
    permission_obj = Permission.objects.filter(permission_rule=name).first()
    # 获取当前的新建按钮的权限id 是否在该用户的权限id列表中，在返回通过，不在拦截
    if str(permission_obj.id) in arr_access:
        return True
    else:
        return False
'''
一定要配置
配置setting.py中的TEMPLATES字段
 'libraries':{
                'my_customer_tags':'back.templatetags.my_tags'
            }
'''
