import json,urllib
from urllib.parse import urlencode
# 定义一个发送短信的方法
def request2(mobile,num,m='GET'):
    # 聚合短信的通行证
    appkey = '8486d13610b1f330eb089e1c23f49e74'
    # 聚合短信的url地址
    url = "http://v.juhe.cn/sms/send"
    # 传过去的参数
    params = {
        # 接收短线的手机号
        'mobile': mobile,
        # 短信模板ID，参考聚合短信个人中心设置模板
        'tpl_id': '166894',
        # 传入模板的参数值 如果有特殊符号序号先转译一下
        'tpl_value': '#code#=%s'%num,
        # 应用appkey(应用详情页查询)
        'key': appkey,
        # 返回数据的格式
        'dtype': '',
    }
    # 转译一下传过去的参数
    params = urlencode(params)

    # 判断如果是GET方式
    if m =='GET':
        f = urllib.request.urlopen('%s?%s'%(url,params))
    else:
        f = urllib.request.urlopen(url,params)
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res['error_code']
        if error_code == 0:
            return 'ok'
        else:
            return '%s:%s'%(res['error_code'],res['reason'])
    else:
        return 'request api error'
