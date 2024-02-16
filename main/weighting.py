import pandas as pd
from scipy.spatial import KDTree
import os

def weighting(
        graph_path, 
        points_path, 
        name_of_weight, 
        top=256, 
        index_of_class_in_graph=-1, 
        index_of_weight_in_points=-1, 
        name_location_points="Геопозиция"
        ):

    # path = os.getcwd()
    graph = pd.read_csv( graph_path)
    points = pd.read_csv(points_path)

    if "Unnamed: 0" in graph.columns:
        graph = graph.drop("Unnamed: 0", axis=1)

    if "Unnamed: 0" in points.columns:
        points = points.drop("Unnamed: 0", axis=1)

    class_in_graph = graph.columns[index_of_class_in_graph]

    graph_most_used_clusters = graph.groupby(by=[class_in_graph], as_index=False).count().sort_values(by="id", ascending=False).head(top)
    graph_most_used_clusters = graph_most_used_clusters.loc[graph_most_used_clusters["id"] > 100]
    graph = graph.loc[graph[class_in_graph].isin(graph_most_used_clusters[class_in_graph])]
    graph["index"] = pd.RangeIndex(start=0, stop=graph.shape[0], step=1)
    graph = graph.set_index("index")

    graph_coordinates = graph[['latitude', 'longitude']].values
    points_coordinates = points[name_location_points].values

    weighted_graph = graph.copy()
    weighted_graph[name_of_weight] = 0

    points_with_class = points.copy()
    points_with_class["class"] = 0

    kdtree = KDTree(graph_coordinates)

    for i in range(points_coordinates.shape[0]):
        query_point = [float(coor) for coor in points_coordinates[i][1:-1].split(",")]
    
        distance, index = kdtree.query(query_point)

        weighted_graph.loc[index, name_of_weight] += points.iloc[i, index_of_weight_in_points]
        points_with_class.loc[i, "class"] = graph.iloc[index, index_of_class_in_graph]

    # name_of_graph = graph_path.split("/")[-1].split(".")[0]
    # path_weighted_graph = f"../data/graph/{name_of_graph}/{name_of_weight}.csv"
    # weighted_graph.to_csv(path_weighted_graph)
    # print(f"weighted graph saved to {path_weighted_graph}")

    # name_of_points = points_path.split("/")[-1].split(".")[0]
    # path_points_with_class = f"../data/result/{name_of_graph}/{name_of_points}_with_class.csv"
    # points_with_class.to_csv(path_points_with_class)
    # print(f"points with class saved to {path_points_with_class}")

    return weighted_graph, points_with_class