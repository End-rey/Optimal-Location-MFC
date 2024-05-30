import osmium
import pandas as pd


class SubwayHandler(osmium.SimpleHandler):
    def __init__(self, ids):
        super(SubwayHandler, self).__init__()
        self.ids = ids
        self.geo = []

    def node(self, n):
        if n.id in self.ids:
            self.geo.append({"id": n.id, "longitude": n.location.lon,
                        "latitude": n.location.lat})


if __name__ == "__main__":
    print("start")
    data = pd.read_csv("Nodes (LSpb)_5.0_N259_M0985.csv")
    data = data.drop("Label", axis=1)
    data["latitude"] = None
    data["longitude"] = None
    print(data)

    h = SubwayHandler(data["id"].to_list())
    h.apply_file("Санкт-Петербург.osm.pbf")

    print("finish handler")
    print(len(h.geo))

    for v in h.geo:
        data.loc[data["id"] == v["id"], "longitude"] = v["longitude"]
        data.loc[data["id"] == v["id"], "latitude"] = v["latitude"]

    print("finish")
    print(data)
    print(data.loc[data["latitude"].isnull()])
    data.to_csv("lalala.csv")
