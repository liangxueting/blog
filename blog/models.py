from django.db import models
from django.contrib.auth.models import AbstractUser
# 创建一个用户表
class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100,default='')
    member_tel = models.CharField(max_length=11,default='')
    member_email = models.CharField(max_length=60,default='')
    member_nickname = models.CharField(max_length=60,default='')
    member_pwd = models.CharField(max_length=60,default='')

    # 创建一个多对多的用户id和文章id
    praise = models.ManyToManyField(to='Member' )
    Praise_list = models.ManyToManyField(
        to='Article',
    )
    def __str__(self):
        return self.member_name

# 创建一个网页介绍表
class Web(models.Model):
    web_id = models.AutoField(primary_key=True)
    web_name = models.CharField(max_length=100,default='')
    web_content = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.web_name


# 创建一个文章表
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=255,default='')
    article_description = models.CharField(max_length=255,default='')
    article_addtime = models.DateTimeField(auto_now_add=True)
    article_content = models.TextField()
    article_praise_num = models.IntegerField(default=0)
    article_is_recommend = models.IntegerField(default=0,verbose_name='0:不推荐,1：推荐')
    article_clicknum = models.IntegerField(default=0)
    article_img = models.CharField(max_length=255,default='')
#     # 创建一个一对多的用户外键
    membered = models.ForeignKey(to='Member',to_field='member_id',on_delete=models.CASCADE)

    def __str__(self):
        return self.article_title

# 创建一个评论表
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_content = models.CharField(max_length=255,default='')
    comment_addtime = models.DateTimeField(auto_now_add=True)
    # # 创建一个一对多的用户id
    member = models.ForeignKey(to=Member,to_field='member_id',on_delete = models.CASCADE)
    # 创建一对多的文章id
    article = models.ForeignKey(to=Article,to_field = 'article_id',on_delete = models.CASCADE)



    def __str__(self):
        return self.comment_content

# 创建一个留言表
class Word(models.Model):
    word_id = models.AutoField(primary_key=True,verbose_name='评论id')
    word_name = models.CharField(max_length=50,verbose_name='用户名')
    word_content = models.CharField(max_length=255,verbose_name='评论内容')
    word_addtime = models.DateField(auto_now_add=True,verbose_name='评论时间')
    word_img = models.CharField(max_length=255,verbose_name='评论头像图片')


    def __str__(self):
        return self.word_name

