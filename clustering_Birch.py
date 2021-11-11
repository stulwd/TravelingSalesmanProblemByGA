import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import Birch

# X为样本特征，Y为样本簇类别， 共1000个样本，每个样本2个特征，共4个簇，簇中心在[-1,-1], [0,0],[1,1], [2,2]
X, y = make_blobs(n_samples=1000, n_features=2, centers=[[-1,-1], [0,0], [1,1], [2,2]], cluster_std=[0.4, 0.3, 0.4, 0.3],
                  random_state =9)

f = open("Cluster_dataset.txt", "r")
cityData = []
for i in range(50):
    each_city = f.readline()
    each_city = list(map(float, each_city.split()))
    cityData.append(each_city)
f.close()
X = np.array(cityData)


##设置birch函数
birch = Birch(n_clusters = 3)
##训练数据
y_pred = birch.fit_predict(X)
##绘图
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.show()