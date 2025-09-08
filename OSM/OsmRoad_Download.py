import os
import osmnx as ox
import geopandas as gpd
# 定义矩形经纬度边界
south_lat, north_lat, west_lon, east_lon = 22.3993661, 22.890827, 113.5721309, 114.7907477
# 使用边界框下载道路网络
G = ox.graph_from_bbox(north_lat, south_lat, east_lon, west_lon, 
                      network_type='drive', simplify=True)
# 将图转换为GeoDataFrames
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
# 修复edges字段类型问题
def convert_list_columns(df):
    """将列表型字段转换为字符串类型"""
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
    return df
# 处理edges字段
gdf_edges = convert_list_columns(gdf_edges)
# 确保CRS正确
gdf_nodes = gdf_nodes.set_crs("EPSG:4326")
gdf_edges = gdf_edges.set_crs("EPSG:4326")
# 保存前处理嵌套结构（可选）
columns_to_keep = ['osmid', 'highway', 'length', 'geometry']  # 只保留必要字段
gdf_edges = gdf_edges[columns_to_keep]
# 保存为shapefile
output_folder = './Funding_China/Sz'
os.makedirs(output_folder, exist_ok=True)
gdf_nodes.to_file(os.path.join(output_folder, 'nodes.shp'))
gdf_edges.to_file(os.path.join(output_folder, 'edges.shp'))
print("道路网络已保存到：", output_folder)
