from django.shortcuts import render,HttpResponse
from back import models
from back.models import Menu
import  json
# 菜单 操作 开始
def menu_list(request):
    # 菜单列表
    # 获取一级菜单的id值
    mid = request.GET.get('mid')
    # print(mid)
    # 渲染一级菜单的菜单列表
    menus_QuerySet = Menu.objects.filter(pid=None)
    # 当存在时差选一级菜单下的所有的二级菜单
    if mid:
        menus_second_Queryset = Menu.objects.filter(pid=mid)
    else:
        # 如果没有返回空
        menus_second_Queryset= {}
    return render(request,'rbac/menu_list1.html',{'menus':menus_QuerySet,'menus_second':menus_second_Queryset,"mid":mid})
# 添加一级菜单 开始
def menu_add(request):
    res = {'status': None, 'info': None}
    if request.method == "POST":
        menu_name = request.POST.get('menu_name')
        # print(menu_name)
        menu_one = Menu.objects.filter(menu_name=menu_name).first()
        if menu_one:
            res['status'] = 0
            res['info'] = '菜单已存在！'
            return HttpResponse(json.dumps(res))
        else:
            menu_obj = Menu.objects.create(menu_name=menu_name)
            if menu_obj:
                res['status'] = 1
                res['info'] = '操作成功！'
            else:
                res['status'] = 0
                res['info'] = '操作失败！'
            return HttpResponse(json.dumps(res))
    return render(request,'rbac/menu_add.html')
# 添加一级菜单结束

# 一级菜单修改开始
def menu_edit(request,mid):
    # 获取菜单id将菜单名称渲染到页面上
    menu_obj = Menu.objects.filter(id=mid).first()
    # print(mid)
    res = {'status': None, 'info': None}
    if request.method == "POST":
        menu_name = request.POST.get('menu_name')
        # menu_one = Menu.objects.filter(menu_name=menu_name).first()
        # if menu_one:
        #     res['status'] = 0
        #     res['info'] = '菜单名已存在！'
        #     return HttpResponse(json.dumps(res))
        # else:
        menu_obj01 = Menu.objects.filter(id=mid).update(menu_name=menu_name)
        print(mid)
        if menu_obj01:
            res['status'] = 1
            res['info'] = '操作成功！'
        else:
            res['status'] = 0
            res['info'] = '操作失败！'
        return HttpResponse(json.dumps(res))
    return render(request,'rbac/menu_edit.html',{'menu':menu_obj,'mid':mid})
# 一级菜单修改结束

# 一级菜单删除 开始
def menu_delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # print(id)
        menu_obj = Menu.objects.filter(id=id).delete()
        # print(menu_obj)
        res = {'status': None, 'info': None}
        if menu_obj:
            res['status'] = 1
            res['info'] = '操作成功！'
        else:
            res['status'] = 0
            res['info'] = '操作失败！'
        return HttpResponse(json.dumps(res))
# 一级菜单删除 结束

# 二级菜单添加 开始
def menu_add_second(request,mid):
    if request.method == "POST":
        res = {'status': None, 'info': None}
        menu_name = request.POST.get('menu_name')
        menu_path = request.POST.get('menu_path')
        menu_one = Menu.objects.filter(menu_name=menu_name).first()
        if menu_one:
            res['status'] = 0
            res['info'] = '菜单已存在！'
            return HttpResponse(json.dumps(res))
        else:
            # 拥有外键的添加 获取该一级菜单的对象。
            obj = Menu.objects.get(id=mid)
            # print(obj)
            # 以对象的方式添加到与主键建立外键的pid中  这个地方的pid指的时model中的外键字段
            menu_obj = Menu.objects.create(menu_name=menu_name,menu_path=menu_path,pid=obj)
            if menu_obj:
                res['status'] = 1
                res['info'] = '操作成功！'
            else:
                res['status'] = 0
                res['info'] = '操作失败！'
            return HttpResponse(json.dumps(res))
    return render(request,'rbac/menu_add_second.html',locals())
# 二级菜单添加 结束

# 二级菜单修改 开始
def menu_edit_second(request,mid,sid):
    # print(mid,sid)
    menu_obj = Menu.objects.filter(id=sid).first()
    # print(menu_obj)
    # print(request.POST)
    res = {'status': None, 'info': None}
    if request.method == "POST":
        menu_name = request.POST.get('menu_name')
        menu_path = request.POST.get('menu_path')
        # menu_one = Menu.objects.filter(menu_name=menu_name).first()
        # if menu_one:
        #     res['status'] = 0
        #     res['info'] = '菜单名已存在！'
        #     return HttpResponse(json.dumps(res))
        # else:
        menu_obj = Menu.objects.filter(id=sid).update(menu_name=menu_name, menu_path=menu_path)
        if menu_obj:
            res['status'] = 1
            res['info'] = '操作成功！'
        else:
            res['status'] = 0
            res['info'] = '操作失败！'
        return HttpResponse(json.dumps(res))
    return render(request,'rbac/menu_edit_second.html',locals())
# 二级菜单修改 结束
# 菜单 操作 结束