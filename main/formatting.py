import pandas as pd

def formatting(
        data:pd.DataFrame, 
        weight_name:str, 
        type_of_weight:int,
        class_name:str="class", 
        geoposition_name:str="Геопозиция", 
        normalize:bool=True
    ) -> pd.DataFrame:

    classes = data[class_name].unique()

    max_in_class = {}
    for cl in classes:
        if normalize:
            max_value = data.loc[data[class_name] == cl][weight_name].max()
        else:
            max_value = 1
        max_in_class.update({cl: max_value})

    new_data = pd.DataFrame({"id":[], "longitude": [], "latitude":[], "modularity_class":[], "weight":[], "type_of_weight":[]})
    new_data = new_data.astype({"id": int, "modularity_class": int, "weight": float})

    for i in range(data.shape[0]-1, -1, -1):
        modularity_class = int(data.iloc[i][class_name])
        weight = float(data.iloc[i][weight_name])/max_in_class.get(modularity_class)
        latitude, longitude = data.iloc[i][geoposition_name][1:-1].split(",")
        row = [int(data.iloc[i].name), float(longitude), float(latitude), modularity_class, weight, type_of_weight]
        new_data = pd.concat([pd.DataFrame([row], columns=new_data.columns), new_data], ignore_index=True)

    new_data = new_data.set_index("id")

    # new_data.to_csv(res_path)
    # print(f"saved to {res_path}")
    return new_data