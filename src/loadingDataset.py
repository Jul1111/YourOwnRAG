import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Stratégies de splitting par type de fichier
SPLITTING_STRATEGIES = {
    # Fichiers de code
    'code': RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["class", "def", "\n\n", "\n", " ", ""],
    ),
    # Fichiers JSON/YAML/Config
    'config': RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        separators=["\n", " ", ""],
    ),
    # Fichiers texte brut
    'text': RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    ),
    'pdf': RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    ),
}

# Mapping extension -> type
FILE_TYPE_MAP = {
    # Code
    '.py': 'code', '.js': 'code', '.ts': 'code', '.jsx': 'code', '.tsx': 'code',
    '.java': 'code', '.cpp': 'code', '.c': 'code', '.h': 'code',
    '.cs': 'code', '.rb': 'code', '.go': 'code', '.rs': 'code',
    '.php': 'code', '.swift': 'code', '.kt': 'code', '.sql':'code',
    # Config
    '.json': 'config', '.yaml': 'config', '.yml': 'config',
    '.toml': 'config', '.ini': 'config', '.conf': 'config','.xml':'config',
    # Texte
    '.txt': 'text', '.md': 'text',
    #PDF
    'pdf':'pdf',
}

def get_file_type(filepath):
    """Détecte automatiquement le type de fichier."""
    _, ext = os.path.splitext(filepath)
    return FILE_TYPE_MAP.get(ext.lower(), 'text')  # Par défaut: texte

#Pour les fichiers PDF
def load_pdf(filepath):
    """Extrait le texte d'un PDF."""
    text = ""
    try:
        reader = PdfReader(filepath)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += f"\n[Page {page_num + 1}]\n{page_text}"
        return text
    except Exception as e:
        print(f"✗ Erreur en lisant le PDF {filepath}: {e}")
        return ""

# Fonction principale pour charger et splitter un fichier 'txt'
def load_and_split_file(filepath):
    """
    Charge et split un fichier automatiquement selon son type.
    Retourne les chunks déjà splitté.
    """
    file_type = get_file_type(filepath)
    splitter = SPLITTING_STRATEGIES[file_type]
    
    try:
        # Traitement spécial pour les PDFs
        if file_type == 'pdf':
            content = load_pdf(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        
        chunks = splitter.split_text(content)
        print(f"✓ {filepath} ({file_type}) -> {len(chunks)} chunks")
        return chunks
    
    except Exception as e:
        print(f"✗ Erreur en lisant {filepath}: {e}")
        return []

def load_multiple_files(paths):
    """
    Charge plusieurs fichiers/dossiers et les split intelligemment.
    Supporte: txt, code, json, yaml, pdf, et plus.
    
    Args:
        paths (list): Liste de chemins (fichiers ou dossiers)
    
    Returns:
        list: Tous les chunks extraits et splittés
    """
    all_chunks = []
    total_files = 0
    total_chunks = 0
    
    for path in paths:
        if not os.path.exists(path):
            print(f"⚠️ Le chemin n'existe pas: {path}")
            continue
            
        try:
            if os.path.isdir(path):
                # Parcourir le dossier
                print(f"\n📁 Traitement du dossier: {path}")
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    if os.path.isfile(filepath):
                        chunks = load_and_split_file(filepath)
                        if chunks:
                            all_chunks.extend(chunks)
                            total_files += 1
                            total_chunks += len(chunks)
            else:
                # Fichier unique
                print(f"\n📄 Traitement du fichier: {path}")
                chunks = load_and_split_file(path)
                if chunks:
                    all_chunks.extend(chunks)
                    total_files += 1
                    total_chunks += len(chunks)
        
        except Exception as e:
            print(f"✗ Erreur lors du traitement de {path}: {e}")
            continue
    
    print(f"\n✅ Résumé: {total_files} fichier(s) traité(s), {total_chunks} chunk(s) créé(s)")
    return all_chunks