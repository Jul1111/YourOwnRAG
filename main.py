from src.loadingDataset import load_dataset
from src.implementVectorDB import create_vector_db_from_dataset

dataset = load_dataset('tmp/cat-facts.txt')

create_vector_db_from_dataset(dataset)