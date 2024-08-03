def create_distinct_dataframes(dataset, schema_dict):
    df_dict = {}
    for key, value in schema_dict.items():
        df = dataset[value].copy()
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        df_dict[key] = df
    return df_dict
        