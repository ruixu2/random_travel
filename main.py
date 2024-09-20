import geopandas as gpd
import random
import config
from shapely.geometry import Point

def random_point(minx, miny, maxx, maxy):
    x = random.uniform(minx, maxx)
    y = random.uniform(miny, maxy)
    return x, y


def isin_area(_gdf, x, y):
    point=Point(x,y)
    res=_gdf['geometry'].contains(point)
    if True in res:
        print(res)
        print(f"{x}, {y} in area")
        return True
    return False


if __name__ == '__main__':
    gdf = gpd.read_file(config.area_file)
    gdf.to_crs(crs='EPSG:4326', inplace=True)
    minx, miny, maxx, maxy = gdf.total_bounds
    print(gdf.total_bounds)
    isin_flag = False
    # while 1:
    #     if isin_flag:
    #         break
    #     x, y = random_point(minx, miny, maxx, maxy)
    #     isin_flag = isin_area(gdf, x, y)
    x, y = random_point(minx, miny, maxx, maxy)
    temp = gpd.tools.reverse_geocode([Point(x,y)])
    print(f"location,x: {x}, y: {y}")
    print(f"address: {temp.loc[0, 'address']}")
