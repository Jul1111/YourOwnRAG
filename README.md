# YourOwnRAG - Your Own Retrieval Augmented Generation Chatbot

Un chatbot alimenté par **Retrieval Augmented Generation (RAG)** qui utilise une base de données vectorielle pour répondre aux questions en se basant sur vos documents personnalisés.

## 🎯 Fonctionnalités

- **Chatbot Interactif** : Pose des questions et reçois des réponses en temps réel
- **Base de Données Vectorielle** : Indexation intelligent des documents via embeddings
- **Recherche Sémantique** : Retrouve les chunks les plus pertinents grâce à la similarité cosinus
- **Support Multi-Format** : Texte brut (.txt), PDF, JSON, YAML, Code source (Python, JavaScript, Java, C++, etc.)
- **Splitting Intelligent** : Découpe automatiquement les fichiers selon leur type pour une meilleure cohérence
- **Modèles Open Source** : Utilise Ollama avec des modèles légers et efficaces
- **Interface Conviviale** : Sélection graphique de fichiers/dossiers (macOS/Windows)
- **Préparation BDD** : Architecture prête pour la persistance future en base de données

## 🏗️ Architecture

```
YourOwnRAG/
├── main.py                          # Point d'entrée - CLI + sélection fichiers
├── requirements.txt                 # Dépendances
├── src/
│   ├── loadingDataset.py           # Chargement & splitting multi-format
│   ├── implementVectorDB.py         # Gestion base vectorielle avec embeddings
│   └── retrievalFunction.py         # Recherche sémantique (similarité cosinus)
├── tmp/
│   ├── cat-facts.txt                # Données d'exemple
│   └── archive/                     # Autres données
├── data/                            # Votre dossier de données personnalisées
└── vector_db/                       # Stockage des embeddings (futur)
```

## 📦 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/Jul1111/YourOwnRAG.git
cd YourOwnRAG/Version1
```

### 2. Créer un environnement virtuel (Python 3.9+)

```bash
python3.9 -m venv .venv
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
# Puis démarrer Ollama en arrière-plan
ollama serve

# Dans un autre terminal, télécharger les modèles nécessaires
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf  # Embeddings
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF   # Modèle de langage
```

## 🚀 Utilisation

### Lancer le chatbot

```bash
python3 main.py
```

### Menu de Configuration

Au démarrage, vous avez 4 options :

```
Options:
1. Sélectionner des fichiers      → Ouvre un dialogue pour choisir des fichiers
2. Sélectionner des dossiers      → Ouvre un dialogue pour choisir des dossiers
3. Continuer sans charger         → Utilise la BDD existante (futur)
4. Utiliser les sources par défaut → Charge tmp/cat-facts.txt
```

Choisissez l'option 1 ou 2 pour une sélection graphique native (macOS/Windows).

### Exemple d'Interaction

```
Configuration de la base de connaissance
==================================================
Chatbot is ready! Type "exit" to quit.
==================================================

You: Quelle est l'histoire des clowders?

Retrieved knowledge:
 - (similarity: 0.92) Un clowder est un groupe de chats...
 - (similarity: 0.87) Les clowders sont souvent observés...

Chatbot response: Un clowder est un groupe de chats qui vivent ensemble...

You: exit
Goodbye!
```

## 📚 Formats Supportés

### Fichiers de Code

- [ ] **Python** (.py) (en cours)
- [ ] **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx) (en cours)
- [ ] **Java** (.java) (en cours)
- [ ] **C/C++** (.c, .cpp, .h) (en cours)
- [ ] **C#** (.cs) (en cours)
- [ ] **Ruby** (.rb) (en cours)
- [ ] **Go** (.go) (en cours)
- [ ] **Rust** (.rs) (en cours)
- [ ] **PHP** (.php) (en cours)
- [ ] **Swift** (.swift) (en cours)
- [ ] **SQL** (.sql) (en cours)

### Fichiers de Configuration

- [ ] **JSON** (.json) (en cours)
- [ ] **YAML** (.yaml, .yml) (en cours)
- [ ] **TOML** (.toml) (en cours)
- [ ] **INI** (.ini) (en cours)
- [ ] **XML** (.xml) (en cours)

### Documents

- [x] **Texte brut** (.txt)
- [ ] **Markdown** (.md) (en cours)
- [ ] **PDF** (.pdf) (en cours)

## 🔧 Fonctionnement Technique

### 1. **Chargement et Splitting Intelligent**

Le système détecte automatiquement le type de fichier et applique la bonne stratégie de splitting :

- **Code** : Découpe par fonctions/classes (`def`, `class`, `\n\n`)
- **Configuration** : Découpe par lignes (`\n`, espaces)
- **Texte** : Découpe par paragraphes (`\n\n`, `\n`)
- **PDF** : Découpe par pages puis par paragraphes

Chaque chunk : **300-500 caractères** avec **chevauchement de 50 caractères**

### 2. **Création de la Base Vectorielle**

```
Fichier → Découpage en chunks → Embedding via Ollama → Base vectorielle
```

### 3. **Recherche Sémantique**

```
Question → Embedding → Similarité cosinus → Top 3 chunks les plus proches
```

### 4. **Génération de Réponse**

```
Chunks pertinents + Question → LLM Ollama → Réponse contextualisée
```

## 🛠️ Configuration Avancée

### Modifier les Paramètres de Splitting

Dans [src/loadingDataset.py](src/loadingDataset.py) :

```python
SPLITTING_STRATEGIES = {
    'code': RecursiveCharacterTextSplitter(
        chunk_size=500,        # Augmentez pour plus de contexte
        chunk_overlap=50,      # Chevauchement entre chunks
        separators=[...],      # Ordre de priorité de séparation
    ),
    # ... autres stratégies
}
```

### Changer les Modèles

Dans [src/implementVectorDB.py](src/implementVectorDB.py) :

```python
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'
```

Remplacez par d'autres modèles disponibles sur Ollama.

### Ajuster la Recherche

Dans [main.py](main.py), modifiez `top_n` :

```python
retrieved_knowledge = retrieve(input_query, top_n=5)  # Au lieu de 3
```

## 📝 Roadmap

- [x] Support multi-format (texte, code, PDF, JSON, YAML)
- [x] Splitting intelligent par type
- [x] Menu de sélection graphique
- [x] Chatbot interactif
- [ ] Persistance en base de données SQLite/PostgreSQL
- [ ] API REST (FastAPI)
- [ ] Interface web (Streamlit/Gradio)
- [ ] Fine-tuning sur domaines spécifiques
- [ ] Support du multi-langue
- [ ] Cache des embeddings
- [ ] Historique des conversations

## 🛡️ Technologies Utilisées

- **Ollama** : Modèles LLM open source (embeddings + génération)
- **LangChain** : Splitting de texte et orchestration
- **PyPDF** : Extraction de texte depuis PDFs
- **Python 3.9+** : Langage principal

## 📄 Licence

MIT License - Voir LICENSE pour plus de détails

## ✨ Contributions

Les contributions sont bienvenues ! Vous pouvez :

- Signaler des bugs via les Issues
- Proposer des améliorations
- Soumettre des PRs

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur le repo GitHub !

---

**Bon RAGing ! 🚀**
