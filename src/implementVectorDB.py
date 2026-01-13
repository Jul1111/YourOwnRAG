import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

#Fonction pour ajouter un chunk à la base de données vectorielle
def add_chunk_to_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  
  VECTOR_DB.append((chunk, embedding))

#Configuration du découpage pour du texte
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Taille maximale de chaque morceau (en caractères)
    chunk_overlap=50,     # Chevauchement pour garder le contexte
    length_function=len,
    is_separator_regex=False,
)

#Configuration du découpage pour du code source
text_splitter_code = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Taille maximale de chaque morceau (en caractères)
    chunk_overlap=50,     # Chevauchement pour garder le contexte
    length_function=len,
    is_separator_regex=False,
    separators=["class", "def", "\n\n", "\n", " ", ""],
)

#Fonction pour créer la base de données vectorielle à partir du dataset chargé
def create_vector_db_from_dataset(dataset):
    chunk_count = 0
    for data in dataset:
        if data.strip().endswith(('.py', '.js', '.java', '.cpp', '.cs', '.rb', '.go')):
            chunks = text_splitter_code.split_text(data)
        else:
            chunks = text_splitter.split_text(data)

        for chunk in chunks:
            add_chunk_to_database(chunk)
            chunk_count += 1
            print(f'Added chunk {chunk_count}/{len(VECTOR_DB)} to the database')
