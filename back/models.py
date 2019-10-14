from django.db import models

# Create your models here.
# 权限管理开始
# 第一个表，管理员表
class Conservator(models.Model):
    """管理员表"""
    conservator_id = models.AutoField(primary_key=True) #用户id可不写默认。逐主键id自增
    conservator_name = models.CharField(verbose_name='用户名',max_length=60)
    conservator_tel = models.CharField(verbose_name= "联系方式",max_length=11,default='',null=True,blank=True)
    conservator_email = models.EmailField(verbose_name="邮箱",max_length=100,default='',null=True,blank=True)
    conservator_province = models.CharField(verbose_name='省份',max_length=30,default='',null=True,blank=True)
    conservator_city = models.CharField(verbose_name='市',max_length=30,default='',null=True,blank=True)
    conservator_area = models.CharField(verbose_name='区',max_length=30,default='',null=True,blank=True)
    conservator_addtime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True,null=True,blank=True)
    conservator_pwd = models.CharField(verbose_name='密码',max_length=100)
    # null:针对数据库，如果null=True，表示数据库中该字段可以为空
    # blank：针对表单，如果blank=True，表示表单中该字段可以不填，对数据库无影响。
    def __str__(self):
        return self.conservator_name

#第二个表，菜单表
class Menu(models.Model):
    '''菜单表'''
    menu_name = models.CharField(verbose_name='菜单名称',max_length=60,null=True)
    menu_path = models.CharField(verbose_name='菜单路径',max_length=60,null=True,blank=True)
    pid = models.ForeignKey(verbose_name='关联的权限',to='Menu',null=True,blank=True,related_name='parents',help_text='父id',on_delete=models.CASCADE) #多级菜单pid
    # null:针对数据库，如果null=True，表示数据库中该字段可以为空
    # blank：针对表单，如果blank=True，表示表单中该字段可以不填，对数据库无影响。
    def __str__(self):
        return self.menu_name

# 第三个表，权限表
class Permission(models.Model):
    '''权限表'''
    permission_name = models.CharField(verbose_name='权限名',max_length=60,null=True)
    permission_rule = models.CharField(verbose_name='规则',max_length=100,null=True,blank=True)
    pid = models.ForeignKey(verbose_name='关联的权限',to='Permission',null=True,blank=True,related_name='parents',help_text='父id',on_delete=models.CASCADE)
    # 一对多的关系 与菜单表
    menu = models.ForeignKey(verbose_name='所属的菜单',to='Menu',null=True,blank=True,help_text='null表示不是菜单(为空的),非null表示的是二级的菜单',on_delete=models.CASCADE)
    # related_name = 'parents' 关系  help_text = '父id' 关系的字段是父id
    # null:针对数据库，如果null=True，表示数据库中该字段可以为空
    # blank：针对表单，如果blank=True，表示表单中该字段可以不填，对数据库无影响。
    def __str__(self):
        return self.permission_name

# 第四个表，角色表
class Role(models.Model):
    '''角色表(为管理员分配角色，不同的管理员有不同的身份)'''
    role_name = models.CharField(verbose_name='角色名',max_length=60,)
    role_access = models.CharField(verbose_name='可以访问的权限',max_length=60,null=True,blank=True,help_text='不同的角色有不同的权限')
    # 多对多关系 角色和管理员
    conservator = models.ManyToManyField(to='Conservator',)
    def __str__(self):
        return self.role_name
