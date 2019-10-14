"""中间件功能通过中间件来减少代码的冗余"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
from my_pro20 import settings
from back.models import Role,Permission

class AuthMiddleware(MiddlewareMixin):
    # 接收函数参数
    def process_view(self, request, fun, fun_args, fun_kwargs):
        # print(request.path)
        # print(request.session)
        # print(settings.WHITE_LIST)
        # 获取白名单的列表
        # print(fun_kwargs['path'])
        # 获取图片的路径值（键值对的方式）
        for k,v in fun_kwargs.items():
            # print(v)
            # 遍历图片的路径值，遍历之后和图片路径进行字符串拼接完整的图片路径
            img_list = settings.MEDIA_URL + v
            # 判断图片是否存在当前完整的图片路径中，存在让他通过，不拦截
            if request.path in img_list:
                return None
        white_list = settings.WHITE_LIST
        # print(request.path)
        # print(white_list)
        # print('*' * 100)
        # print(white_list)
        # 判断带参数的路径的配置
        if fun_args:
            # 拼接文章的路径字符串
            text_list = white_list[4] + fun_args[0]+'/'
            white_list.append(text_list)
            # 拼接个人列表的路径字符串
            person_list = white_list[10]+fun_args[0]+'/'
            white_list.append(person_list)
        # 判断文章路径是否存在,在的话白名单通过不拦截
            if request.path in white_list:
                return None

        elif request.path in white_list:
            return None

        elif 'blog/' in request.path:
            if not request.session.get('member_id'):
                return redirect('/blog/newtext/')




        # 判断路径中是否存在back的命名空间
        elif 'back/' in request.path:
            # print(request.path)
            # 当back/在当前路径时，获取当前的session值，存在则直接访问，不存在，则返回登录界面
            if request.session.get('conservator_id'):
                conservator_id = request.session.get('conservator_id')
                role_objs = Role.objects.filter(conservator=conservator_id).all() #用户所有的角色
                # print(role_objs)
                # 例如http://127.0.0.1:8000/back/index/index/ 这个不是菜单，应该放行
                permission_obj = Permission.objects.filter(permission_rule=request.path).first()
                # print(permission_obj)
                if permission_obj:
                    permission_list = []
                    for role in role_objs:
                        permission_list.extend(role.role_access.split(','))
                    if str(permission_obj.id) not in permission_list:
                        return render(request,'rbac/no_power.html')
                    else:
                        return None
            else:
                return redirect('/back/login/')
        else:
            return  None


