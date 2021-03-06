# 正常输入：
#
# 0. 乾之不动                            v
# 1. 乾 & 乾不动                         v
# 2. 乾 坤 & 乾为天 坤为地                v
# 3. 乾之坤 & 天之地                     v
# 4. 乾为天之坤为地 & 乾为天之坤          v
# 5. 乾为天 之 坤 & 乾为天 之 地为坤      v
#
# (用strip：删除两端的空格)
#
# python 不能表达式赋值，就是不能在if()里赋值，这点感觉不错
# python 里没有switch，要用if-else和字典，还有其他方法实现
#
#
# 乾为1 坤为2， 输入 1之2 感觉不方便
# 考虑用个符号代替之字， . 或者 -， 英文是点 中文是句号，不过减号中英相同
# 键入的都是字符
#
# https://regex101.com/
# 还有有一种算法，就是search函数，search 之，zhi，- 这三个关键字符, 比如 qianzhiqian
# 关键字符之前是本卦，关键字符之后为变卦
#
#  ▅▅▅▅▅
#  ▅▅　▅▅

__author__ = 'hanpeizhi'
import re
from datetime import datetime
import lookup_dic
import dir64gua
# from lookup_dic import to_bi

instr_gua = input('输入卦名：')
# instr_gua = '3 - 2'
#(ben_gua, bian_gua) = ('', '')  # 可不申明
#(bin_ben_gua, bin_bian_gua) = ('', '')
SYS_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# global chk_bengua
# global chk_biangua
matrix = [['  ' for col in range(13)] for row in range(6)]
# (yao1, yao2, yao3, yao4, yao5, yao6) = ('', '', '', '', '', '')
# instr_gua = instr_gua.strip()  # 检测前删除两端的空格
instr_gua = instr_gua.lower()


def get_benbian_gua():
    global ben_gua, bian_gua
    ben_gua = match_str.group(1)    # .lower()  # .rstrip()
    bian_gua = match_str.group(2)   # .lower()  # .lstrip()


def get_bin_benbian():
    global bin_ben_gua, bin_bian_gua    # chk_bengua, chk_biangua
    global chk_bin_bengua, chk_bin_biangua
    chk_bin_bengua = chk_bin_biangua = False
    # bin_ben_gua = lookup_dic.to_bin(ben_gua)
    # bin_bian_gua = lookup_dic.to_bin(bian_gua)

    for k, v in dir64gua.chk_64gua.items():
        if ben_gua in dir64gua.chk_64gua[k]:
            bin_ben_gua = k
            chk_bin_bengua = True

    if not chk_bin_bengua:  # 没有找到本卦
        bin_ben_gua = ' '

    for k, v in dir64gua.chk_64gua.items():
        if bian_gua in dir64gua.chk_64gua[k]:
            bin_bian_gua = k
            chk_bin_biangua = True

    if not chk_bin_biangua: # 没有找到变卦
        bin_bian_gua = ' '


#    if bin_ben_gua != ' ':  # 如果没有查到有效的本卦
#        chk_bengua = True
#    else:
#        chk_bengua = False
#
#    if bin_bian_gua != ' ':  # 如果没有查到有效的变卦
#        chk_biangua = True
#    else:
#        chk_biangua = False

    if bin_ben_gua == bin_bian_gua:  # 如果 本卦和变卦相同，就没有变卦
        bin_bian_gua = ' '
        chk_bin_biangua = False


# for i in range(6):
#        for j in range(12):
def set_liuyao():
    x = 0
    if chk_bin_bengua:  # 设置本卦的阴阳爻
        for i in bin_ben_gua:
            if i == '1':
                for y in range(5):
                    matrix[x][y] = '▅'
            elif i == '0':
                for y in range(5):
                    if not y == 2:
                        matrix[x][y] = '▅'
                    else:
                        matrix[x][y] = '  '
            # else:
            #     print('！')
            x += 1

    if chk_bin_bengua and chk_bin_biangua:  # 必须有本变卦 才能设置变卦的阴阳爻
        x = 0
        for i in bin_bian_gua:
            if i == '1':
                for y in range(8, 13):
                    matrix[x][y] = '▅'
            elif i == '0':
                for y in range(8, 13):
                    if not y == 10:
                        matrix[x][y] = '▅'
                    else:
                        matrix[x][y] = '  '
            # else:
            #     print('!！')
            x += 1


def set_dongyao():
    if chk_bin_bengua and chk_bin_biangua:  # 必须有本卦和变卦的时候才能设置动爻 ' ' == False
        for i in range(6):
            if bin_ben_gua[i] == '0' and bin_bian_gua[i] == '1':
                matrix[i][6] = 'X'
                matrix[i][7] = '→  '
            elif bin_ben_gua[i] == '1' and bin_bian_gua[i] == '0':
                matrix[i][6] = '0'
                matrix[i][7] = '→  '
        # else:
        #     print("!!!")


def print_liuyao():
    for x in range(6):
        print('\n')
        for y in range(13):
            print(matrix[x][y], end='')


