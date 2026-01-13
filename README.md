# YourOwnRAG - Your Own Retrieval Augmented Generation Chatbot

Un chatbot alimenté par **Retrieval Augmented Generation (RAG)** qui utilise une base de données vectorielle pour répondre aux questions en se basant sur des documents personnalisés.

## 🎯 Fonctionnalités

- **Chatbot Interactif** : Pose des questions et reçois des réponses en temps réel
- **Base de Données Vectorielle** : Indexation intelligent des documents via embeddings
- **Recherche Sémantique** : Retrouve les chunks les plus pertinents grâce à la similarité cosinus
- **Support Multi-Format** : Texte brut, code source, etc.
- **Modèles Open Source** : Utilise Ollama avec des modèles légers et efficaces

## 🏗️ Architecture

```
YourOwnRAG/
├── main.py                          # Point d'entrée principal
├── requirements.txt                 # Dépendances
├── src/
│   ├── loadingDataset.py           # Charge les données depuis des fichiers
│   ├── implementVectorDB.py         # Gestion de la base vectorielle
│   └── retrievalFunction.py         # Recherche sémantique
├── tmp/
│   └── cat-facts.txt                # Données d'exemple
└── vector_db/                       # Stockage des embeddings
```

## 📦 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/Jul1111/YourOwnRAG.git
cd YourOwnRAG/Version1
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer Ollama

Le projet utilise [Ollama](https://ollama.ai/) pour les embeddings et le modèle de langage.

```bash
# Installer Ollama depuis https://ollama.ai/
# Puis télécharger les modèles nécessaires
ollama pull nomic-embed-text      # Pour les embeddings
ollama pull llama2                 # Pour le modèle de langage
```

## 🚀 Utilisation

### Lancer le chatbot

```bash
python main.py
```

### Exemple d'interaction

```
==================================================
Chatbot is ready! Type "exit" to quit.
==================================================

You: Quelle est l'histoire des clowders?

Retrieved knowledge:
 - (similarity: 0.92) Un clowder est un groupe de chats...
 - (similarity: 0.87) Les clowders sont souvent observés...

Bot: Un clowder est un groupe de chats qui vivent ensemble...

You: exit
Goodbye!
```

## 🔧 Configuration

### Modifier la source de données

Éditez `main.py` pour charger vos propres documents :

```python
dataset = load_dataset('chemin/vers/votre/fichier.txt')
```

### Ajuster les paramètres de RAG

- **Taille des chunks** : Modifiez `chunk_size` dans `implementVectorDB.py`
- **Similarité minimale** : Ajustez `top_n` dans `main.py`
- **Modèles** : Changez `EMBEDDING_MODEL` ou `LANGUAGE_MODEL`

## 📚 Modules Principaux

### `implementVectorDB.py`

- Crée la base de données vectorielle avec embeddings
- Gère le découpage de texte adapté (code source vs texte brut)
- `create_vector_db_from_dataset()` : Indexe tous les chunks

### `retrievalFunction.py`

- Calcule la similarité cosinus entre embeddings
- `retrieve(query, top_n=3)` : Retrouve les chunks pertinents

### `loadingDataset.py`

- `load_dataset(filename)` : Charge les données depuis un fichier texte

## 💡 Comment fonctionne le RAG

1. **Indexation** : Les documents sont divisés en chunks et convertis en embeddings
2. **Recherche** : La question est transformée en embedding
3. **Similarité** : On trouve les chunks les plus proches sémantiquement
4. **Contexte** : Ces chunks sont passés au modèle de langage
5. **Génération** : Le modèle génère une réponse basée sur le contexte

## 🛠️ Technologies Utilisées

- **Ollama** : Modèles LLM open source
- **LangChain** : Splitting de texte et orchestration
- **Python** : Langage principal
- **Embeddings** : BGE (Base General Embedding)

## 📝 Roadmap

- [ ] Support des fichiers PDF
- [ ] Interface web (Streamlit/FastAPI)
- [ ] Persistance de la base vectorielle
- [ ] Fine-tuning sur domaines spécifiques
- [ ] Support du multi-langue

## 📄 Licence

MIT License - Voir LICENSE pour plus de détails

## ✨ Contributions

Les contributions sont bienvenues ! Ouvre une issue ou un PR pour proposer des améliorations.
