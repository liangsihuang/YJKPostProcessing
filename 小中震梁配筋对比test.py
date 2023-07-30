import sqlite3
import matplotlib.pyplot as plt

# 建立与数据库文件的连接
conn1 = sqlite3.connect('dtlCalc-小.ydb')
conn2 = sqlite3.connect('dtlCalc-中.ydb')
# 创建游标cursor对象
cur1 = conn1.cursor()
cur2 = conn2.cursor()

# 取得模型的总层数
sqltext = "SELECT ParaVal FROM tblProjectPara WHERE ID=2"
cur1.execute(sqltext)
FloorTotal = cur1.fetchall()[0][0]
#塔号，主结构一般塔号是1
TowelNo = 1

# 自定义工具函数：取某一层的所有梁ID,输入塔号、层号，返回梁ID列表
def getBeamIDs(TowekNo, FloorNo):
    beamIDs = []
    sqltext = "SELECT ID FROM tblBeamSeg WHERE TowNo=(?) AND FlrNo=(?)"
    cur1.execute(sqltext,(TowelNo, FloorNo))
    t1 = cur1.fetchall()
    for t2 in t1:
        beamIDs.append(t2[0])
    return beamIDs

# 画散点图用的坐标，x是中震/小震比值，y是层号
x = []
y = []
# 画堆叠柱状图用的坐标，标签barlable是层号列表，bar1是中震配筋控，ratio>1，bar2是配筋相等，ratio=1，，bar3是小震配筋控，ratio<1
barlable = list(range(1,FloorTotal+1))
bar1 = []
bar2 = []
bar3 = []


for FloorNo in range(1,FloorTotal+1):
    beamIDs = getBeamIDs(TowelNo, FloorNo)
    # 每层分别统计中震配筋控、配筋相等、小震配筋控的数量，占比用于作图
    num1 = 0
    num2 = 0
    num3 = 0
    for beamid in beamIDs:
        # 顶筋只比较左右两端截面处的配筋
        # 底筋比较最大值
        # 从YJK数据库取出的配筋数值是文本，要转换为数字
        # 取出顶筋
        sqltext = "SELECT AsTop FROM tblRCBeamDsn WHERE ID=(?)"
        cur1.execute(sqltext,(beamid,))
        t1 = cur1.fetchall()[0][0]
        t1 = t1.split(',')
        cur2.execute(sqltext,(beamid,))
        t2 = cur2.fetchall()[0][0]
        t2 = t2.split(',')
        t1 = list(float(x) for x in t1)
        t2 = list(float(x) for x in t2)
        # 判断此梁是否配筋全为0, 如果是则跳过该梁
        if max(t1) == 0.0 and max(t2) == 0.0:
            continue
        # 小震左顶筋、右顶筋
        AsTopLeft1 = float(t1[0])
        AsTopRight1 = float(t1[-1])
        # 中震左顶筋、右顶筋
        AsTopLeft2 = float(t2[0])
        AsTopRight2 = float(t2[-1])
        # 取出底筋
        sqltext = "SELECT AsBtm FROM tblRCBeamDsn WHERE ID=(?)"
        cur1.execute(sqltext,(beamid,))
        t1 = cur1.fetchall()[0][0]
        t1 = t1.split(',')
        cur2.execute(sqltext,(beamid,))
        t2 = cur2.fetchall()[0][0]
        t2 = t2.split(',')
        t1 = list(float(x) for x in t1)
        t2 = list(float(x) for x in t2)
        # 小震底筋最大值
        AsBtmMax1 = max(t1)
        # 中震底筋最大值
        AsBtmMax2 = max(t2)

        # print(beamid,AsTopLeft1,AsTopRight1,AsBtmMax1)

        # 悬挑梁可能顶筋一端为0，由于梁跨未按实际（按有限元单元），可能出现梁顶筋全为0或底筋全为0
        if AsTopLeft1 == 0.0 and AsTopRight1 != 0.0:
            steelbarRatio = max(AsTopRight2/AsTopRight1,AsBtmMax2/AsBtmMax1)
        elif AsTopRight1 == 0.0 and AsTopLeft1 != 0.0:
            steelbarRatio = max(AsTopLeft2/AsTopLeft1,AsBtmMax2/AsBtmMax1)
        elif AsTopRight1 == 0.0 and AsTopLeft1 == 0.0:
            steelbarRatio = AsBtmMax2/AsBtmMax1
        elif AsBtmMax1 == 0.0:
            steelbarRatio = max(AsTopLeft2/AsTopLeft1,AsTopRight2/AsTopRight1) 
        else:
            steelbarRatio = max(AsTopLeft2/AsTopLeft1,AsTopRight2/AsTopRight1,AsBtmMax2/AsBtmMax1)

        # 有根梁配筋比值大于2，删除
        if steelbarRatio>2:
            continue
        x.append(steelbarRatio)
        y.append(FloorNo)

        if steelbarRatio > 1.0:
            num1 = num1 + 1
        elif steelbarRatio == 1.0:
            num2 = num2 + 1
        else:
            num3 = num3 + 1
    numall = num1 + num2 + num3
    bar1.append(num1/numall)
    bar2.append(num2/numall)
    bar3.append(num3/numall)
    

# # 画散点图
# # s：点的大小，默认是20
# plt.scatter(x,y,s=5)
# # 画线,plot的第一个参数全是x坐标，第二个参数全是y坐标
# plt.plot([1,1],[0,FloorTotal],linestyle='dashed',color='red')
# # 设置轴标签
# plt.xlabel('框架梁纵筋面积 中震/小震')
# plt.ylabel('层号')
# # 设置正常显示中文
# plt.rcParams['font.sans-serif']=['SimHei']

# plt.show()

# 画堆叠柱状图(竖向柱状图，ax.bar())
# fig, ax = plt.subplots()
# ax.bar(barlable, bar1, width=0.4, label='中震配筋控')
# ax.bar(barlable, bar2, width=0.4, bottom=bar1, label='配筋相等')
# ax.bar(barlable, bar3, width=0.4, bottom=[i+j for i,j in zip(bar1,bar2)], label='小震配筋控')
# ax.set_ylabel('层号')
# ax.legend() #图例
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.show()

# 画堆叠柱状图(横向柱状图，ax.barh())
fig, ax = plt.subplots()
ax.barh(barlable, bar1, label='中震配筋控', color='red')
ax.barh(barlable, bar2, left=bar1, label='配筋相等', color='blue')
ax.barh(barlable, bar3, left=[i+j for i,j in zip(bar1,bar2)], label='小震配筋控', color='green')
ax.set_ylabel('层号')
ax.set_xlabel('构件屈服比例（红色为屈服）')
ax.legend() #图例
plt.rcParams['font.sans-serif']=['SimHei']
plt.show()

# print(type(beamIDs[0]))
# print(len(beamIDs))
# text1 = "SELECT AsTop FROM tblRCBeamDsn WHERE ID=1000001"
# cur.execute(text1)
# re = cur.fetchall()
# print(re)
# print(type(re))
# print(re[0])
# print(re[0][0])
# print(type(re[0][0]))

# s = re[0][0]
# s = s.split(',')
# print(s)

# for i in s:
#     s1 = float(s)
# s1 = float(s)




cur1.close()
cur2.close()
conn1.close()
conn2.close()