import joblib
import datetime as DT
import GetModel
from pyecharts.charts import Bar, Grid, Line, Tab
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Map
from pyecharts import options as opts


# 训练并保存模型并返回MAE
import ProcessData
import GetData

r = GetModel.getModel()
print("MAE:", r[0])
# 读取保存的模型
model = joblib.load('Model.pkl')

# 最终预测结果
preds = model.predict(r[1])

print("未来7天预测")
for a in range(0, 7):
    today = DT.datetime.now()
    time = (today + DT.timedelta(days=a)).date()
    print(time.year, '-', time.month, '-', time.day,
          '最高气温', preds[a][0],
          '最低气温', preds[a][1],
          "空气质量", preds[a][2],
          )


'''
数据可视化代码
通过爬虫获取到的天气信息，利用pyecharts框架来实现绘图功能，实现天气的可视化
'''


'''
可视化当日长春天气数据
'''
# 获取当日长春天气数据
today_data = GetData.getToday(54161)
headers_ = ["日期", "最高温", "最低温", "天气", "风力风向", "空气质量指数"]
rows_ = [
    [today_data['日期'].values[0], today_data['最高温'].values[0], today_data['最低温'].values[0],
     today_data['天气'].values[0], today_data['风力风向'].values[0], today_data['空气质量指数'].values[0]],
]
def table_main() ->Table:
  c=(
    Table()
    .add(headers_, rows_)
    .set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="")
    )
  )
  return c


'''
可视化当日长春近一周的天气质量和气温
'''
# 获取最近七天的天气数据
week_data=GetData.getWeek(54161)
# 最近长春一周的天气和空气
airs = ProcessData.setAir(week_data)
low_temperature = ProcessData.setLowTemp(week_data)
high_temperature = ProcessData.setHighTemp(week_data)

def grid_week() -> Grid:
    x_data = ["前七天", "前六天", "前五天", "前四天", "前三天", "前两天", "前一天"]
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "最高温",
           high_temperature,
            yaxis_index=0,
            color="#d14a61",
        )
        .add_yaxis(
            "最低温",
            low_temperature,
            yaxis_index=1,
            color="#5793f3",
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="最高温",
                type_="value",
                min_=-30,
                max_=40,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="天气质量指数",
                min_=0,
                max_=300,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="最低温",
                min_=-30,
                max_=40,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            ),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "天气质量指数 "
            "优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
            airs,
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(
        bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True
    )

'''
可视化预测长春的天气
'''

# 预测长春一周的天气和空气
predict_airs=[]
predict_low_temperature=[]
predict_high_temperature=[]
x_data=[]
for i in range(0,7):
    predict_high_temperature.append(round(preds[i][0],4))
    predict_low_temperature.append(round(preds[i][1],4))
    predict_airs.append(round(preds[i][2],4))
    x_data.append((today + DT.timedelta(days=i)).date())

def grid_week_predict() -> Grid:
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "最高温",
           predict_high_temperature,
            yaxis_index=0,
            color="#d14a61",
        )
        .add_yaxis(
            "最低温",
            predict_low_temperature,
            yaxis_index=1,
            color="#5793f3",
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="最高温",
                type_="value",
                min_=-30,
                max_=40,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="天气质量指数",
                min_=0,
                max_=300,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="最低温",
                min_=-30,
                max_=40,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            ),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "天气质量指数 "
            "优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
            predict_airs,
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(
        bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True
    )




'''
获取全国各省会城市今日的天气情况
'''
china_today = GetData.getChinaToday()
china_today.to_csv("china_today.csv")


def setData(str,i):
    return china_today[i:i+1][str].values[0]
provinces = [
    "黑龙江","内蒙古", "吉林",  "辽宁", "河北","天津","山西", "陕西",
    "甘肃","宁夏", "青海","新疆", "西藏", "四川", "重庆", "山东", "河南",
    "江苏", "安徽","湖北", "浙江", "福建", "江西", "湖南", "贵州",
    "广西", "海南","上海","广东","云南","台湾"
]
rows=[]
for i in range(0,31):
    rows.append([provinces[i],setData('最低温',i),setData('最高温',i),setData('天气',i),setData('风力风向',i)])


def today_china_table() ->Table:
  c=(
    Table()
    .add(["省份","最低温","最高温", "天气", "风力风向"], rows)
    .set_global_opts(
     title_opts=ComponentTitleOpts(title="今日全国各省会城市的天气信息表", subtitle="")
  )
  )
  return c


china_airs = ProcessData.setAir(china_today)
airs_list=[]
for i in range(0,31):
    airs_list.append(china_airs[i])

def today_china() ->Map:
    c = (
        Map()
        .add("天气质量指数 优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)", [list(z) for z in zip(provinces, airs_list)], "china")
        .set_global_opts(
         title_opts=opts.TitleOpts(title="今日中国空气质量"),
         visualmap_opts=opts.VisualMapOpts(max_=300),
        )
    )
    return c


# 分页图的标题
tab = Tab()
tab.add(table_main(), "今日长春")
tab.add(grid_week_predict(), "未来长春")
tab.add(grid_week(), "近一周长春")
tab.add(today_china_table(), "今日中国天气")
tab.add(today_china(), "今日全国空气质量")
tab.render("天气网.html")


'''
 
    all_high_t = []
    all_low_t = []
    all_air = []
    all_high_t.append(preds[a][0])
    all_low_t.append(preds[a][1])
    all_air.append(preds[a][2])
temp = {"最高温": all_high_t, "最低温": all_low_t, "空气质量": all_air}
# 绘画折线图
plt.plot(range(1, 7), temp["最高温"], color="red", label="high_t")
plt.plot(range(1, 7), temp["最低温"], color="blue", label="low_t")
plt.legend()  # 显示图例
plt.ylabel("Temperature(°C)")
plt.xlabel("day")
# 显示
plt.show()
plt.plot(range(1, 7), temp["空气质量"], color="black", label="air")
plt.legend()
plt.ylabel(" ")
plt.xlabel("day")
plt.show()
'''