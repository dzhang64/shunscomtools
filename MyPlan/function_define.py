from math import *
from pyproj import Transformer, CRS
from sklearn.neighbors import KNeighborsClassifier


def se_angle(angle, HBWD, HBWD_R):
    if float(HBWD) * HBWD_R >= 360:
        s0 = 0
        e0 = 360
    else:
        s0 = azimuth_xy(angle) - float(HBWD) * HBWD_R / 2
        e0 = azimuth_xy(angle) + float(HBWD) * HBWD_R / 2
    return s0, e0


# def distancefuc(lon1, lat1, lon2, lat2):
#     return haversine((lat1, lon1), (lat2, lon2)) * 1000

def distancefuc(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(
        radians,
        [float(lon1), float(lat1),
         float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance, 0)
    return distance


def azimuth(lon1, lat1, lon2, lat2):
    """
    经纬度判断方位
    """
    from geographiclib.geodesic import Geodesic
    geod = Geodesic.WGS84
    ll = geod.InverseLine(lat1, lon1, lat2, lon2)
    s12 = distancefuc(lat1, lon1, lat2, lon2)
    g = ll.Position(s12, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
    if g['azi2'] < 0:
        g['azi2'] = g['azi2'] + 180
    return g['azi2']


def wgs842utm(lon, lat):
    """
    经纬度转UTM坐标
    :param lon: 经度
    :param lat: 维度
    :return: UTM的xy坐标
    """
    d = int(lon / 6) + 31
    L0 = (6 * d - 3) - 180
    format1 = '+proj=tmerc +lat_0=0 +lon_0=' + str(L0) + ' +k=0.9996 +x_0=500000 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    crs_WGS84 = CRS.from_epsg(4326)  # WGS84地理坐标系
    crs_UTM = CRS.from_proj4(format1)
    transformer = Transformer.from_crs(crs_WGS84, crs_UTM)
    utm_x, utm_y = transformer.transform(lat, lon)
    return utm_x, utm_y


def knn_distance(data, find):
    """
    data:数据帧，源数据
    find:数据帧，待规划邻区数据
    """
    # 从数据库中筛选出经纬度特征数据，用于给KNN分类器训练
    data_fit = data.loc[:, ['LON', 'LAT']]
    # y本身用于标注每条数据属于哪个类别，但我并不使用KNN的分类功能，所以统一全部标注为类别1
    y = [1] * len(data_fit)
    # 筛选需要求出最近N个点的的基站的经纬度特征数据
    find_x = find.loc[:, ['LON', 'LAT']]
    # 指定算法为ball_tree
    knn = KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', metric=lambda s1, s2: distancefuc(*s1, *s2))
    # 训练模型
    knn.fit(data_fit, y)
    # 计算它们最近的N个（n_neighbors）点，这里生成全量数据便于后面筛选距离
    distance, points = knn.kneighbors(find_x, n_neighbors=data.shape[0], return_distance=True)
    return distance, points


def azimuth_xy(azimuth):
    if azimuth > 90:
        A1 = 90 - float(azimuth) + 360
    else:
        A1 = 90 - float(azimuth)
    return A1


if __name__ == '__main__':
    # print(haversine((34.29972, 117.15964), (34.29913, 117.16635)) * 1000)
    print(distancefuc(20, 30, 50, 30))
    print(sqrt(pow((13042151.466323247 - 13042898.420106467), 2) + pow((4069118.451939744 - 4069038.948023094), 2)))
