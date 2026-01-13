import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
import loadingDataset

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

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
