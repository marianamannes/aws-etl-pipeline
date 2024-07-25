class Normalizer:
    def __init__(self, dataset):
        self.dataset = dataset

    def create_distinct_dataframes(self, schema_dict):
        df_dict = {}
        for key, value in schema_dict.items():
            df = self.dataset[value].copy()
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)
            df_dict[key] = df
        return df_dict
           