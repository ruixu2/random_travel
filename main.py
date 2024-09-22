import geopandas as gpd
import random
import config
from shapely.geometry import Point
import os
import datetime
import folium
from folium.plugins import MarkerCluster
from folium import FeatureGroup, Marker
from folium.map import Popup
import plotly.graph_objects as go

def random_point(minx, miny, maxx, maxy):
    x = random.uniform(minx, maxx)
    y = random.uniform(miny, maxy)
    return x, y


def isin_area(_gdf, x, y):
    point=Point(x,y)
    res=_gdf['geometry'].geometry.contains(point)
    if res[0]:
        return True
    return False
def write_history(point,address):
    if not os.path.exists("./history.csv"):
        f=open("history.csv",mode='w',encoding="utf-8")
        f.write("生成时间;address;去过了吗;x;y\n")
        f.close()
    f=open("history.csv",mode='a',encoding='utf-8')
    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x=round(point[0],4)
    y=round(point[1],4)
    f.write(f"{t};{address};no;{x};{y}\n")
    f.close()

def create_map(point_list,address_list):
    # 纬度、经度
    for item in point_list:
        x=item[0]
        y=item[1]
    coordinates=point_list
    # 创建地图，设置初始位置和缩放级别
    m = folium.Map(location=[x,y], zoom_start=10,tiles="OpenStreetMap",crs="EPSG4326") # CartoDB Positron, OpenStreetMap
    """    - "OpenStreetMap"
    - "Mapbox Bright" (Limited levels of zoom for free tiles)
    - "Mapbox Control Room" (Limited levels of zoom for free tiles)
    - "Stamen" (Terrain, Toner, and Watercolor)
    - "Cloudmade" (Must pass API key)
    - "Mapbox" (Must pass API key)
    - "CartoDB" (positron and dark_matter)"""
    # 添加标记到地图
    i=0
    for coord in coordinates:
        lat, lon = coord
        folium.Marker(
            location=[x,y],
            popup=address_list[i]
        ).add_to(m)
    # 保存地图为HTML文件
        i+=1
    m.save('map.html')

def create_map_by_plotly(point_list,address_list):
    i=0
    latitudes=[] 
    longitudes=[]
    for item in point_list:
        latitudes.append(item[0]) # 纬度
        longitudes.append(item[1])# 经度

    # 创建散点图层，用于表示标记
    scatter_map = go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=address_list,  # 标记的文本说明
    )

    # 创建图形对象
    fig = go.Figure(data=[scatter_map])

    # 显示地图
    fig.show()

if __name__ == '__main__':
    gdf = gpd.read_file(config.area_file)
    gdf.to_crs(crs='EPSG:4326', inplace=True)
    minx, miny, maxx, maxy = gdf.total_bounds
    print(gdf.total_bounds)
    isin_flag = False
    while 1:
        if isin_flag:
            break
        x, y = random_point(minx, miny, maxx, maxy)
        isin_flag = isin_area(gdf, x, y)
    # x, y = random_point(minx, miny, maxx, maxy)
    temp = gpd.tools.reverse_geocode([Point(x,y)]) # arcgis
    print(f"location,x: {x}, y: {y}")
    address=temp.loc[0, 'address']
    print(f"address: {temp.loc[0, 'address']}")

    write_history([x,y],temp.loc[0, 'address'])
    # create_map([[y,x]],[address])
    # create_map_by_plotly([[y,x]],[address])
