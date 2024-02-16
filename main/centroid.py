import pandas as pd

def centroid(
        data:pd.DataFrame,
        # res_path:str, 
        class_name:str = "modularity_class", 
        weight_name:str="weight"
    ):

    classes = data[class_name].unique()

    centroid = pd.DataFrame(columns=data.columns)

    for cl in classes:
        cluster = data.loc[data[class_name] == cl]
        lon = cluster["longitude"].sum()/cluster["longitude"].count()
        lat = cluster["latitude"].sum()/cluster["latitude"].count()
        weight = cluster[weight_name].sum()
        row = [
               lon,
               lat,
               cl,
               weight,
               10]
        lon_weighted = (cluster["longitude"]*cluster[weight_name]).sum()/cluster[weight_name].sum()
        lat_weighted = (cluster["latitude"]*cluster[weight_name]).sum()/cluster[weight_name].sum()
        data_weighted = cluster[weight_name].sum()
        row_weighted = [
               lon_weighted,
               lat_weighted,
               cl,
               data_weighted,
               11]

        centroid = pd.concat([pd.DataFrame([row], columns=centroid.columns), centroid], ignore_index=True)
        centroid = pd.concat([pd.DataFrame([row_weighted], columns=centroid.columns), centroid], ignore_index=True)

    data_with_centroids = pd.concat([data, centroid], ignore_index=True)
    data_with_centroids.index.name = "id"

    # data_with_centroids.to_csv(res_path)
    return data_with_centroids