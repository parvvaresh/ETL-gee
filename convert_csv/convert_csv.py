from get_all_csv import get_all_csv
import pandas as pd

def conver_csv(folder_path : str,
               path_to_save : str) -> None:
    csv_files = get_all_csv(folder_path)

    result = dict()
    csv = pd.DataFrame()
    for  file in csv_files:
        path , name = file
        name = name.split(".csv")[0]

        Polygon = name.split("_")[0]


        if Polygon in result:
            result[Polygon].append(path)
        
        elif Polygon not in result:

            result[Polygon] = list()
            result[Polygon].append(path)
    
    for Polygon in result:
        df_temp = pd.DataFrame()
        all_Polygon = result[Polygon]
        for _Polygon in all_Polygon:
            df = pd.read_csv(_Polygon)
            df_temp = df_temp._append(df,
                    ignore_index = True)
        df_temp["id_Polygon"] = Polygon
        csv = csv._append(df_temp,
                    ignore_index = True)
        

    csv.to_csv(path_to_save)


conver_csv("/home/alireza/Desktop/usa_data", "usa_5_15")