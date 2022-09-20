from calendar import isleap

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import GetData
import datetime as DT
'''
处理预测数据
'''

# 空气质量数据处理：只获取其中的数据
def setAir(week_data):
    airs = []
    for i in week_data['空气质量指数']:
        i = i.split(' ')[0]
        airs.append(int(i))
    return airs

# 气温数据处理：去掉数据的单位°并把数据变为整形
def setHighTemp(week_data):
    temperature = []
    for i in week_data['最高温']:
        i = i.split('°')[0]
        temperature.append(int(i))
    return temperature

def setLowTemp(week_data):
    temperature = []
    for i in week_data['最低温']:
        i = i.split('°')[0]
        temperature.append(int(i))
    return temperature

# 处理天气数据，为天气状态编码
def setCondition(week_data):
    # 天气状况编码
  flag = []
  for StringData in week_data['最低温']:
    if '晴' in str(StringData):
        flag.append(1)
    elif '多云' in str(StringData):
        flag.append(2)
    elif '阴' in str(StringData):
        flag.append(3)
    elif '雨' in str(StringData):
        flag.append(4)
    elif '雪' in str(StringData):
        flag.append(5)
    elif '雾' in str(StringData) or '霾' in str(StringData):
        flag.append(6)
    elif  '扬沙' in str(StringData):
        flag.append(7)
    else:
        flag.append(-1)
    return flag

def process(date):
   date['最高温']=setHighTemp(date)
   date['最低温']=setLowTemp(date)
   date['空气质量指数']=setAir(date)
   date1=date.drop('天气', axis=1)
   date2=date1.drop('风力风向',axis=1)
   return date2


def write(years, b,c):
    """
    :param years: [开始日期距离现在的年份]
    :param b: [开始日期距离现在日期的天数, 结束日期距离现在日期的天数]
    :param c: csv文件名
    :return: None
    """
    # 取现在日期
    today = DT.datetime.today()
    # 闰年片段
    st = isleap(today.year)
    # 取20天前日期
    week_ago = (today - DT.timedelta(days=b[0])).date()
    # 20天后
    week_pre = (today + DT.timedelta(days=b[1])).date()
    if week_ago.month + week_pre.month == 3 or week_ago.month + week_pre.month == 5:
        if week_ago.month == 2 and not st == isleap(today.year - years[0]):
            if st:
                # 今年是，去年或未来不是，所以-1
                week_ago -= DT.timedelta(days=1)
            else:
                # 今年不是，去年或未来是，所以+1
                week_ago += DT.timedelta(days=1)
        if week_pre.month == 2 and not st == isleap(today.year - years[1]):
            if st:
                # 今年是，去年或未来不是，所以要-1
                week_pre -= DT.timedelta(days=1)
            else:
                # 今年不是，去年或未来是，所以+1
                week_pre += DT.timedelta(days=1)
    #print(week_ago.year-years[0],week_ago.month,week_ago.day)
    #print(week_pre.year-years[1],week_pre.month,week_pre.day)
    # 爬取数据
    id =54161
    # 取到预处理后的用来预测的数据
    date0 = GetData.getPredictDate(week_ago.year-years[0],week_ago.month,week_ago.day,week_pre.year-years[1],week_pre.month,week_pre.day)
    date_=process(date0).set_index("日期")
    date_.to_csv(c)





# 功能: 对用来预测的数据进行预处理

def ProcessData():
    """
    X_train，y_train是原始的数据集。X_train,y_train 是原始数据集划分出来作为训练模型的，fit模型的时候用。
    X_test,y_test 这部分的数据不参与模型的训练，而是用于评价训练出来的模型好坏，score评分的时候用。
    :return:
        [X_train X训练数据集,
        X_valid X训练数据集的验证集,
        y_train Y训练数据集,
        y_valid Y训练数据集的验证集,
        imputed_X_test 预测数据集]
    """
    # 写入csv
    write([1,1], [14, 0], "date_train.csv")
    write([1,1],  [0, 14], "date_valid.csv")
    write([0,0], [14, 0], "date_test.csv")

    X_test = pd.read_csv("date_test.csv", index_col="日期", parse_dates=True)
    # 读取测试集和验证集
    X = pd.read_csv("date_train.csv", index_col="日期", parse_dates=True)
    y = pd.read_csv("date_valid.csv", index_col="日期", parse_dates=True)

    my_imputer = SimpleImputer()
    # train_test_split()是sklearn包的model_selection模块中提供的随机划分训练集和测试集的函数；
    # 使用train_test_split函数可以将原始数据集按照一定比例划分训练集和测试集对模型进行训练

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
    imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
    imputed_X_valid = pd.DataFrame(my_imputer.transform(X_valid))
    imputed_X_train.columns = X_train.columns
    imputed_X_valid.columns = X_valid.columns
    imputed_y_train = pd.DataFrame(my_imputer.fit_transform(y_train))
    imputed_y_valid = pd.DataFrame(my_imputer.transform(y_valid))
    imputed_y_train.columns = y_train.columns
    imputed_y_valid.columns = y_valid.columns
    imputed_X_test = pd.DataFrame(my_imputer.fit_transform(X_test))

    # 画折线图
    '''
    sns.lineplot(data=X)
    plt.show()
    sns.lineplot(data=y)
    plt.show()
    sns.lineplot(data=X_test)
    plt.show()
    '''
    # 返回分割后的数据集
    return [imputed_X_train, imputed_X_valid, imputed_y_train, imputed_y_valid, imputed_X_test]


