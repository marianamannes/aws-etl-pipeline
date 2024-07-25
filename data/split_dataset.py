import pandas as pd

# Load the dataset
dataset = pd.read_csv('global_superstore.csv', sep = ';', encoding='latin-1').sort_values('Row ID')

# Determine chunk size
chunk_size = len(dataset) // 5

# Split the dataset into chunks and save each chunk to a CSV file
end_row = 0
for i in range(5):
    start_row = i * chunk_size
    end_row += chunk_size 
    dataset_chunk = dataset[start_row:end_row]
    dataset_chunk.to_csv(f'datasets/dataset_{i+1}.csv', index=False)
    print(f'dataset {i+1}')
    print(f'start row = {start_row}, end row = {end_row}')
    print ('--------------------')