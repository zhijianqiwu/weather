import requests
import pandas as pd
import datetime
'''
 使用python爬虫技术,爬取长春和全国的天气信息数据
 爬取网站：http://tianqi.2345.com/wea_history/54161.htm
 areaid 和各省会城市对应关系
 area_id = [
    ("黑龙江", 50953), ("内蒙古", 53463),("吉林", 54161), ("辽宁", 54342),
    ("河北", 53698), ("天津", 54527), ("山西", 53772), ("陕西",57036 ),
    ("甘肃",52889 ), ("宁夏",53614 ), ("青海",52866 ), ("新疆", 51463),
    ("西藏", 55591), ("四川", 56294), ("重庆", 57516), ("山东", 54823),
    ("河南", 57083), ("江苏",58238 ), ("安徽", 58321), ("湖北", 57494),
    ("浙江", 58457), ("福建",58847 ), ("江西", 58606), ("湖南",57687 ),
    ("贵州",57816 ), ("广西", 59431), ("海南",59758 ), ("上海",58362 ),
     ("广东",59287),  ("云南",56778), ("台湾",59554) ,
]
 
'''

# 提供年份和月份，爬取对应的的表格数据
url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
   "User-Agent":
       """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"""
}

def craw_table(id,year,month):
    params = {
        "areaInfo[areaId]": id,
        "areaInfo[areaType]": 2,
        "date[year]": year,
        "date[month]": month
    }
    resq = requests.get(url, headers=headers, params=params)
    data = resq.json()["data"]
    # data frame
    df = pd.read_html(data)[0]
    return df


# 输入城市id，爬取该城市今日的天气数据
def getToday(id):
    # 获取当前年份和月份
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    # 获取当日长春天气数据
    month_data =craw_table(id, year, month)
    return month_data.tail(1)

# 输入城市id，爬取该城市近七周的天气数据
def getWeek(id):
    # 获取当前年份和月份
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    # 获取当日长春天气数据
    month_data =craw_table(id, year, month)
    return month_data.tail(7)

# 爬取全国各个省会城市的今日的天气数据
def getChinaToday():
    ids=[50953, 53463,54161,54342,53698,54527,53772,57036 ,52889,53614,52866,51463,
          55591, 56294, 57516,54823,57083,58238, 58321, 57494, 58457,58847,58606,
          57687,57816 ,59431,59758 ,58362 ,59287,56778,59554]
    list=[]
    for i in ids:
        df=getToday(i)
        list.append(df)
    return pd.concat(list).reset_index(drop=True)

# 获取长春最近3年的天气数据，用于预测
def getYears():
    today = datetime.datetime.today()
    df_list = []
    for year in range(today.year-5, today.year):
      for month in range(1, 13):
          df = craw_table(54161,year, month)
          df_list.append(df)

    for month in range(1,today.month+1):
        df = craw_table(54161, today.year, month)
        df_list.append(df)
     # 多年数据合并
    return pd.concat(df_list).reset_index(drop=True)

# 传入一个时间范围，获取某个时间范围的天气数据
def getPredictDate(year0,month0,day0,year1,month1,day1):
    id=54161
    date_list=[]
    if month0!=month1:
      date0=craw_table(id,year0,month0)
      date_ago=date0[day0-1:]
      date1 = craw_table(id,year1, month1)
      date_pre = date1[:day1]

      date_list.append(date_ago)
      date_list.append(date_pre)
      date=pd.concat(date_list).reset_index(drop=True)
    else:
      date0 = craw_table(id, year0, month0)
      date=date0[day0-1:day1]
    return date



'''
def craw_year(year1, year2):
    df_list= []
    for year in range(year1, year2):
        for month in range(1, 13):
            df =craw_table(year, month)
            df_list.append(df)
    # 多年数据合并
    return pd.concat(df_list).reset_index(drop=True)
    
    #df =craw_table(2022,4)
#print(df)
#date =df["最高温"]
#print(date)
'''




