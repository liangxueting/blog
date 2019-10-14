from django.shortcuts import render
from back.utils import function
from blog.models import Article
# 导入自定义的时间方法
def click(request):
    # 导入聚合函数
    from django.db.models import Sum
    recent_seven_days = function.recent_seven_days()
    list_week_day = recent_seven_days[::-1]  #倒序排列
    # 定义两个空列表用来接受点击量和点赞量
    clicknum_list = []
    praise_num_list = []
    # 遍历时间，取出对应的值
    for v in list_week_day:
        res= Article.objects.filter(article_addtime__icontains=v).aggregate(clicknum=Sum('article_clicknum'),praisenum=Sum('article_praise_num'))
        # 判断点击量是否为none为none的情况下让他等于0
        clicknum = res['clicknum'] if (res['clicknum'] is not None)  else 0
        praisenum = res['praisenum'] if (res['praisenum'] is not None)  else 0
        # 追加的方式写入空白列表
        clicknum_list.append(clicknum)
        praise_num_list.append(praisenum)

    return render(request,'statistics/click.html',locals())