# 两个卦名必须全中文 或者 拼音和数字
# 目前只匹配阿拉伯数字和小写拼音 #'\s*([a-zA-Z0-9]+)\s*-*[Zz][h]*i*之*\s*([a-zA-Z0-9]*)\s*'
# '1 - 2' or '1 - ' or '1' or '11 之 1'  
# qianzhiqian 还不行
match_str = re.match(r'\s*([a-zA-Z0-9]+)\s*[-之\s*]*\s*([a-zA-Z0-9]*)\s*', instr_gua)
if match_str:
    get_benbian_gua()
    get_bin_benbian()
else:
    match_str = re.match(r'\s*([\u4e00-\u9fa5]+)\s*[-之\s*]\s*([\u4e00-\u9fa5]*)\s*', instr_gua)
    if match_str:
        get_benbian_gua()
        get_bin_benbian()
    else:  # '乾'
        ben_gua = instr_gua
        get_bin_benbian()
        print('to check the dic')  # 如果字典里查不到就是输入错误

# main
# if __name__ == "__main__"：
print('输入的本卦：', ben_gua)
print('输入的变卦：', bian_gua)
print('本卦：', bin_ben_gua if bin_ben_gua else ' ')
print('变卦：', bin_bian_gua if bin_bian_gua else ' ')
print('本卦卦名：', dir64gua.chk_64gua[bin_ben_gua][1] if bin_ben_gua else ' ')
print('变卦卦名：', dir64gua.chk_64gua[bin_bian_gua][1] if bin_bian_gua else ' ')
set_liuyao()
set_dongyao()
print(SYS_TIME)
print_liuyao()
instr_gua = input('')

'''
# 排版

    0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28 
  0 ▅  ▅ '__' ▅  ▅ '__'  X '→__' ▅  ▅   ▅  ▅  ▅
  1 ▅  ▅ '__' ▅  ▅ '__' '__''__' ▅  ▅  '__' ▅  ▅
  2
  3
  4
  5 ▅  ▅ '__' ▅  ▅ '__'  X '→__' ▅  ▅   ▅  ▅  ▅
  6
  7
  8
  9
  



'''



'''

>>> s = 'zhi zhi'
>>> t = re.search('zhi',s)
>>> t
<_sre.SRE_Match object; span=(0, 3), match='zhi'>

>>> t.start()
0
>>> t.end()
3

>>> s.rfind('zhi')
4

>>> s.rindex('z')
>>> s.rindex('zhi')
4

if re.search('不动', instr_gua) and not re.search('之', instr_gua)\
    and not re.search('-', instr_gua):  # '乾不动'
        match_str = re.match('\s*(.+)\s*不动\s*(.*)\s*',
        instr_gua)  # if match_str:
        get_benbian_gua()
        get_bin_benbian()
    else:   #' 乾 - 不动 ' or '乾之不动' or ' 乾 之 不动 ' or '乾 坤'
            #  or '乾为天' or '乾为天之不动'  or '乾为天 之 不动'

match_str = re.match('\s*(.+)\s*之*\s*(.*)\s*', instr_gua)       # '乾之坤'

if match_str:
    get_benbian_gua()
    get_bin_benbian()
    if ben_gua == bian_gua or bian_gua == '不动':   # '乾之不动'
        bian_gua = ''
        get_bin_benbian()
else:
    match_str = re.match('(.*)\s+(.*)', instr_gua)  # '乾 坤'
    if match_str:
        get_benbian_gua()
        get_bi_benbian()
    else:
        if re.search('不动', instr_gua):  # '乾不动'
            match_str = re.match('(.*)不动(.*)', instr_gua)  # if match_str:
            get_benbian_gua()
            get_bi_benbian()
        else:  # '乾'
            ben_gua = instr_gua
            get_bi_benbian()
            print('to check the dic')  # 如果字典里查不到就是输入错误
        '''


'''

# 'QIAN' 'Qian' 'qIan' 'qiAN' ben bian gua检查是不是字母，是则全转成小写
# isalpha() 方法检测字符串是否只由字母组成，No space & digit in this string
# lower() 方法转换字符串中所有大写字符为小写


语法
################################################
#0. 乾之不动
#3. 乾之坤 & 天之地
#4. 乾为天之地为坤

>>> import re
>>> match = re.match('(.*)之(.*)', '乾之不动')
>>> match.group(1)
'乾'
>>> match.group(2)
'不动'
>>> match.groups()
('乾', '不动')
>>> match.group(0)
'乾之不动'

>>> match = re.match('(.*)之(.*)', '乾之')
>>> match
<_sre.SRE_Match object; span=(0, 2), match='乾之'>
>>> match.groups()
('乾', '')


################################################
#2. 乾 坤

>>> match = re.match('(.*)\s+(.*)', '乾 坤')
>>> match.groups()
('乾', '坤')

>>> re.split(r'\s+', '乾 坤')
['乾', '坤']

################################################
#1. 乾 & 乾不动

>>> if re.search('不动', '乾不动'):
    print('1')

1

>>> match = re.match('(.*)不动(.*)', '乾不动')
>>> match
<_sre.SRE_Match object; span=(0, 3), match='乾不动'>
>>> match.groups()
('乾', '')

#最后才是只有一个乾字的时候再直接查字典，如果查不到就报错

################################################

#5. 用strip：删除两端的空格

>>> s = '   乾   '
>>> s.strip()
'乾'

################################################

#...
#to be continued...
looks like done...
'''
