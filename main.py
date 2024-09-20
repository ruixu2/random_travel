import geopandas as gpd
import random
import config
from shapely.geometry import Point
import os
import datetime

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
    if not os.path.exists("./history.txt"):
        f=open("history.txt",mode='w',encoding="utf-8")
        f.write("datetime;address;x;y\n")
        f.close()
    f=open("history.txt",mode='a',encoding='utf-8')
    t=datetime.datetime.now().strftime("%Y-%m-%d")
    x=round(point[0],4)
    y=round(point[1],4)
    f.write(f"{t};{address};{x};{y}\n")
    f.close()

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
    temp = gpd.tools.reverse_geocode([Point(x,y)],provider="arcgis")
    print(f"location,x: {x}, y: {y}")
    print(f"address: {temp.loc[0, 'address']}")
    write_history([x,y],temp.loc[0, 'address'])
