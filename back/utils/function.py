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

# 定义一个获取七天时间的方法
def recent_seven_days():
    # 导入时间模块
    import datetime
    # 获取当前时间
    d = datetime.datetime.now()
    # 定义一个空列表
    list1 = []
    # 循环天数
    for i in range(1, 8):
        oneday = datetime.timedelta(days=i)
        day = d - oneday
        date_to = datetime.datetime(day.year, day.month, day.day)
        list1.append(str(date_to)[0:10])
    return list1

