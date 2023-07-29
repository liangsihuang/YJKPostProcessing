import sqlite3

# 自定义工具函数：取某一层的所有梁ID,输入塔号、层号，返回梁ID列表
def getBeamIDs(TowekNo, FloorNo):
    beamIDs = []
    t = "SELECT ID FROM tblBeamSeg WHERE TowNo=(?) AND FlrNo=(?)"
    cur.execute(t,(TowelNo, FloorNo))
    t1 = cur.fetchall()
    for t2 in t1:
        beamIDs.append(t2[0])
    return beamIDs

# 建立与数据库文件的连接
conn = sqlite3.connect('dtlCalc-小.ydb')

# 创建游标cursor对象
cur = conn.cursor()

# 取得模型的总层数
t = "SELECT ParaVal FROM tblProjectPara WHERE ID=2"
cur.execute(t)
FloorTotal = cur.fetchall()[0][0]
#塔号，主结构一般塔号是1
TowelNo = 1 


# for i in range(1,FloorTotal+1):

beamIDs = getBeamIDs(TowelNo, 1)
# print(type(beamIDs))
# print(beamIDs)







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




cur.close()
conn.close()