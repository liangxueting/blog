from django.shortcuts import render,HttpResponse
from back import models
from back.models import Menu,Permission
import  json
# 权限的操作开始
def permission_list(request):
    # 权限列表
    # print(request.POST)
    mid = request.GET.get('mid')
    # print(mid)
    # 渲染页面显示出一级菜单(权限)
    permissions_QuerySet = Permission.objects.filter(pid=None)
    if mid:
        permissions_second_QuerySet = Permission.objects.filter(pid=mid)
    else:
        permissions_second_QuerySet = {}
    return render(request,'rbac/permission_list1.html',locals())

# 添加权限 开始
def permission_add(request):
    # 渲染所有的菜单
    menu_QuerySet = Menu.objects.all()
    # 获取前台传的数据
    res = {'status': None, 'info': None}
    if request.method == "POST":
        permission_name = request.POST.get('permission_name')
        menu_id = request.POST.get('menu_id')
        permission_one = Permission.objects.filter(permission_name=permission_name).first()
        if permission_one:
            res['status'] = 0
            res['info'] = '权限(菜单)已存在！'
            return HttpResponse(json.dumps(res))
        else:
            if  permission_name:
                permission_obj = Permission.objects.create(permission_name=permission_name,menu_id=menu_id)
                if permission_obj:
                    res['status'] = 1
                    res['info'] = '操作成功'
                else:
                    res['status'] = 0
                    res['info'] = '操作失败'
                return HttpResponse(json.dumps(res))
    return render(request,'rbac/permission_add.html',locals())
# 添加权限 结束

# 修改权限 开始
def permission_edit(request,mid):
    menu_QuerySet = Menu.objects.all()
    permission_obj = Permission.objects.filter(id=mid).first()
    # print(permission_obj)
    # print(menu_QuerySet)
    res = {'status': None, 'info': None}
    if request.method == "POST":
        # print(request.POST)
        permission_name = request.POST.get('permission_name')
        menu_id = request.POST.get('menu_id')
        # 判断修改的权限名是否存在，存在则不能修改返回信息
        # permission_one = Permission.objects.filter(permission_name=permission_name).first()
        # if permission_one:
        #     res['status'] = 0
        #     res['info'] = '菜单(权限)已存在！'
        #     return HttpResponse(json.dumps(res))
        # else:
        if permission_name:
            # print(permission_name)
            permission_obj = Permission.objects.filter(id=mid).update(permission_name=permission_name, menu_id=menu_id)
            if permission_obj:
                res['status'] = 1
                res['info'] = '操作成功'
            else:
                res['status'] = 0
                res['info'] = '操作失败'
            return HttpResponse(json.dumps(res))
    return render(request,'rbac/permission_edit.html',locals())
# 修改权限 结束

# 权限删除 开始
def permission_delete(request):
    # print(request.POST)
    if request.method == "POST":
        print(request.POST)
        id = request.POST.get('id')
        permission_obj = Permission.objects.filter(id=id).delete()
        res = {'status': None, 'info': None}
        if permission_obj:
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败'
        return HttpResponse(json.dumps(res))
# 权限删除 开始

# 二级菜单(权限)的增加 开始
def permission_add_second(request,mid):
    import json
    menu_QuerySet = Menu.objects.all()
    res = {'status': None, 'info': None}
    if request.method == "POST":
        print(request.POST)
        permission_name = request.POST.get('permission_name')
        permission_rule = request.POST.get('permission_rule')
        menu_id = request.POST.get('menu_id')
        permission_one = Permission.objects.filter(permission_name=permission_name).first()
        if permission_one:
            res['status'] = 0
            res['info'] = '权限(菜单)已存在！'
            return HttpResponse(json.dumps(res))
        else:
            # 拥有外键的数据添加
            obj = Permission.objects.filter(id=mid).first()
            # print(obj)
            permission_obj = Permission.objects.create(permission_name=permission_name,permission_rule=permission_rule,menu_id=menu_id,pid=obj)
            # print(permission_obj)
            if permission_obj:
                res['status'] = 1
                res['info'] = '操作成功'
            else:
                res['status'] = 0
                res['info'] = '操作失败'
            return HttpResponse(json.dumps(res))
    return render(request,'rbac/permission_add_second.html',locals())
# 二级菜单(权限)的增加 结束

# 二级菜单(权限)的修改 开始
def permission_edit_second(request,sid,mid):
    permission_obj = Permission.objects.filter(id=sid).first()
    menu_obj = Menu.objects.all()
    # print(permission_obj)
    res = {'status': None, 'info': None}
    import json
    if request.method == "POST":
        # print(request.POST)
        permission_name = request.POST.get('permission_name')
        permission_rule = request.POST.get('permission_rule')
        menu_id = request.POST.get('menu_id')
        # 判断修改的权限名是否存在，存在则不能修改返回信息
        # permission_one = Permission.objects.filter(permission_name=permission_name).first()
        # if permission_one:
        #     res['status'] = 0
        #     res['info'] = '菜单(权限)已存在！'
        #     return HttpResponse(json.dumps(res))
        # else:
        permission_obj = Permission.objects.filter(id=sid).update(permission_name=permission_name,permission_rule=permission_rule,menu_id=menu_id)
        print(permission_obj)

        if permission_obj:
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败'
        return HttpResponse(json.dumps(res))
    return render(request,'rbac/permission_edit_second.html',locals())
# 二级菜单(权限)的修改 结束

# 权限的操作结束
def permission_tree(request):
    return  render(request,'rbac/permission_tree.html')