import osmium
import pandas as pd

class SubwayHandler(osmium.SimpleHandler):
    def __init__(self):
        super(SubwayHandler, self).__init__()
        self.subway = []

    def node(self, n):
        if n.tags.get("railway") == "station" and n.tags.get("station") == "subway":
            self.subway.append({"Name":n.tags.get('name'), "coordinates": (n.location.lat, n.location.lon)})


class SubwayEntrancesHandler(osmium.SimpleHandler):
    def __init__(self):
        super(SubwayEntrancesHandler, self).__init__()
        self.ids_subway_entrances = []
        self.ids_with_coordinates_subway_entrances = []
        self.entrances = []

    def node(self, n):
        if n.tags.get("railway") == "subway_entrance" or n.tags.get("construction:railway") == "subway_entrance":
            self.ids_subway_entrances.append(n.id)
            self.ids_with_coordinates_subway_entrances.append(
                {
                    "id": n.id,
                    "coordinates": (n.location.lat, n.location.lon), 
                    "Name": n.tags.get("name")
                })

    def relation(self, r):
        for member in r.members:
            if member.role in ["entrance", "entry_only"] or (member.role == "subway_entrance" and r.tags.get("subway") == "yes") and member.ref in self.ids_subway_entrances:
                for entrance in self.ids_with_coordinates_subway_entrances:
                    if entrance["id"] == member.ref:
                        name = entrance["Name"] if entrance["Name"] != None else r.tags.get("name")
                        norm = True
                        for res in self.entrances:
                            if name == res["Name"]:
                                norm = False
                        if norm:
                            self.entrances.append(
                                {
                                    "Name": name,
                                    "coordinates": entrance["coordinates"]
                                })


if __name__ == "__main__":

    h = SubwayEntrancesHandler()

    h.apply_file("Санкт-Петербург.osm.pbf")

    print(h.entrances)

    print(len(h.entrances))

    data = pd.DataFrame(h.entrances)

    print(data.head())

    data.to_csv("subway_entrances.csv", sep="\t")