import pandas as pd
from weighting import weighting
from formatting import formatting
from centroid import centroid
from vis import visualization

def main():
    leiden = "../data/leiden_labels.csv"
    mod_0973 = "../data/lspb_5.csv"
    mod_new20 = "../data/Nodes (mod-new)20.0.csv"
    louvain = "../data/louvain_light.csv"
    results = [
        leiden, 
        mod_0973, 
        mod_new20, 
        louvain
        ]

    residents = "../data/result/Residents.csv"
    subway = "../data/result/subway_passangers_traffic.csv"
    plan_residents = "../data/result/plan_residents.csv"
    weights = [
        {"name": "residents", "data": residents, "weight_name": "Кол-во жильцов", "type_of_weight": 1},
        {"name": "subway", "data": subway, "weight_name": "Пассажирооборот", "type_of_weight": 2},
        {"name": "plan_residents", "data": plan_residents, "weight_name": "Кол-во жильцов", "type_of_weight": 3}
        ]

    for res in results:
        folder = "/".join(res.split("/")[:-1])
        print("folder", folder)
        name = res.split("/")[-1]

        layers = []
        for weight in weights:
            print("weighting", weight)
            weighted_graph, points_with_class = weighting(res, weight["data"], weight["name"])

            print("formatting")
            format_data = formatting(points_with_class, weight["weight_name"], weight["type_of_weight"])
            layers.append({"data": format_data, "name": weight["name"]})

        concat_residents_subway = pd.concat([layers[0]["data"], layers[1]["data"]], ignore_index=True)
        layers.append({"data": concat_residents_subway, "name": "concat_residents_subway"})
        concat_residents_subway_plan = pd.concat([concat_residents_subway, layers[2]["data"]], ignore_index=True)
        layers.append({"data": concat_residents_subway_plan, "name": "concat_residents_subway_plan"})

        for layer in layers:
            print("find centroid", layer["name"])
            data_with_centroid = centroid(layer["data"])
            visualization(data_with_centroid, "modularity_class", "weight", f"{folder}/centroid_{name}_{layer['name']}.html")
            data_with_centroid.to_csv(f"{folder}/centroid_{layer['name']}.csv")
        


if __name__ == "__main__":
    main()
