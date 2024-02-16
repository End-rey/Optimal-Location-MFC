import argparse

import folium
import pandas as pd
import colourmap as cm


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to csv file")
    parser.add_argument("column", help="Labels column name")
    parser.add_argument("-i", "--index", default=True, help="True, if csv file contains index column", 
                        type=lambda x: True if x == "True" else False)
    parser.add_argument("-t", "--top", default=None, help="Draw top N clusters", type=int)
    parser.add_argument("-w", "--weight", default=None, help="Weight column name, if exist", type=str)
    parser.add_argument("-n", "--normalize", default=False, help="True if you want to normalize weights")
    return parser


def get_top_clusters_df(df: pd.DataFrame, n: int) -> pd.DataFrame:
    df_most_used_clusters = df.groupby(by=["cluster"], as_index=False).count().sort_values(by=["id"], ascending=False).head(n)
    return df.loc[df["cluster"].isin(df_most_used_clusters["cluster"])]
    

def create_df(args) -> pd.DataFrame:
    print("Creating DataFrame")
    if args.index:
        df = pd.read_csv(args.path, index_col=0)
    else:
        df = pd.read_csv(args.path)
    df = df.drop_duplicates()

    df["cluster"] = df[args.column]
    if args.column != "cluster":
        df = df.drop(args.column, axis=1)

    if args.top is not None:
        df = get_top_clusters_df(df, args.top)
    
    if args.weight is not None and args.normalize:
        max_weight = df[args.weight].max()
        df["weight"] = df[args.weight].apply(lambda loc: loc/max_weight)
    elif args.weight is not None:
        df["weight"] = df[args.weight]

    print(df)

    df["color"], palette = cm.fromlist(df["cluster"], scheme="hex", cmap="Spectral")
    return df


def create_marker(x, map):
    weight = 1
    if "weight" in x.index and 1 >= x["weight"] >= 0.5:
        weight = 2
    elif "weight" in x.index and x["weight"] == 1.1:
        weight = 10
    elif "weight" in x.index and x["weight"] > 1.1:
        weight = 15
    marker = folium.CircleMarker(location = (x["latitude"], x["longitude"]),
                                 fill_opacity = 0.6, 
                                 radius = weight,
                                 popup= f"{x['weight']}, {x.name}, {x['cluster']}" if "weight" in x.index else None,
                                 # fill_color = ,
                                 color = x["color"]).add_to(map)


def create_map(df: pd.DataFrame, res_path:str="spb.html") -> None:
    print("Creating map")
    spb = folium.Map(location=[59.9386, 30.3141], min_lat= 59.5, min_lon=29.5, max_lat=60.5, max_lon=30.8, max_bounds=True, zoom_start=10)
    df.apply(lambda x: create_marker(x, spb), axis=1)
    spb.save(res_path)

def visualization(data:pd.DataFrame, column:str, weight:str, res_path:str, normalize:bool=False):
    
    data = data.drop_duplicates()
    data["cluster"] = data[column]
    if column != "cluster":
        data = data.drop(column, axis=1)
    
    if weight is not None and normalize:
        max_weight = data[weight].max()
        data["weight"] = data[weight].apply(lambda loc: loc/max_weight)
    elif weight is not None:
        data["weight"] = data[weight]

    print(data)

    data["color"], palette = cm.fromlist(data["cluster"], scheme="hex", cmap="Spectral")

    create_map(data, res_path)

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    df_nodes = create_df(args)
    create_map(df_nodes)