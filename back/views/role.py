from django.shortcuts import render,HttpResponse
from back import models
from back.models import Role,Conservator,Menu,Permission
from collections import OrderedDict
import json
# 权限管理 开始
# 显示左边列表 开始
# (1)角色列表
def role_list(request):
    # 获取角色列表 ，渲染页面
    role_queryset = Role.objects.all()
    # 写页面
    return render(request, 'rbac/role_list.html', {'role':role_queryset})

def role_add(request):
    # 获取指定的角色的对象
    permission_current = Role.objects.all()
    permission_all = OrderedDict()  # 有序的字典对象
    # 判断pid isnull时，则为一级菜单
    permission = Permission.objects.filter(pid__isnull=True).all()
    # print(permission) 遍历所有的一级菜单
    for v in permission:
        # 遍历出一级菜单下面的二级菜单
        permission2 = Permission.objects.filter(pid=v.id).all()
        # print(permission2)
        permission_all[v.id] = {
            'id': v.id,
            'permission_name': v.permission_name,
            'permission_rule': v.permission_rule,
            'children': permission2,
        }
    # print(permission_all)
    # 获取指定的角色的对象
    res = {'status': None, 'info': None}
    if request.method == "POST":
        role_name = request.POST.get('role_name')
        role_access = request.POST.getlist('role_access[]',[])
        role_one = Role.objects.filter(role_name=role_name).first()
        if role_one :
            res['status'] = 0
            res['info'] = '角色名已存在！'
            return HttpResponse(json.dumps(res))
        else:
            str_role = ','.join(role_access)
            if role_name:
                role_obj = Role.objects.create(role_name=role_name,role_access=str_role)
                # join方式将列表拼接成字符串
                if role_obj:
                    res['status'] = 1
                    res['info'] = '操作成功!'
                else:
                    res['status'] = 0
                    res['info'] = '操作失败！'
            return HttpResponse(json.dumps(res))
    return render(request,'rbac/role_add.html',locals())
# 删除角色
def role_delete(request):
    res = {'status': None, 'info': None}
    if request.method == "POST":
        print(request.POST)
        id = request.POST.get('id')
        role_name = request.POST.get('role_name')
        if role_name == 'admin':
            res['status'] = 0
            res['info'] = 'admin  角色不能删除！'
            return HttpResponse(json.dumps(res))
        else:
            # print(123)
            role_obj = Role.objects.filter(id=id).delete()
            if role_obj:
                res['status'] = 1
                res['info'] = '操作成功!'
            else:
                res['status'] = 0
                res['info'] = '操作失败！'
    return HttpResponse(json.dumps(res))

# (2)当前用户拥有的权限 开始
def permission(request,rid):
    # print(rid)
    # 获取指定的角色的对象
    permission_current = Role.objects.filter(id=rid).first()
    # print(permission_current)
    # 如 admin
    # 权限的id ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    # 获取该角色的所有的权限的id
    permission_current = permission_current.role_access.split(',')
    # print(permission_current)
    permission_all = OrderedDict()  #有序的字典对象
    # 判断pid isnull时，则为一级菜单
    permission = Permission.objects.filter(pid__isnull=True).all()
    # print(permission) 遍历所有的一级菜单
    for v in permission:
        # 遍历出一级菜单下面的二级菜单
        permission2 = Permission.objects.filter(pid=v.id).all()
        # print(permission2)
        permission_all[v.id] = {
            'id':v.id,
            'permission_name':v.permission_name,
            'permission_rule':v.permission_rule,
            'children':permission2,
        }
    # # print(permission_all)
    # power_list_all = [{"id": '0', "pId": '0', "children": [], "name": '所有权限',},]
    # # power_list2_id = []
    # # power_list_name = []
    # # power_list2_name = []
    # for k, v in permission_all.items():
    #     power_id = v['id']
    #     name = v['permission_name']
    #     rule = v['permission_rule']
    #     power_list_1 = {"id": power_id, "pId": '0', "children": [], "name": name,}
    #     power_list_all.append(power_list_1)
    #     # print(power_list_all)
    #     for v2 in v['children']:
    #         power_v2_id= v2.id
    #         power_v2_name = v2.permission_name
    #         power_v2_rule = v2.permission_rule
    #         power_v2_pid = v2.pid_id
    #         power_list_2 = {"id": power_v2_id, "pId": power_v2_pid, "children": [],"name": power_v2_name,}
    #         power_list_all.append(power_list_2)
            # print(power_list2_id)
    return render(request,'rbac/permission_tree1.html',locals())
# (2)当前用户拥有的权限 结束

# (3)修改(分配的)权限 开始
# 将需要修改的权限传到该方法中
def do_permission(request):
    if request.method == "POST":
        # 获取角色id值
        print(request.POST)
        rid = request.POST.get('rid')
        # 获取该角色的权限id
        permission = request.POST.getlist('permission[]',[]) #没有让它默认为空
        # join方式将列表拼接成字符串
        str_permission = ','.join(permission)
        # 将拼接好的字符串以修改的方式添加到角色表中的权限字段中
        permission_obj = Role.objects.filter(id=rid).update(role_access=str_permission)
        # 定义一个空白的字典
        res = {'status':None,'info':None}
        if permission_obj:
            res['status'] = 1
            res['info'] = '操作成功!'
        else:
            res['status'] = 0
            res['info'] = '操作失败！'
        return HttpResponse(json.dumps(res))
# (3)修改(分配的)权限 结束

# (4)显示管理员列表开始
def admin_list(request):
    return render(request,'article/conservator_list.html',locals())

# (4)显示管理员列表结束

# 显示左边列表 结束

# 权限管理 结束