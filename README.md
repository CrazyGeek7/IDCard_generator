## 0x00 前言

    最近过生日，女朋友送了几本Python黑客编程的书（没错，小黑阔也是可以有女朋友的）。哈哈，皮一下就是很开心。

    言归正传，最近看这几本Python黑客编程的书有点上头，感觉理论是有了，就是没有实践。然后我就盯上了我们学校教务处（滑稽脸）。看着账号密码的输入框，对着电脑相视一笑，搞一波？

    我们学校的教务处系统默认密码为身份证号码，于是我就打算写一个自动生成身份证号字典的Python脚本。只要能生成一个字典，就能靠Burpsuite的Intruder功能提交Web表单，实现暴力破解。

## 0x01 身份证号码结构

    公民身份号码是特征组合码，由十七位数字本体码和一位校验码组成。排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位数字校验码。

    地址码表示编码对象常住户口所在县（市、旗、区）的行政区划代码，按GB/T2260的规定执行。

    出生日期码表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。

    顺序码表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。

    校验码是根据前面十七位数字码，按照ISO 7064:1983.MOD 11-2校验码计算得出。

    具体参考：[https://baike.baidu.com/item/](https://baike.baidu.com/item/)居民身份证号码?fromtitle=身份证号码&fromid=2135487

## 0x02 校验码规则

    1、将前面的身份证号码17位数分别乘以不同的系数。从第一位到第十七位的系数分别为：7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 ；

    2、将这17位数字和系数相乘的结果相加；

    3、用加出来和除以11，看余数是多少；

    4、余数只可能有0 1 2 3 4 5 6 7 8 9 10这11个数字。其分别对应的最后一位身份证的号码为1 0 X 9 8 7 6 5 4 3 2；

    5、通过上面得知如果余数是2，就会在身份证的第18位数字上出现罗马数字的X。

    例如：某男性的身份证号码是34052419800101001X。我们要看看这个身份证是不是合法的身份证。

    首先：我们计算3*7+4*9+0*10+5*5+...+1*2，前17位的乘积和是189

    然后：用189除以11得出的结果是商17余2

    最后：通过对应规则就可以知道余数2对应的数字是x。所以，这是一个合格的身份证号码。

    具体参考：[https://baike.baidu.com/item/](https://baike.baidu.com/item/)身份证校验码/3800388?fr=aladdin

## 0x03 思路

    一个完整的身份证号码包括地址码，出生日期码，顺序码，校验码。那么我们可以通过社工的手段获取到对方的地址和出生日期（相信这对各位黑阔大佬，社工大佬不是什么问题），这样我们就得到了地址码加出生日期码。比如说我们知道对方是的户籍是北京朝阳区，生于2000年1月1日，那么我们就可以得到对方的前14位身份证号码：11010520000101。我们再列举出从001到999的3位顺序码，将前面的14位身份证号码加上3位顺序码一共17位代入校验规则中计算出校验码。这样我们可以列出来的字典有999中可能。

    如果我们知道对方的性别的话，我们则可以筛选一下顺序码。因为顺序码规则中奇数分配给男性，偶数分配给女性。这样列出来的男性身份证号的字典有500种可能，女性身份证号码的字典则有499种可能。

## 0x04 代码分析

```
import os
#根据地址码，出生日期码，性别生成身份证号码字典函数。性别可以为空
def generator(address_code,birthday_code,sex=""):
    id_list=[]
    #如果地址码不等于6位
    if len(address_code)!=6:
        print "address code error"
                    return
    #如果出生日期码不等于8位
    if len(birthday_code)!=8:
        print "birthday code error"
            return
    #如果性别为空的话则不对顺序码进行奇偶判断
    if sex == "":
        for i in range(1,1000):
            i = repair_i(str(i))
                id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
                id_list.append(id)
    #如果性别位男，则对顺序码进行奇偶判断，如果顺序码为偶则跳过
    elif sex == "male":
        for i in range(1,1000):
            if i%2 == 0:
                pass            
            else:
                i = repair_i(str(i))
                id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
                id_list.append(id)
    #如果性别位女，则对顺序码进行奇偶判断，如果顺序码为奇则跳过
    elif sex == "female":
        for i in range(1,1000):
            if i%2 != 0:
                pass
            else:
                i = repair_i(str(i))
                id = address_code + birthday_code + i + cheak(address_code + birthday_code + i)
                id_list.append(id)
                return id_list

#进行校验位计算的方法
def cheak(s):
    sum = int(s[0]) * 7 + int(s[1]) * 9 + int(s[2]) * 10 + int(s[3]) * 5 + int(s[4]) * 8 + int(s[5]) * 4 + int(s[6]) * 2 + int(s[7]) * 1 + int(s[8]) * 6 + int(s[9]) * 3 + int(s[10]) * 7 + int(s[11]) * 9 + int(s[12]) * 10 + int(s[13]) * 5 + int(s[14]) * 8 + int(s[15]) * 4 + int(s[16]) * 2
    return '10X98765432'[sum % 11]

#对顺序码进行补全
def repair_i(i):
    #如果顺序码长度为1，则在左边补“00”
    if len(i) == 1:
        i = "00" + I
    #如果顺序码长度为2，则在左边补“0”
    elif len(i) == 2:
        i = "0" + i
     return i

def main():
    address = "110105"                          #地址码
    birthday = "20000101"                       #出生日期码
    sex = "male"                                #性别
    id_list = generator(address,birthday,sex)
    #用系统的echo命令和“>>”输出流，将字典列表中的每个身份证号码输出到txt
    for i in range(len(id_list)):
        os.system("echo " + id_list[i] + " >> " + "../IDCard_dictionary/" + address + birthday + sex + ".txt")

if __name__ == "__main__":
    main()
```

## 0x05 写在最后

    本文源代码链接：[https://github.com/CrazyGeek7/IDCard_generator.git](https://github.com/CrazyGeek7/IDCard_generator.git)

    我来自西南某不知名高校，喜欢研究网络安全，数据挖掘，机器学习以及人工智能。这也是我第一次在微信公众号上投稿，无论是水平还是经验，都比不上各位大佬，文中出现的错误与不足请各位大佬多多指教。

    我的个人邮箱是：CrazyGeek7@qq.com。

    我的微博主页是：[https://weibo.com/5778036633](https://weibo.com/5778036633)。

    我的Github主页是：[https://github.com/CrazyGeek7](https://github.com/CrazyGeek7)。
