import os
import pandas as pd

folder_path = 'Places_IDs_Banks'
dfs = []
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)
df_concatenado = pd.concat(dfs, ignore_index=True)
df_concatenado.to_csv("data/place_id_banks.csv")
