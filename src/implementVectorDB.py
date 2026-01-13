import ollama
from src.loadingDataset import load_multiple_files

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def add_chunk_to_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  
  VECTOR_DB.append((chunk, embedding))

#Fonction pour créer la base de données vectorielle à partir du dataset chargé
def create_vector_db_from_dataset(chunks):
    """
    Ajoute les chunks déjà splitté à la base de données vectorielle.
    Les chunks doivent être pré-splitté par load_multiple_files()
    """
    chunk_count = 0
    for chunk in chunks:
        add_chunk_to_database(chunk)
        chunk_count += 1
        #print(f'Added chunk {chunk_count}/{len(VECTOR_DB)} to the database')

def reset_vector_db():
    global VECTOR_DB
    VECTOR_DB.clear()
