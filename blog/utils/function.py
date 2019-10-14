import random

# 定义一个获取随机数的函数
def range_num(num):
    # 定义一个种子，从这里面随机查出一个值，可以使一个字母
    seed = '1234567890'
    # 定义一个空列表，没次循环，拿到一个值，并添加到列表中
    random_num = []
    # choice函数：没次从seeds中拿出一个值，添加到列表中
    for i in range(num):  #num循环次数
        # 以追加的方式将循环获取到的每个数值添加到列表中去
        random_num.append(random.choice(seed))
        # 将列表中的值，变成一个四位数的字符串
    return ''.join(random_num)


# 定义一个where条件的函数
def getWhere(request):
    where = dict()
    article_title = request.POST.get('article_title','')
    article_is_recommend = request.POST.get('article_is_recommend','')
    print(article_is_recommend)
    member_id = request.POST.get('member_id','')
    print(member_id)
    if article_title:
        where['article_title__icontains'] = article_title
    if article_is_recommend:

        where['article_is_recommend'] = article_is_recommend
    if member_id:
        where['membered'] = member_id
    return where
# 管理员
def getWhere01(request):
    where = dict()
    member_name = request.POST.get('conservator_name','')
    # role_names = request.POST.get('role_names','')
    # print(role_names)
    if member_name:
        where['conservator_name__icontains'] = member_name
    # if role_names:
    #     where['role_names'] = role_names
    return where

# 用户
def getWhere02(request):
    where = dict()
    member_name = request.POST.get('member_name','')
    member_tel = request.POST.get('member_tel','')
    if member_name:
        where['member_name__icontains'] = member_name
    if member_tel:
        where['member_tel__icontains'] = member_tel
    return where

# 评论
def getWhere03(request):
    where = dict()
    member_name = request.POST.get('member_name','')
    article_title = request.POST.get('article_title','')
    if member_name:
        where['member__member_name__icontains'] = member_name
    if article_title:
        where['article__article_title__icontains'] = article_title
    return where
# 留言
def getWhere04(request):
    where = dict()
    word_name = request.POST.get('word_name','')
    if word_name:
        where['word_name__icontains'] = word_name
    return where