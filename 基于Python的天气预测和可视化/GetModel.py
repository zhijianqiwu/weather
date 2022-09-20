
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.metrics import mean_absolute_error
import ProcessData


# 训练并保存模型
def getModel(a="Model.pkl"):
    """
    :param a: 模型文件名
    :return:
        [socre: MAE评估结果,
        X_test: 预测数据集]
    """
    # 获取测试集、训练集、验证集
    [X_train, X_valid, y_train, y_valid, X_test] = ProcessData.ProcessData()

    # 随机树森林模型
    model = RandomForestRegressor(random_state=0, n_estimators=1001)
    # 训练模型
    model.fit(X_train, y_train)
    # 预测模型
    preds = model.predict(X_valid)
    # 用MAE评估
    score = mean_absolute_error(y_valid, preds)
    # 保存模型到本地
    joblib.dump(model, a)
    # 返回MAE
    return [score, X_test]
