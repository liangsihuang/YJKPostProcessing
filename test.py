import re
#正则表达式库
filepath ='C:\\Users\lyoshi\Desktop\YJKPostProcessing\测试源文件\wdisp.out'
# 路径第一个是双斜线
f = open(filepath,'r', encoding='ANSI')
# print(f)
for line in f.readlines():
    s = 'X 方向地震作用下的楼层最大位移'
    if s in line:
        print(line)
#利用正则表达式筛选数据
# print(a[100])

f.close()
