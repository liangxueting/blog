# 导入一个随机数包
import random
# 导入Pillow的所运用的模块（图形验证码所需要的模块）(image图片制作模块,imageDraw图片绘画模块,imageFont图形字体模块)
from PIL import Image,ImageDraw,ImageFont
# 导入io模块
from io import BytesIO
# 定义一个随机颜色值(随机生成3个0-255的三个数字)
# def get_random_color():
#     return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def get_valid_code_img(request):
    # 1.定义制作一个随机颜色的图片对象(RGB,(270,40)图片的类型及大小,背景颜色随机色(调用的get_random_color()随机色方法))
    img = Image.new('RGB',(114,46),color=(60,180,40))
    # 对图片进行绘画(写入对象,生成的图片颜色)(实例化出一个图片)
    draw = ImageDraw.Draw(img)
    # 创建一个字体的对象
    kumo_font = ImageFont.truetype('static/font/kumo.ttf',size=32)
    # 定义一个空白字符串
    valid_code_str = ''
    # for in 循环出随机数
    for i in range(4):
        # 获取第一个数字
        random_num = str(random.randint(0,9))  #获取一个0-9的随机数字
        # 获取第二个数字
        random_low_alpha = chr(random.randint(97,122))  #获取一个a-z的小写随机字母
        # 获取第三个数字
        random_upper_alpha = chr(random.randint(65,90)) #获取一个A-Z的大写随机字母
        # 从上面的三个随机数中再获的一个随机数
        random_char = random.choice([random_num,random_low_alpha,random_upper_alpha])
        # 将获取的随机数写入到指定的图形中去
        #(i * 50 + 20, 5)写入的位置， random_char写入的内容， get_random_color()写入的随机颜色，  font=kumo_font写入的字体类型
        draw.text((i*20+15,5),random_char,(255,255,255),font=kumo_font)
        # 将要写入的随机数字拼接在一起
        valid_code_str += random_char

    # 创建验证码的干扰项
    # width = 270
    # height = 40
    # 1.干扰线条(for循环，循环一次创建一条线条)
    # for i in range(5):
        #(创建(四个坐标)形成两个点画一条线)
        # x1 = random.randint(0,width)
        # x2 = random.randint(0,width)
        # y1 = random.randint(0,height)
        # y2 = random.randint(0,height)
        # 画一条线((x1,y1,x2,y2)形成两个点，fill=get_random_color()随机线的颜色)
        # draw.line((x1,y1,x2,y2),fill=get_random_color())

    # 2.干扰原点(for循环，循环一次创建一个点)
    # for i in range(500):
        #[random.randint(0, width), random.randint(0, height) 获取一个随机的横坐标，获取一个随机的纵坐标。
        #fill = get_random_color() 获取一个随机色
        # draw.point([random.randint(0,width),random.randint(0,height)],fill=get_random_color())

    # 3.干扰小断线
    # for i in range(10):
        # 获取随机的x轴坐标
        # x = random.randint(0,width)
        # 获取随机的y轴坐标
        # y = random.randint(0,height)
        #(x, y, x, y + 15) 控制小短线的弧度(随机位置)
        # 0, 90, 控制小短线的长度 (角度)
        #fill = get_random_color() 控制小短线的颜色(随机色)
        # draw.arc((x,y,x+5,y+5),0,500,fill=get_random_color())
    request.session['valid_code_str'] = valid_code_str




    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()

    return data